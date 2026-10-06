const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const KEY = 'ac3-jp-mission-tracker-v1';

function app(t, { start = '', saved, storageBlocked = false } = {}) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => errors.push(e.message));
  const dom = new JSDOM(html, {
    url: 'https://tsnl.github.io/ac3-guide/' + start,
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.confirm = () => true;
      w.HTMLElement.prototype.scrollIntoView = function () {};
      w.HTMLElement.prototype.scrollTo = function () {};
      w.HTMLDialogElement.prototype.showModal = function () { this.open = true; };
      w.HTMLDialogElement.prototype.close = function () { this.open = false; };
      if (saved) w.localStorage.setItem(KEY, saved);
      if (storageBlocked) Object.defineProperty(w, 'localStorage', { get() { throw new Error('blocked'); } });
    }
  });
  t.after(() => { dom.window.close(); assert.deepEqual(errors, []); });
  const w = dom.window, d = w.document;
  return { w, d, api: w.AC3Tracker, click: s => d.querySelector(s).dispatchEvent(new w.MouseEvent('click', { bubbles:true, cancelable:true })) };
}
const plain = x => JSON.parse(JSON.stringify(x));

test('public fresh start and after-02 preset do not assume an unconfirmed A', t => {
  const fresh = app(t);
  assert.deepEqual(Object.keys(fresh.api.getState().missions), []);
  assert.equal(fresh.d.querySelectorAll('.graph-node').length, 52);
  const current = app(t, { start: '?start=after02' });
  assert.equal(current.api.getState().missions[1].rank, '?');
  assert.equal(current.api.getState().missions[2].rank, 'A');
  current.click('[data-record="0"]');
  assert.equal(current.api.getState().missions[1].rank, '?');
  assert.equal(current.api.getState().missions[3].rank, 'A');
  assert.equal(current.api.getState().slots[0].after, 3);
});

test('route legs cover every A rank and ending and preserve the six-slot plan', t => {
  const { api, click, d } = app(t);
  for (let i = 0; i < 13; i++) click('[data-record="' + i + '"]');
  const s = api.getState();
  assert.equal(Object.values(s.missions).filter(m => m.rank === 'A').length, 52);
  assert.equal(Object.values(s.steps).filter(Boolean).length, 13);
  assert.deepEqual(plain(s.slots.map(x => x.after)), [33, 38, 18, 52, 47, 34]);
  for (const n of [7, 24, 34, 39]) assert.equal(s.missions[n].rank, 'A');
  assert.match(d.getElementById('next-banner').textContent, /All 52 A ranks/);
  click('#undo');
  assert.equal(api.getState().steps[12], undefined);
  assert.equal(api.getState().slots[1].after, 28);
  assert.equal(api.getState().missions[34].rank, 'A');
});

test('sequence has nine required repetitions and six checkpoint reloads', t => {
  const { api } = app(t);
  const data = api.getData();
  assert.equal(data.sequence.length, 61);
  assert.equal(new Set(data.sequence).size, 52);
  const repeats = [...new Set(data.sequence.filter((n, i, a) => a.indexOf(n) !== i))].sort((a,b)=>a-b);
  assert.deepEqual(plain(repeats), [4,7,9,20,24,28,34,39,43]);
  const links = new Set(data.edges.map(e => e.a+'-'+e.b));
  const reloads = [];
  for(let i=1;i<data.sequence.length;i++) if(!links.has(data.sequence[i-1]+'-'+data.sequence[i])) reloads.push([data.sequence[i-1],data.sequence[i]]);
  assert.deepEqual(plain(reloads), [[18,7],[52,39],[47,4],[21,20],[33,24],[34,34]]);
  assert.equal(data.plan.every(p => p.slot >= 1 && p.slot <= 6), true);
});

test('JSON round-trip preserves ranks, notes, route progress and slots across loads', t => {
  const { api, w, d, click } = app(t, { start: '?start=after02' });
  click('[data-record="0"]');
  const notes = d.getElementById('mission-notes');
  notes.value = 'Use missiles <only> & preserve this note.';
  notes.dispatchEvent(new w.Event('input', { bubbles: true }));
  click('[data-slot="5"]');
  d.getElementById('slot-mission').value = '3';
  d.getElementById('slot-label').value = 'Working backup';
  d.getElementById('slot-form').dispatchEvent(new w.Event('submit', { bubbles:true, cancelable:true }));
  assert.deepEqual(plain(api.validate(JSON.parse(api.exportJSON()))), plain(api.getState()));
  const restored = app(t, { saved: w.localStorage.getItem(KEY) });
  assert.deepEqual(plain(restored.api.getState()), plain(api.getState()));
  assert.equal(restored.api.getState().slots[5].label, 'Working backup');
});

test('invalid imports fail and imported notes cannot become HTML', async t => {
  const { api, d, w } = app(t);
  assert.throws(() => api.validate({ version: 9 }), /progress file/);
  const bad = api.getState(); bad.missions[1] = { rank: 'S' };
  assert.throws(() => api.validate(bad), /Invalid rank/);
  const s = api.getState();
  s.missions[1] = { rank:'A',notes:'</textarea><img id="injected" src=x onerror="alert(1)">' };
  s.selected = 1;
  const input = d.getElementById('import-file');
  Object.defineProperty(input, 'files', { configurable:true, value:[{size:1000,text:async()=>JSON.stringify(s)}] });
  input.dispatchEvent(new w.Event('change'));
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(api.getState().missions[1].rank, 'A');
  assert.equal(d.getElementById('injected'), null);
  assert.equal(d.getElementById('mission-notes').value, s.missions[1].notes);
});

test('rank filters, graph selection and branch visits remain synchronized', t => {
  const { d, w, api, click } = app(t);
  click('[data-tab="missions"]');
  d.getElementById('filter').value = 'branch';
  d.getElementById('filter').dispatchEvent(new w.Event('change'));
  assert.equal(d.querySelectorAll('#mission-rows tr').length, 12);
  click('#graph [data-select="39"]');
  assert.match(d.getElementById('mission-detail').textContent, /Power for Life/);
  const branch = d.querySelector('[data-edge="39-41"]');
  branch.checked = true; branch.dispatchEvent(new w.Event('change'));
  assert.equal(api.getState().branches['39-41'], true);
  click('#mark-a');
  assert.match(d.querySelector('#graph [data-select="39"]').getAttribute('class'), / a /);
});

test('progress still works and exports when storage is unavailable', t => {
  const { d, click, api } = app(t, { storageBlocked:true });
  assert.equal(d.getElementById('storage-warning').classList.contains('hidden'), false);
  click('#mark-a');
  assert.equal(JSON.parse(api.exportJSON()).state.missions[1].rank, 'A');
});

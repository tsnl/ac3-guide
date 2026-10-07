const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM,VirtualConsole}=require('jsdom');
const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
const KEY='ac3-jp-mission-tracker-v1';
const plain=x=>JSON.parse(JSON.stringify(x));
function app(t,{saved,blocked=false}={}){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(html,{url:'https://tsnl.github.io/ac3-guide/',runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.confirm=()=>true;w.HTMLElement.prototype.scrollIntoView=function(){};
  if(saved)w.localStorage.setItem(KEY,saved);
  if(blocked)Object.defineProperty(w,'localStorage',{get(){throw Error('blocked');}});
 }});
 t.after(()=>{dom.window.close();assert.deepEqual(errors,[]);});
 const w=dom.window,d=w.document,api=w.AC3Tracker;
 const click=sel=>d.querySelector(sel).click();
 const next=()=>d.querySelector('input[data-action]:not(:checked):not(:disabled)');
 return{w,d,api,click,next};
}

test('one mission box per attempt, six load boxes, five starred endings, only next enabled',t=>{
 const {d,api,next}=app(t),data=api.getData();
 assert.equal(data.actions.length,67);
 assert.equal(d.querySelectorAll('.action:not(.load)').length,61);
 assert.equal(d.querySelectorAll('.load').length,6);
 assert.equal(d.querySelectorAll('.ending .star').length,5);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,0);
 assert.equal(d.querySelectorAll('input[data-action]:disabled').length,66);
 assert.equal(next().dataset.action,'mission-01-1');
 for(const a of data.actions.filter(a=>a.type==='mission')){
  const card=d.getElementById(a.id);
  assert.deepEqual([...card.querySelectorAll('dt')].map(x=>x.textContent),a.decision?['Decision','Save after']:['Save after']);
  assert.equal(card.querySelector('.decision strong')?.textContent||'',a.decision);
 }
 assert.equal(d.querySelector('#mission-detail'),null);
 assert.equal(d.querySelector('[data-tab]'),null);
 for(const a of data.actions.filter(a=>a.type==='mission'))assert.ok(a.save && a.save.slot>=1 && a.save.slot<=6);
 assert.deepEqual(plain(data.actions.slice(0,6).map(a=>a.save.slot)),[1,1,1,2,2,2]);
});

test('checkbox completion unlocks one next action; skipped future events cannot advance',t=>{
 const {d,w,api,next,click}=app(t);
 const future=d.querySelector('[data-action="mission-03-1"]');
 future.checked=true;future.dispatchEvent(new w.Event('change',{bubbles:true}));
 assert.equal(api.getState().done['mission-03-1'],undefined);
 assert.equal(future.checked,false);
 next().click();assert.equal(next().dataset.action,'mission-02-1');
 next().click();assert.equal(next().dataset.action,'mission-03-1');
 assert.equal(d.querySelectorAll('input[data-action]:not(:checked):not(:disabled)').length,1);
 click('#undo');assert.equal(next().dataset.action,'mission-02-1');
 click('[data-action="mission-01-1"]');assert.equal(next().dataset.action,'mission-01-1');
 assert.equal(d.querySelector('[data-action="mission-02-1"]').disabled,true);
});

test('complete route covers 52 A ranks and valid saves; every load is an explicit gate',t=>{
 const {api,d,next}=app(t),data=api.getData(),slots={},best={},order=[],fresh=[],endingSlots=new Set();
 for(const action of data.actions){
  assert.equal(next().dataset.action,action.id);
  if(action.type==='load'){
   assert.equal(slots[action.slot],action.after);
   const i=data.actions.findIndex(a=>a.id===action.id),following=data.actions[i+1];
   assert.equal(d.querySelector('[data-action="'+following.id+'"]').disabled,true);
  }else{
   order.push(action.mission);
   if(action.rank==='A')best[action.mission]='A';
   const slot=action.save.slot,mode=slot in slots?'overwrite':'fresh';
   assert.equal(endingSlots.has(slot),false,'A completed ending must remain saved.');
   assert.equal(action.save.mode,mode);
   const instruction=d.getElementById(action.id).querySelector('.field.save dd').textContent;
   assert.ok(instruction.startsWith(mode==='fresh'?'Fresh save → Slot '+slot:'Overwrite Slot '+slot));
   if(mode==='fresh')fresh.push([action.mission,slot]);
   slots[slot]=action.mission;
   if(action.ending)endingSlots.add(slot);
  }
  next().click();
 }
 assert.equal(next(),null);
 assert.deepEqual(order,plain(data.sequence));
 assert.equal(Object.keys(best).length,52);
 assert.deepEqual(slots,{1:38,2:47,3:18,4:52,5:33,6:34});
 assert.deepEqual(fresh,[[1,1],[4,2],[7,3],[39,4],[20,5],[34,6]]);
 assert.equal(endingSlots.size,5);
 assert.equal(d.getElementById('count').textContent,'67 / 67');
 assert.equal(d.getElementById('jump').disabled,true);
});

test('JSON and browser reload preserve completion and next-action locking',t=>{
 const first=app(t);for(let i=0;i<20;i++)first.next().click();
 const exported=first.api.exportJSON(),validated=first.api.validate(JSON.parse(exported));
 assert.deepEqual(plain(validated),plain(first.api.getState()));
 const restored=app(t,{saved:first.w.localStorage.getItem(KEY)});
 assert.deepEqual(plain(restored.api.getState()),plain(first.api.getState()));
 assert.equal(restored.next().dataset.action,first.next().dataset.action);
});

test('v1 migration preserves notes and completed legs without marking every replay',t=>{
 const old={version:1,game:'ac3-jp',missions:{1:{rank:'A',notes:'Keep this note'},7:{rank:'A',notes:''}},steps:{0:true},slots:[{after:3,label:'Root checkpoint'}],branches:{'6-7':true}};
 const {api,d}=app(t,{saved:JSON.stringify(old)}),s=api.getState();
 assert.equal(s.version,2);
 assert.equal(s.done['mission-01-1'],true);
 assert.equal(s.done['mission-02-1'],true);
 assert.equal(s.done['mission-03-1'],true);
 assert.equal(s.done['mission-07-1'],true);
 assert.equal(s.done['mission-07-2'],undefined);
 assert.equal(s.done['load-1'],undefined);
 assert.equal(s.legacy.missions[1].notes,'Keep this note');
 assert.equal(s.legacy.slots[0].after,3);
 assert.equal(d.querySelectorAll('input[data-action]:not(:checked):not(:disabled)').length,1);
});

test('JSON import validates structure, retains old notes as data, and can be undone',async t=>{
 const {api,w,d,click}=app(t);
 assert.throws(()=>api.validate({version:9,game:'ac3-jp'}),/supported/);
 assert.throws(()=>api.validate({version:2,game:'ac3-jp',done:[]}),/Invalid/);
 const raw={version:1,game:'ac3-jp',missions:{1:{rank:'A',notes:'<img id="injected" src=x onerror="alert(1)">'}}};
 const input=d.getElementById('import-file');
 Object.defineProperty(input,'files',{configurable:true,value:[{size:500,text:async()=>JSON.stringify(raw)}]});
 input.dispatchEvent(new w.Event('change'));
 await new Promise(resolve=>setImmediate(resolve));
 assert.equal(api.getState().done['mission-01-1'],true);
 assert.equal(d.getElementById('injected'),null);
 assert.equal(JSON.parse(api.exportJSON()).state.legacy.missions[1].notes,raw.missions[1].notes);
 click('#undo');assert.deepEqual(Object.keys(api.getState().done),[]);
});

test('storage denial still allows checklist and JSON export',t=>{
 const {api,d,next}=app(t,{blocked:true});
 assert.equal(d.getElementById('storage-warning').classList.contains('hidden'),false);
 next().click();assert.equal(JSON.parse(api.exportJSON()).state.done['mission-01-1'],true);
});

test('all mission names link to a matching separate A-rank reference entry',t=>{
 const {d}=app(t),reference=fs.readFileSync(path.join(__dirname,'..','ranks.html'),'utf8');
 const doc=new JSDOM(reference);t.after(()=>doc.window.close());
 assert.equal(doc.window.document.querySelectorAll('section[id^="mission-"]').length,52);
 for(const link of d.querySelectorAll('.mission-title a')){
  const id=link.getAttribute('href').split('#')[1];assert.ok(doc.window.document.getElementById(id));
 }
});

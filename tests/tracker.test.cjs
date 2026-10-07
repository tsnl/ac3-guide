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

test('one mission box per attempt, six load boxes, five starred endings, next highlighted',t=>{
 const {d,api,next}=app(t),data=api.getData();
 assert.equal(data.actions.length,67);
 assert.equal(d.querySelectorAll('.action:not(.load)').length,61);
 assert.equal(d.querySelectorAll('.load').length,6);
 assert.equal(d.querySelectorAll('.ending .star').length,5);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,0);
 assert.equal(d.querySelectorAll('input[data-action]:disabled').length,0);
 assert.equal(d.querySelectorAll('[aria-current="step"]').length,1);
 assert.equal(next().dataset.action,'mission-01-1');
 assert.deepEqual([...d.querySelectorAll('.tools .menu-button')].map(x=>x.textContent),['Save','Load','Feedback','Credits']);
 assert.equal(d.getElementById('feedback').href,'https://github.com/tsnl/ac3-guide/issues/new');
 assert.equal(d.getElementById('credits').getAttribute('href'),'ranks.html#credits');
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

test('checking ahead confirms and fills earlier actions; unchecking clears every later action',t=>{
 const {d,w,api,next,click}=app(t);
 const prompts=[];w.confirm=msg=>{prompts.push(msg);return true;};
 click('[data-action="mission-05-1"]');
 assert.deepEqual(Object.keys(api.getState().done),['mission-01-1','mission-02-1','mission-03-1','mission-04-1','mission-05-1']);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,5);
 assert.equal(next().dataset.action,'mission-06-1');
 assert.equal(prompts.length,1);assert.match(prompts[0],/Broken Truce.*4 earlier unfinished actions/);
 click('[data-action="mission-02-1"]');assert.equal(next().dataset.action,'mission-02-1');
 assert.deepEqual(Object.keys(api.getState().done),['mission-01-1']);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,1);
 assert.equal(d.getElementById('mission-02-1').getAttribute('aria-current'),'step');
 click('[data-action="mission-01-1"]');assert.equal(next().dataset.action,'mission-01-1');
 assert.deepEqual(Object.keys(api.getState().done),[]);
 next().click();assert.equal(next().dataset.action,'mission-02-1');
 assert.equal(prompts.length,1,'Sequential completion and unchecking need no confirmation.');
});

test('cancelling a forward jump preserves both browser progress and checkbox state',t=>{
 const {d,w,api,next,click}=app(t);
 next().click();
 const before=plain(api.getState()),saved=w.localStorage.getItem(KEY);
 w.confirm=msg=>{assert.match(msg,/Enter Dision.*1 earlier unfinished action/);return false;};
 click('[data-action="mission-03-1"]');
 assert.deepEqual(plain(api.getState()),before);
 assert.equal(w.localStorage.getItem(KEY),saved);
 assert.equal(d.querySelector('[data-action="mission-03-1"]').checked,false);
 assert.equal(next().dataset.action,'mission-02-1');
});

test('progress advances and rewinds across reloads and repeated mission visits',t=>{
 const {d,api,next,click}=app(t);
 click('[data-action="mission-07-2"]');
 assert.equal(api.getState().done['mission-18-1'],true);
 assert.equal(api.getState().done['load-1'],true);
 assert.equal(api.getState().done['mission-07-2'],true);
 assert.equal(next().dataset.action,'mission-08-1');
 click('[data-action="load-1"]');
 assert.equal(api.getState().done['mission-18-1'],true);
 assert.equal(api.getState().done['load-1'],undefined);
 assert.equal(api.getState().done['mission-07-2'],undefined);
 assert.equal(next().dataset.action,'load-1');
 assert.equal(d.querySelector('[data-action="mission-07-1"]').checked,true);
});

test('complete route covers 52 A ranks and valid saves; pictograms preserve all six files',t=>{
 const {api,d,next}=app(t),data=api.getData(),slots={},best={},order=[],fresh=[],endingSlots=new Set();
 for(const action of data.actions){
  assert.equal(next().dataset.action,action.id);
  if(action.type==='load'){
   assert.equal(slots[action.slot],action.after);
   const i=data.actions.findIndex(a=>a.id===action.id),following=data.actions[i+1];
   assert.equal(d.querySelector('[data-action="'+following.id+'"]').checked,false);
  }else{
   order.push(action.mission);
   if(action.rank==='A')best[action.mission]='A';
   const slot=action.save.slot,mode=slot in slots?'overwrite':'fresh';
   assert.equal(endingSlots.has(slot),false,'A completed ending must remain saved.');
   assert.equal(action.save.mode,mode);
   const icons=[...d.getElementById(action.id).querySelectorAll('.save-slot')];
   assert.equal(icons.length,6);
   const targets=icons.filter(icon=>icon.classList.contains('is-target'));
   assert.equal(targets.length,1);
   assert.equal(targets[0].dataset.slot,String(slot));
   assert.equal(targets[0].classList.contains(mode),true);
   assert.equal(targets[0].querySelector('.slot-mark').textContent,mode==='fresh'?'+':'↻');
   const instruction=targets[0].getAttribute('aria-label');
   assert.ok(instruction.startsWith(mode==='fresh'?'Fresh save → Slot '+slot:'Overwrite Slot '+slot));
   if(mode==='fresh')fresh.push([action.mission,slot]);
   slots[slot]=action.mission;
   assert.deepEqual(plain(action.save.slots),Array.from({length:6},(_,i)=>slots[i+1]||null));
   for(let i=0;i<6;i++){
    assert.equal(icons[i].classList.contains('unused'),!(i+1 in slots));
    if(i+1!==slot&&endingSlots.has(i+1))assert.equal(icons[i].querySelector('.slot-mark').textContent,'★');
   }
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
 assert.equal(d.getElementById('progress').style.width,'100%');
});

test('JSON and browser reload preserve contiguous completion and the next action',t=>{
 const first=app(t);for(let i=0;i<20;i++)first.next().click();
 const exported=first.api.exportJSON(),validated=first.api.validate(JSON.parse(exported));
 assert.deepEqual(plain(validated),plain(first.api.getState()));
 const restored=app(t,{saved:first.w.localStorage.getItem(KEY)});
 assert.deepEqual(plain(restored.api.getState()),plain(first.api.getState()));
 assert.equal(restored.next().dataset.action,first.next().dataset.action);
});

test('old browser records and JSON with gaps resume at the first unfinished action',t=>{
 const old={version:2,game:'ac3-jp',done:{'mission-01-1':true,'mission-03-1':true,'mission-07-2':true}};
 const {api,d,next}=app(t,{saved:JSON.stringify(old)});
 assert.deepEqual(Object.keys(api.getState().done),['mission-01-1']);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,1);
 assert.equal(next().dataset.action,'mission-02-1');
 assert.deepEqual(Object.keys(api.validate({state:old}).done),['mission-01-1']);
 assert.deepEqual(Object.keys(api.validate({...old,done:{'mission-03-1':true}}).done),[]);
});

test('v1 migration preserves legacy notes and ranks while repairing progress gaps',t=>{
 const old={version:1,game:'ac3-jp',missions:{1:{rank:'A',notes:'Keep this note'},7:{rank:'A',notes:''}},steps:{0:true},slots:[{after:3,label:'Root checkpoint'}],branches:{'6-7':true}};
 const {api,d}=app(t,{saved:JSON.stringify(old)}),s=api.getState();
 assert.equal(s.version,2);
 assert.equal(s.done['mission-01-1'],true);
 assert.equal(s.done['mission-02-1'],true);
 assert.equal(s.done['mission-03-1'],true);
 assert.equal(s.done['mission-07-1'],undefined);
 assert.equal(s.done['mission-07-2'],undefined);
 assert.equal(s.done['load-1'],undefined);
 assert.equal(s.legacy.missions[1].notes,'Keep this note');
 assert.equal(s.legacy.missions[7].rank,'A');
 assert.equal(s.legacy.slots[0].after,3);
 assert.equal(d.querySelectorAll('input[data-action]:checked').length,3);
});

test('JSON import validates structure, retains old notes as data, and allows unchecking',async t=>{
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
 click('[data-action="mission-01-1"]');assert.deepEqual(Object.keys(api.getState().done),[]);
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

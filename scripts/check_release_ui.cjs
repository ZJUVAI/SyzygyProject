const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const html=fs.readFileSync(process.argv[2],'utf8');
const scripts=[...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)];
const data=JSON.parse(scripts.find(s=>s[1].includes('application/json'))[2]);
const code=scripts.find(s=>!s[1].includes('application/json'))[2];
class Element {
 constructor(tag='div'){this.tagName=tag;this.children=[];this.listeners={};this.attributes={};this._text='';}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=nodes;this._text='';}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}
 setAttribute(k,v){this.attributes[k]=v;}
 addEventListener(k,f){this.listeners[k]=f;}
 fire(k){assert(this.listeners[k]);this.listeners[k]({target:this});}
}
const elements=new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>[m[1],new Element()]));
elements.get('release-data').textContent=JSON.stringify(data);
elements.get('mathbench-release').querySelector=s=>{assert(s.startsWith('#'));assert(elements.has(s.slice(1)),s);return elements.get(s.slice(1));};
const saved=[],events={};
const window={openai:{setWidgetState:async s=>saved.push(s)},addEventListener:(k,f)=>events[k]=f};
vm.runInNewContext(code,{document:{getElementById:id=>elements.get(id),createElement:t=>new Element(t)},window});
const get=id=>elements.get('release-'+id);
assert(get('counts').textContent.includes('20 任务'));
assert.equal(get('tasks').children.length,20);
assert.equal(get('scores').children.length,4);
for(let i=0;i<data.tasks.length;i++){
 get('tasks').children[i].children[0].children[0].fire('click');
 assert(get('title').textContent.includes(data.tasks[i].task_id));
 assert.equal(get('scores').children.length,4);
 assert(get('exact').textContent.includes('independent_quantity'));
}
get('tasks').children[2].children[0].children[0].fire('click');
assert.equal(get('config').children.length,2);
get('config').value='T005-C02';get('config').fire('change');
assert(get('parameters').textContent.includes('32'));
assert.equal(saved.at(-1).modelContent.configuration_id,'T005-C02');
events['openai:set_globals']({detail:{globals:{widgetState:{privateContent:{mathbenchRelease:{task:'T073',config:'T073-C01'}}}}}});
assert(get('title').textContent.includes('T073'));
assert(get('scores').textContent.includes('578'));
assert(get('records').textContent.includes('未署发现者'));
assert(get('command').textContent.includes('replay T073'));
assert(!/<(?:html|head|body|!doctype)\b/i.test(html));
assert(Buffer.byteLength(html)<1000000);
console.log('UI logic passed: 20 task selections, two-config switch, exact scores, saved state, sources, replay command. Browser layout not tested.');

const formats={remote:{label:'ПИТАНИЕ ВАХТОВОЙ КОМАНДЫ',title:'Тёплая атмосфера.\nЗнакомые блюда.',text:'Разнообразные способы приготовления, меню «От шефа» и программы сбалансированного питания. Пространство и сервис адаптируются к условиям удалённого объекта.',image:'remote-food.webp',alt:'Столовая для команды на удалённом объекте',list:['Рационы под график работы','Разнообразие ежедневного меню','Учёт условий и потребностей команды']},canteen:{label:'ДЛЯ ПРЕДПРИЯТИЙ И ОФИСОВ',title:'Современная столовая.\nУдобный ежедневный сервис.',text:'Комплексные рационы с учётом графика предприятия. Популярные и международные блюда, гриль и предложения от шефа.',image:'canteen.webp',alt:'Современная корпоративная столовая с линией раздачи',list:['Эффективная линия раздачи','Современный интерьер','Комплексное питание сотрудников']},restaurant:{label:'ПРЕМИАЛЬНЫЙ ФОРМАТ',title:'Корпоративный ресторан.\nИндивидуальное обслуживание.',text:'Формат для небольших площадок: блюда от шефа, à la carte и предзаказ. Современное оборудование и натуральные материалы.',image:'restaurant.webp',alt:'Интерьер корпоративного ресторана',list:['Блюда от шефа и предзаказ','Комплексное питание','Индивидуальный сервис']},sanatorium:{label:'ПИТАНИЕ В САНАТОРИЯХ',title:'Питание с учётом\nпотребностей гостей.',text:'Заказное питание, шведский стол и система «всё включено». Лечебно-профилактические рационы по диетическим столам, питание гостей и персонала.',image:'sanatorium.webp',alt:'Иллюстрация светлого обеденного зала санатория',list:['Лечебно-профилактические рационы','VIP-обслуживание и доставка в номера','Рестораны, бары, кафе и мероприятия']}};
const tabs=[...document.querySelectorAll('[data-format]')];
function activate(tab){tabs.forEach(t=>{t.setAttribute('aria-selected',String(t===tab));t.tabIndex=t===tab?0:-1});const f=formats[tab.dataset.format];document.querySelector('#format-panel').setAttribute('aria-labelledby',tab.id);document.querySelector('#format-label').textContent=f.label;document.querySelector('#format-title').textContent=f.title;document.querySelector('#format-title').style.whiteSpace='pre-line';document.querySelector('#format-text').textContent=f.text;const im=document.querySelector('#format-image');im.src=new URL('assets/'+f.image,document.querySelector('link[rel=icon]').href.replace('assets/symbol.png','')).href;im.alt=f.alt;const list=document.querySelector('#format-list');list.replaceChildren(...f.list.map(text=>{const li=document.createElement('li');li.textContent=text;return li}))}
tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>activate(tab));tab.addEventListener('keydown',e=>{let n;if(e.key==='ArrowRight')n=(i+1)%tabs.length;if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==undefined){e.preventDefault();activate(tabs[n]);tabs[n].focus()}})});
const menu=document.querySelector('#menu');menu.addEventListener('click',()=>{const open=document.querySelector('header').classList.toggle('menu-open');menu.setAttribute('aria-expanded',String(open))});document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelector('header').classList.remove('menu-open');menu.setAttribute('aria-expanded','false')}));
const dialog=document.querySelector('#brief');document.querySelectorAll('[data-brief]').forEach(b=>b.addEventListener('click',()=>dialog.showModal()));document.querySelector('.close').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
document.querySelector('#brief-form').addEventListener('submit',e=>{e.preventDefault();const data=new FormData(e.currentTarget);const text='Запрос в РЕСК\n\nОбъект: '+data.get('object')+'\nКоличество людей и график: '+data.get('people')+'\nУслуги: '+(data.getAll('services').join(', ')||'Требуют уточнения')+'\nСрок запуска и задачи: '+data.get('task')+'\n';const url=URL.createObjectURL(new Blob(['\ufeff'+text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='Запрос-в-РЕСК.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);document.querySelector('#brief-status').textContent='Файл подготовлен для скачивания. Передайте его представителю РЕСК.'});

// Keep the format panel at the height required by its longest variant.
function lockFormatHeight(){
 const panel=document.querySelector('#format-panel');
 if(!panel)return;
 const copy=panel.querySelector('.format-copy');
 const width=copy.getBoundingClientRect().width;
 if(!width)return;
 const probe=copy.cloneNode(true);
 Object.assign(probe.style,{position:'absolute',visibility:'hidden',pointerEvents:'none',width:width+'px',height:'auto',inset:'auto',zIndex:'-1'});
 panel.append(probe);
 let max=0;
 for(const f of Object.values(formats)){
  probe.querySelector('#format-label').textContent=f.label;
  const title=probe.querySelector('#format-title');title.textContent=f.title;title.style.whiteSpace='pre-line';
  probe.querySelector('#format-text').textContent=f.text;
  probe.querySelector('#format-list').replaceChildren(...f.list.map(t=>{const li=document.createElement('li');li.textContent=t;return li}));
  max=Math.max(max,probe.getBoundingClientRect().height);
 }
 probe.remove();
 const stacked=matchMedia('(max-width:820px)').matches;
 const imageHeight=stacked?(matchMedia('(max-width:520px)').matches?240:320):0;
 panel.style.setProperty('--format-height',Math.ceil(stacked?max+imageHeight+2:Math.max(430,max+2))+'px');
}
let lastFormatWidth=0;
if(document.querySelector('#format-panel'))new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-lastFormatWidth)>1){lastFormatWidth=width;lockFormatHeight()}}).observe(document.querySelector('#format-panel'));
document.fonts.ready.then(lockFormatHeight);
window.addEventListener('resize',lockFormatHeight);

// Animate native details while keeping their background image anchored.
const disclosureState=new WeakMap();
document.querySelectorAll('.service details').forEach(details=>{
 details.querySelector('summary').addEventListener('click',event=>{
  event.preventDefault();
  const previous=disclosureState.get(details);
  const opening=previous?!previous.opening:!details.open;
  const from=details.getBoundingClientRect().height;
  if(previous)previous.animation.cancel();
  details.style.height='auto';details.open=true;
  const to=opening?details.getBoundingClientRect().height:details.querySelector('summary').getBoundingClientRect().height;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches){details.open=opening;return}
  details.style.overflow='hidden';
  const animation=details.animate([{height:from+'px'},{height:to+'px'}],{duration:300,easing:'cubic-bezier(.2,.7,.2,1)'});
  disclosureState.set(details,{animation,opening});
  animation.onfinish=()=>{details.open=opening;details.style.height='';details.style.overflow='';disclosureState.delete(details)};
 });
});

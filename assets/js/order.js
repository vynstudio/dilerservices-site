(function(){
var f=document.querySelector('.ds-order');if(!f)return;
var P=window.DS_PRODUCTS||{},email=window.DS_EMAIL||'';
var steps=f.querySelectorAll('fieldset[data-step]'),ind=document.querySelectorAll('.ds-step'),cur=1,N=steps.length;
var back=f.querySelector('[data-back]'),next=f.querySelector('[data-next]'),sub=f.querySelector('[data-submit]'),msg=f.querySelector('.dzFormMsg');
var $=function(s){return document.querySelector(s)};
function links(){return window.DS_PAYMENT_LINKS||{}}
function money(c){var d=c/100;return '$'+(c%100?d.toFixed(2):String(d)).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
function val(n){var e=f.querySelector('input[name="'+n+'"]:checked');return e?e.value:''}
var ref='DS-'+new Date().toISOString().slice(2,10).replace(/-/g,'')+'-'+Math.random().toString(36).slice(2,6).toUpperCase();
function cart(){
 var base=val('product'),items=[],einBox=f.querySelector('input[name="ein"]'),einOk=(base!=='formation-bundle'&&base!=='ein-filing');
 einBox.disabled=!einOk;if(!einOk)einBox.checked=false;einBox.closest('.ds-ein-addon').classList.toggle('ds-off',!einOk);
 var noRa=f.querySelector('input[name="ra"][value=""]');noRa.disabled=(base==='registered-agent-only');
 if(noRa.disabled&&noRa.checked)f.querySelector('input[name="ra"][value="registered-agent-yearly"]').checked=true;
 if(base!=='registered-agent-only')items.push(base);
 if(einBox.checked)items.push('ein-addon');
 var ra=val('ra');if(ra)items.push(ra);
 var fees=0,state=0,unknown=false,renew=[];
 items.forEach(function(k){var p=P[k];fees+=p.fee;if(p.state===null)unknown=true;else state+=p.state;if(p.renew)renew.push(p.name.replace(/ \(.*/,'')+' renews at '+money(p.fee)+' per '+p.renew+'.')});
 var notes=[];if(unknown)notes.push('Plus the state fee at cost for this filing. Diler Services confirms the exact state fee by email before filing.');
 notes=notes.concat(renew);
 var payKeys=items.map(function(k){return P[k].pay_key||k});
 var L=links(),url=L[payKeys.join('+')]||(payKeys.length===1?L[payKeys[0]]:'')||'';
 return {items:items,fees:fees,state:state,total:fees+state,unknown:unknown,note:notes.join(' '),url:url,base:base,ein:einBox.checked};
}
function render(){
 var c=cart(),rows=$('[data-sum-rows]');rows.textContent='';
 c.items.forEach(function(k){var p=P[k],tr=document.createElement('tr');
  [p.name,money(p.fee),p.state===null?'At cost':(p.state?money(p.state):'None')].forEach(function(t,i){var td=document.createElement(i?'td':'th');if(!i)td.scope='row';td.textContent=t;tr.appendChild(td)});rows.appendChild(tr)});
 $('[data-sum-fees]').textContent=money(c.fees);$('[data-sum-state]').textContent=c.unknown?(c.state?money(c.state)+' + at cost':'At cost'):money(c.state);
 $('[data-sum-total]').textContent=money(c.total);$('[data-sum-note]').textContent=c.note;
 f.querySelector('[data-running]').textContent='Total due today: '+money(c.total);
 f.querySelector('[data-total]').textContent=money(c.total);f.querySelector('[data-total-note]').textContent=c.note;
 f.querySelector('[data-bundle-tip]').hidden=!(c.base==='llc-formation'&&c.ein);
 f.querySelector('[data-ra-req]').hidden=c.base!=='registered-agent-only';
 f.querySelector('[data-paynote-link]').hidden=!c.url;f.querySelector('[data-paynote-manual]').hidden=!!c.url;
 sub.innerHTML=(c.url?'Pay '+money(c.total)+' securely':'Submit order')+' <span><i class="fa-solid fa-arrow-right"></i></span>';
 var set=function(k,v){f.querySelector('[data-f="'+k+'"]').value=v};
 set('ref',ref);set('items',c.items.map(function(k){return P[k].name+' ('+P[k].note+')'}).join('; '));
 set('fees',money(c.fees));set('state',money(c.state)+(c.unknown?' plus state fee at cost':''));set('total',money(c.total)+(c.note?' ('+c.note+')':''));
 set('pay',c.url?'Sent to online checkout':'Not paid. Email a secure payment link within 1 business day.');
 f.querySelector('[data-subject]').value='New order '+ref+': '+(c.items.map(function(k){return P[k].name}).join(', ')||'Registered agent')+': Diler Services';
 var dl=f.querySelector('[data-review]');dl.textContent='';
 var rv=[['Order reference',ref]].concat(c.items.map(function(k){return [P[k].name,money(P[k].fee)+' our fee'+(P[k].state===null?' + state fee at cost':(P[k].state?' + '+money(P[k].state)+' state fee':''))]}));
 ['Business name','Alternate name','Business type','Name','Email','Phone','Mailing address'].forEach(function(n){var el=f.elements[n];if(el&&el.value)rv.push([n==='Name'?'Full name':n,el.value])});
 rv.push(['Total due today',money(c.total)]);
 rv.forEach(function(r){var d=document.createElement('div'),a=document.createElement('dt'),b=document.createElement('dd');a.textContent=r[0];b.textContent=r[1];d.appendChild(a);d.appendChild(b);dl.appendChild(d)});
 return c;
}
function show(n){cur=n;steps.forEach(function(s){s.hidden=+s.dataset.step!==n});ind.forEach(function(i){i.classList.toggle('on',+i.dataset.stepInd<=n)});
 back.hidden=n===1;next.hidden=n===N;sub.hidden=n!==N;render();msg.textContent='';}
function valid(n){var ok=true;steps[n-1].querySelectorAll('[required]').forEach(function(el){if(ok&&!el.checkValidity()){ok=false;el.reportValidity();el.focus()}});return ok}
next.addEventListener('click',function(){if(valid(cur)){show(cur+1);var b=document.querySelector('.ds-order-box');if(b&&b.getBoundingClientRect().top<0)b.scrollIntoView({behavior:'smooth'})}});
back.addEventListener('click',function(){show(cur-1)});
f.addEventListener('change',render);f.addEventListener('input',function(){if(cur>=3)render()});
f.querySelector('[data-to-bundle]').addEventListener('click',function(){f.querySelector('input[name="product"][value="formation-bundle"]').checked=true;f.querySelector('input[name="ein"]').checked=false;render()});
f.reset();var q=new URLSearchParams(location.search),want=q.get('service');
function pick(v){var m=f.querySelector('input[name="product"][value="'+v+'"]');if(m)m.checked=true;return !!m}
if(want){if(want==='registered-agent'||want==='registered-agent-yearly'||want==='registered-agent-monthly'){pick('registered-agent-only');
  f.querySelector('input[name="ra"][value="'+(want==='registered-agent-monthly'?'registered-agent-monthly':'registered-agent-yearly')+'"]').checked=true}else pick(want)}
if(q.get('addon')==='ein')f.querySelector('input[name="ein"]').checked=true;
f.addEventListener('submit',function(e){e.preventDefault();for(var i=1;i<N;i++){if(!valid(i)){show(i);valid(i);return}}
 var c=render();sub.disabled=true;msg.innerHTML='<div class="alert-success">Sending your order...</div>';
 fetch(f.action,{method:'POST',headers:{Accept:'application/json'},body:new FormData(f)}).then(function(r){return r.json()}).then(function(j){if(!j.success)throw 0;
  if(c.url){var u=new URL(c.url);u.searchParams.set('prefilled_email',f.elements['Email'].value);u.searchParams.set('client_reference_id',ref);
   msg.innerHTML='<div class="alert-success">Order '+ref+' recorded. Opening secure checkout...</div>';location.href=u.toString();return}
  msg.innerHTML='<div class="alert-success"><b>Order '+ref+' received.</b> We\'ll email you a secure payment link within 1 business day. No payment has been taken.</div>';
  sub.hidden=true;back.hidden=true}).catch(function(){
  msg.innerHTML='<div class="alert-danger">The order could not be sent. Please email <a href="mailto:'+email+'">'+email+'</a> with order reference '+ref+'.</div>';sub.disabled=false})});
show(1);
})();

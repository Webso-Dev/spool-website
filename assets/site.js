// The thread: fill the frame's left guide up to the middle of the screen,
// and light each section's knot once the thread reaches it.
(function(){
  var win=document.querySelector('.win'), frame=document.querySelector('.frame'), blocks=[].slice.call(document.querySelectorAll('.frame .block'));
  if(!frame) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){frame.style.setProperty('--p',1);blocks.forEach(function(b){b.classList.add('lit')});return;}
  var ticking=false;
  function update(){
    ticking=false;
    // the hero window tilts upright over the first part of the scroll
    if(win) win.style.setProperty('--t',Math.min(1,window.scrollY/240).toFixed(3));
    var r=frame.getBoundingClientRect(), mid=window.innerHeight*0.6;
    var p=Math.max(0,Math.min(1,(mid-r.top)/r.height));
    frame.style.setProperty('--p',p.toFixed(4));
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(update)}},{passive:true});
  window.addEventListener('resize',update);update();
})();
// Example ticket tabs
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tabs [role=tab]'));
  var area=document.querySelector('.ex-area'), seen=false, timer;
  if(!area) return;
  // Rows arrive one at a time; each is ticked off when the next one starts, and the list scrolls up.
  function play(){
    clearTimeout(timer);
    var k=area.querySelector('.tk:not([hidden])'), list=k.querySelector('.steps'), rows=[].slice.call(list.children), view=k.querySelector('.feed'), n=0;
    rows.forEach(function(r){r.classList.remove('on','done')});
    (function step(){
      if(n>0) rows[n-1].classList.add('done');
      if(n===rows.length){timer=setTimeout(play,3200);return;}
      var r=rows[n++]; r.classList.add('on');
      list.style.transform='translateY('+Math.min(0,view.clientHeight*.5-(r.offsetTop+r.offsetHeight/2))+'px)';
      timer=setTimeout(step,1500);
    })();
  }
  function pick(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on});if(seen)play();}
  if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){
    area.classList.add('anim');
    [].forEach.call(area.querySelectorAll('.steps'),function(l){[].forEach.call(l.children,function(r,i){r.style.setProperty('--i',i)})});
    // when the list is scrolled to, the rows ease in one after another, then the first step starts
    var feeds=[].slice.call(area.querySelectorAll('.feed'));
    var io=new IntersectionObserver(function(e,o){
      if(!e.some(function(x){return x.isIntersecting})) return; o.disconnect();
      feeds.forEach(function(f){f.classList.add('intro','in')});
      timer=setTimeout(function(){feeds.forEach(function(f){f.classList.remove('intro')});seen=true;play();},1100);
    },{threshold:.6});
    feeds.forEach(function(f){io.observe(f)}); // whichever example is open when the list comes into view
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){pick(t)});
    t.addEventListener('keydown',function(e){var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!d)return;var n=tabs[(i+d+tabs.length)%tabs.length];pick(n);n.focus();});
  });
})();
// Comparison: the question and the cards share one pinned stage. Scrolling far enough, or choosing,
// swaps them with a class change only; the page is never scrolled or re-laid-out by script.
(function(){
  var sec=document.getElementById('why'); if(!sec) return;
  var ask=sec.querySelector('.ask'), stage=sec.querySelector('.ask-in'), res=sec.querySelector('.res');
  var big=[].slice.call(sec.querySelectorAll('.pick button')), small=[].slice.call(sec.querySelectorAll('.switch button')), panels=[].slice.call(sec.querySelectorAll('.gains'));
  var pinned=window.matchMedia('(min-width:901px) and (min-height:640px)'), motion=!window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var shown=false, cur=0, askTop=0, travel=1;
  function draw(){if(!motion)return;var g=panels[cur];g.classList.remove('go');void g.offsetWidth;g.classList.add('go');}
  function pick(i){cur=i;
    small.forEach(function(x,k){x.setAttribute('aria-pressed',k===i)});
    panels.forEach(function(g,k){g.hidden=k!==i});draw();}
  // Swap to the cards and stop pinning. The section collapses to the height of the cards; the page is
  // moved once, by exactly the space that disappeared above, so what is on screen does not jump.
  function show(){
    if(shown)return;shown=true;
    // keep whatever the reader is looking at where it is: the cards if they are on screen, otherwise the
    // content after this section
    var on=pinned.matches, r=stage.getBoundingClientRect(), stageSeen=r.top>-40&&r.top<window.innerHeight;
    function ref(){return stageSeen?stage.getBoundingClientRect().top:ask.getBoundingClientRect().bottom;}
    var before=on?ref():0;
    stage.classList.add('shown');ask.classList.add('done');
    if(on&&(stageSeen||before<=window.innerHeight)){var d=ref()-before; if(Math.abs(d)>1) window.scrollBy({top:d,behavior:'instant'});}
    draw();
  }
  // measure once (and on resize): the taller of the two card sets fixes the stage height
  function measure(){
    var h=0;panels.forEach(function(g,k){panels.forEach(function(x,j){x.hidden=j!==k});h=Math.max(h,res.offsetHeight)});
    panels.forEach(function(g,k){g.hidden=k!==cur});
    if(!shown) ask.style.setProperty('--h',h+'px');
    askTop=ask.getBoundingClientRect().top+window.scrollY; travel=Math.max(1,ask.offsetHeight-stage.offsetHeight);
  }
  big.forEach(function(b,i){b.addEventListener('click',function(){pick(i);if(pinned.matches)show();else panels[i].scrollIntoView({block:'start'});})});
  small.forEach(function(b,i){b.addEventListener('click',function(){pick(i)})});
  if(motion) sec.classList.add('draw');
  measure();
  // While reading, the swap happens as soon as the question has been held long enough. During a jump
  // (a link, or a very fast scroll) nothing is touched until scrolling has stopped.
  function past(){var sticky=parseFloat(getComputedStyle(stage).top)||0;return (window.scrollY+sticky-askTop)/travel>.8;}
  var tick=false, lastY=window.scrollY, jumpUntil=0, idle;
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(a)jumpUntil=Date.now()+2500;});
  window.addEventListener('scroll',function(){
    if(shown||!pinned.matches) return;
    var y=window.scrollY, step=Math.abs(y-lastY); lastY=y;
    if(Date.now()<jumpUntil||step>160){clearTimeout(idle);idle=setTimeout(function(){if(past())show()},180);return;}
    if(tick) return; tick=true;
    requestAnimationFrame(function(){tick=false;if(past())show();});
  },{passive:true});
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(measure,150)});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(measure);
  window.addEventListener('load',measure);
  // small screens: the cards sit below the question, so draw them when they scroll into view
  if(motion&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(e,o){if(!e.some(function(x){return x.isIntersecting}))return;o.disconnect();if(!pinned.matches)draw();},{threshold:.3});
    panels.forEach(function(g){io.observe(g)});
  }
})();
// Hero queue: tickets move through the steps; a finished one makes room for the next.
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var rows=[].slice.call(document.querySelectorAll('.hrow:not([data-hold])')); if(!rows.length) return;
  var steps=['Planned','Building','Testing','In review','Live'];
  var next=[['Renew TLS certificate on the order API','Dependency scan'],['Fix duplicate rows in the stock report','Error logs'],['Update Node.js 18 to 22 in the label printer service','Dependency scan'],['Add cost centre to purchase invoices','Request from Liisa'],['Supplier price list moves to a new format','API change'],['Patch log4j in the warehouse sync','Security advisory']];
  var n=1048, k=0, turn=0;
  function paint(r,st){var s=+r.style.getPropertyValue('--s'), b=r.querySelector('.st'); b.textContent=steps[s]; b.className='st'+(s===4?' live':s>0?' run':'');}
  setInterval(function(){
    if(document.hidden) return;
    var r=rows[turn++%rows.length], s=+r.style.getPropertyValue('--s');
    if(s<4){r.style.setProperty('--s',s+1);paint(r);return;}
    r.classList.add('swap');
    setTimeout(function(){var t=next[k++%next.length];r.querySelector('.id').textContent='SP-'+(n++);r.querySelector('.t').textContent=t[0];r.querySelector('.src').textContent=t[1];r.style.setProperty('--s',0);paint(r);r.classList.remove('swap');},380);
  },1300);
})();

// Comparison cards outside the pinned section (the Compare and Pricing pages): draw the dot figures when scrolled to
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)) return;
  var g=[].slice.call(document.querySelectorAll('.gains')).filter(function(x){return !x.closest('#why')});
  if(!g.length) return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('go');io.unobserve(e.target);}})},{threshold:.35});
  g.forEach(function(x){x.parentNode.classList.add('draw');io.observe(x)});
})();

// The short quiz before the call: three clicks (or skip), then an email with the answers already filled in.
(function(){
  var box=document.querySelector('[data-quiz]'); if(!box) return;
  var MAIL='hello@hellospool.com', motion=!window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Q=[
    {k:'Maintained by',q:'Who maintains your custom software today?',a:['An outside vendor','Our own developers','A mix of both','Nobody, really']},
    {k:'Systems',q:'How many systems are we talking about?',a:['One','Two to five','More than five','Not sure yet']},
    {k:'Biggest problem',q:'What bothers you most about it?',a:['It costs too much','Changes take too long','We depend on one vendor or person','Updates and security fall behind'],other:'Or say it in your own words'}
  ];
  var ans=[], busy=false;
  function el(tag,cls,text){var e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}
  function link(text,fn){var b=el('button','quiz-back',text);b.type='button';b.addEventListener('click',fn);return b;}
  // Build one screen: k is the question number, Q.length is the last page.
  function screen(k,live){
    var f=document.createDocumentFragment(), last=k>=Q.length;
    var t=el('div','quiz-top');t.appendChild(el('span',null,last?'Ready':'Question '+(k+1)+' of '+Q.length));
    var m=el('div','quiz-meter');m.style.setProperty('--n',Q.length);m.style.setProperty('--k',Math.min(k+1,Q.length));t.appendChild(m);f.appendChild(t);
    var body=el('div','quiz-body');
    if(!last){
      body.appendChild(el('h3',null,Q[k].q));
      var o=el('div','quiz-opts');
      Q[k].a.forEach(function(a,i){var b=el('button',ans[k]===a?'picked':null,a);b.type='button';b.style.setProperty('--i',i);
        if(live)b.addEventListener('click',function(){if(busy)return;ans[k]=a;[].forEach.call(o.children,function(x){x.classList.remove('picked')});b.classList.add('picked');go(k+1,1,180)});o.appendChild(b)});
      body.appendChild(o);
      if(Q[k].other){ // a free-text answer for the last question
        var form=el('form','quiz-other'), inp=el('input'), ok=el('button','pill pill-sm','Next');
        inp.type='text';inp.maxLength=160;inp.placeholder=Q[k].other;inp.setAttribute('aria-label',Q[k].other);
        if(ans[k]&&Q[k].a.indexOf(ans[k])<0)inp.value=ans[k];
        ok.type='submit';form.appendChild(inp);form.appendChild(ok);
        if(live)form.addEventListener('submit',function(e){e.preventDefault();var v=inp.value.trim();if(!v){inp.focus();return;}if(busy)return;ans[k]=v;go(k+1,1)});
        body.appendChild(form);
      }
    }else{
      var some=ans.some(function(x){return x});
      body.appendChild(el('h3',null,some?'Thanks. That is enough to start the call in the right place.':'No problem. We can go through it on the call.'));
      var ul=el('ul','quiz-sum');
      Q.forEach(function(q,i){var li=el('li',ans[i]?null:'none');li.appendChild(el('span',null,q.k));var v=el('b',null,ans[i]||'Not answered');v.title=ans[i]||'';li.appendChild(v);ul.appendChild(li)});
      body.appendChild(ul);
    }
    f.appendChild(body);
    var foot=el('div','quiz-foot');
    if(!last){
      var bk=link('Back',function(){go(k-1,-1)}); if(!k)bk.style.visibility='hidden'; foot.appendChild(bk);
      foot.appendChild(link('Skip the questions',function(){go(Q.length,1)}));
    }else{
      var lines=Q.map(function(q,i){return ans[i]?q.k+': '+ans[i]:null}).filter(Boolean);
      var mail='Hello,\n\nWe would like a 30-minute call about our system.\n\n'+(lines.length?lines.join('\n')+'\n\n':'')+'Company: \nYour name: \nTimes that suit us: \n';
      var a=el('a','pill pill-blue','Book a 30-minute call');
      a.href='mailto:'+MAIL+'?subject='+encodeURIComponent('30-minute call about our system')+'&body='+encodeURIComponent(mail);
      foot.appendChild(a);foot.appendChild(link(ans.some(function(x){return x})?'Change an answer':'Answer the questions',function(){ans=[];go(0,-1)}));
      foot.classList.add('end');
    }
    f.appendChild(foot);return f;
  }
  function paint(k,dir){box.textContent='';box.appendChild(screen(k,true));box.dataset.dir=dir||0;box.classList.remove('in');void box.offsetWidth;box.classList.add('in');}
  // slide the old screen out, then the new one in; the box itself never changes size
  function go(k,dir,wait){
    if(busy)return;busy=true;
    setTimeout(function(){
      if(!motion){paint(k,0);busy=false;return;}
      box.dataset.dir=dir;box.classList.remove('in');box.classList.add('out');
      setTimeout(function(){box.classList.remove('out');paint(k,dir);busy=false;},190);
    },wait||0);
  }
  // one fixed height: as tall as the tallest screen at this width
  function size(){
    var keep=ans.slice(), max=0; box.style.minHeight='';
    for(var k=0;k<=Q.length;k++){ans=k===Q.length?Q.map(function(q){return q.a.reduce(function(a,b){return b.length>a.length?b:a})}):keep;box.textContent='';box.appendChild(screen(k,false));max=Math.max(max,box.offsetHeight);}
    ans=keep;box.style.minHeight=max+'px';
  }
  var cur=0; box.classList.add('on');
  var _paint=paint; paint=function(k,dir){cur=k;_paint(k,dir)};
  size();paint(0,0);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){size();_paint(cur,0)});
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){size();_paint(cur,0)},200)});
})();

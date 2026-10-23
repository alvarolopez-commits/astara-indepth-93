const DATA = /*__DATA__*/null;

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const $ = id => document.getElementById(id);
const fmt = v => Math.round(v).toLocaleString('en-US');
const fmtM = v => v>=1e6 ? (v/1e6).toFixed(2).replace(/0$/,'')+' m' : fmt(v);
const pct = (v,d=1) => (v*100).toFixed(d)+'%';
const ndNote = (list,what) => list.length ? `<span class="nd-note"><b>No data (ND) for ${what}:</b> ${list.map(esc).join(', ')}. ND means no defensible figure was found; it never means zero.</span>` : '';
const flag = (m,cls='') => { const f=DATA.flags[m]; if(!f) return '';
  return f==='blank' ? `<span class="flag flag--blank ${cls}" aria-hidden="true"></span>`   // plain white tile (Israel)
    : `<span class="flag ${cls}" style="background-image:url('deploy/flags/${f}.svg')" aria-hidden="true"></span>`; };
const mlab = (m,label,sub) => `<span class="row__mt">${label ?? esc(m)}${sub?`<small>${sub}</small>`:''}</span>${flag(m)}`;   // market label: name, optional sub-line, flag tile
const LAB = 'var(--lab)';   // space reserved at the end of a bar row for its value label (CSS: 92px, 70px on phones)

/* ================= summary — 12 plugs to 1 pump, one row at a time ================= */
function renderRatioViz(){
  const rows=6, plugs=12, S=44, R=12;
  const w=(plugs+1)*S, h=rows*S;
  let s=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Illustration: each of six rows shows 12 public charging points and 1 fuel station">`;
  for(let r=0;r<rows;r++){
    for(let k=0;k<=plugs;k++){
      const x=k*S+S/2, y=r*S+S/2, d=(r*(plugs+1)+k)*28;
      if(k<plugs) s+=`<g transform="translate(${x},${y})"><g class="rv__plug" style="--d:${d}ms"><circle r="${R}"/><path d="M1.5,-7 L-4,1 H0 L-1.5,7 L4,-1 H0 Z"/></g></g>`;
      else s+=`<g transform="translate(${x},${y})"><g class="rv__pump" style="--d:${d+120}ms"><rect x="-11" y="-14" width="22" height="28" rx="5"/><rect x="-6.5" y="-9" width="13" height="8" rx="2"/></g></g>`;
    }
  }
  $('ratio-viz').innerHTML=s+'</svg>';
}

/* ================= ch01 — public vs private vs vehicles (1 square = 1 million) ================= */
function renderUnits(){
  const R=[{n:7,v:'>7 m',t:'Public charging points',c:'var(--col-plug)'},
           {n:43,v:'>43 m',t:'Private points at homes and workplaces',c:'var(--col-cap)'},
           {n:76,v:'~76 m',t:'Electric light-duty vehicles (BEV + PHEV)',c:'var(--col-bev)'}];
  $('units').innerHTML=R.map(r=>`<div class="urow"><div class="urow__lab"><b style="color:${r.c}">${r.v}</b><span>${r.t}</span></div>`+
    `<div class="usq" role="img" aria-label="${r.t}: ${r.v}">${Array.from({length:r.n},(_,i)=>`<i style="background:${r.c};--i:${i}"></i>`).join('')}</div></div>`).join('');
}

/* ================= V02 — public points by market, fast vs slow ================= */
function barRow(m,segs,frac,val,cls='',i=0,lab=LAB){
  const fill=`<span class="row__fill" style="--i:${i};width:calc((100% - ${lab})*${frac})">${segs.map(([w,bg])=>`<i style="width:${w*100}%;background:${bg}"></i>`).join('')}</span>`;
  return `<div class="row ${cls}"><div class="row__m">${m}</div><div class="row__bar">${fill}<span class="row__v">${val}</span></div></div>`;
}
function ticks(vals,max,f){
  return `<div class="rows__axis"><span></span><div class="rows__ticks" style="margin-right:${LAB}">${vals.map(v=>`<span style="left:${v/max*100}%">${f(v)}</span>`).join('')}</div></div>`;
}
function pointSegs(d){
  return d.fast==null ? [[1,'var(--col-unsplit)']] : [[d.fast/d.total,'var(--col-fast)'],[d.slow/d.total,'var(--col-slow)']];
}
function renderPoints(){
  const P=[...DATA.points].sort((a,b)=>b.total-a.total), cn=P[0], rest=P.slice(1), max=500000;
  const val=d=>`${fmtM(d.total)}${d.share!=null?`<small>${Math.round(d.share*100)}% fast</small>`:''}`;
  let h=`<div class="rows" role="img" aria-label="Public charging points by market, end-2025: ${P.map(d=>`${d.m} ${fmt(d.total)}${d.share!=null?` (${pct(d.share)} fast)`:''}`).join('; ')}">`;
  h+=barRow(mlab('China',null,'own scale'),pointSegs(cn),1,val(cn),'row--hi row--sep',0);
  rest.forEach((d,i)=>{ h+=barRow(mlab(d.m),pointSegs(d),d.total/max,val(d),d.m==='South Korea'||d.m==='United States'?'row--hi':'',i+1); });
  h+='</div>'+ticks([0,100000,200000,300000,400000,500000],max,v=>v?(v/1000)+'k':'0');
  $('v02').innerHTML=h;
  $('v02-nd').innerHTML=ndNote(DATA.points_nd,'public points');
}

/* ================= V03 — China's share (waffle of 100) ================= */
function renderChina(){
  const C=DATA.china, n=Math.round(C.share*100);
  $('v03').innerHTML=`<div class="waffle" role="img" aria-label="China ${n} percent of the world's public charging points; rest of the world ${100-n} percent">`+
    Array.from({length:100},(_,i)=>`<i class="${i<n?'cn':''}" style="--i:${i}"></i>`).join('')+'</div>'+
    `<div class="waffle-k"><div><b style="color:var(--col-plug)">${n}%</b><span>${flag('China')} China</span><small>${fmtM(C.china)} public points</small></div>`+
    `<div><b style="color:var(--txt-sec)">${100-n}%</b><span>Rest of the world</span><small>${fmtM(C.rest)} public points</small></div></div>`;
}

/* ================= V04 — fuel stations ================= */
function renderStations(){
  const S=DATA.stations, max=125000;
  let h=`<div class="rows" role="img" aria-label="Fuel stations by market: ${S.map(d=>`${d.m} ${fmt(d.n)} (${d.date})`).join('; ')}">`;
  S.forEach((d,i)=>{
    const bg=d.grade==='C'?'var(--hatch-pump)':'var(--col-pump)';
    const sub=d.m==='United States'?'c-stores selling fuel':(d.m==='Mexico'?'permits in force':'');
    h+=barRow(mlab(d.m,null,sub),[[1,bg]],d.n/max,`${fmt(d.n)}<small>${esc(d.date)}${d.grade==='C'?' · indicative':''}</small>`,'',i);
  });
  h+='</div>'+ticks([0,25000,50000,75000,100000,125000],max,v=>v?(v/1000)+'k':'0');
  $('v04').innerHTML=h;
  $('v04-nd').innerHTML=ndNote(DATA.stations_nd,'fuel stations');
}

/* ================= V05 — fleet composition (100% stacked) ================= */
const SCOPE=s=>s.startsWith('All automobiles')?'ALL':(/light|4,536/i.test(s)?'LDV':'PC');
function renderFleets(){
  const F=[...DATA.fleets].sort((a,b)=>b.share-a.share);
  let h=`<div class="rows" role="img" aria-label="Electric share of the fleet by market: ${F.map(d=>`${d.m} ${pct(d.share)}`).join('; ')}">`;
  F.forEach((d,i)=>{
    const T=d.total, segs=[];
    if(d.bev==null) segs.push([d.ev/T,'var(--hatch-ev)']);
    else { segs.push([d.bev/T,'var(--col-bev)']);
      if(d.phev!=null) segs.push([d.phev/T,'var(--col-phev)']);
      else if(d.ev>d.bev) segs.push([(d.ev-d.bev)/T,'var(--hatch-ev)']); }
    segs.push([d.ice/T,'var(--col-ice)']);
    h+=barRow(mlab(d.m,`${esc(d.m)}<span class="tag">${SCOPE(d.scope)}</span>`,esc(d.date)),segs,1,pct(d.share),'',i,'52px');
  });
  h+='</div>';
  $('v05').innerHTML=h;
  $('v05-nd').innerHTML=ndNote(DATA.fleets_nd,'the fleet');
}

/* ================= V06 — two ratios, two panels, same order ================= */
const median=a=>{ const s=[...a].sort((x,y)=>x-y), m=s.length>>1; return s.length%2?s[m]:(s[m-1]+s[m])/2; };
function renderRatios(){
  const R=DATA.ratios, mxE=36, mxI=4000, mE=median(R.map(d=>d.evpp)), mI=median(R.map(d=>d.icepst));
  const W=48; // px for the value label inside each panel
  const cell=(v,max,col,txt,i,med)=>`<div class="pan__cell"><span class="pan__med" style="left:calc((100% - ${W}px)*${med/max})"></span><span class="row__fill" style="--i:${i};width:calc((100% - ${W}px)*${v/max});background:${col}"></span><span class="row__v">${txt}</span></div>`;
  const mark={'United States':'†','Brazil':'‡'};
  let h=`<div class="pan" role="img" aria-label="${R.map(d=>`${d.m}: ${d.evpp.toFixed(1)} EVs per public point, ${fmt(d.icepst)} combustion vehicles per station`).join('; ')}">`;
  h+=`<div class="pan__head"><span></span><div class="pan__h pan__h--ev">EVs per public charging point<small>median ${mE.toFixed(0)} · dashed line</small></div><div class="pan__h pan__h--ice">Combustion vehicles per fuel station<small>median ${fmt(mI)} · dashed line</small></div></div>`;
  R.forEach((d,i)=>{
    h+=`<div class="pan__row"><div class="row__m">${mlab(d.m,esc(d.m)+(mark[d.m]||''))}</div>`+
       cell(d.evpp,mxE,'var(--col-bev)',d.evpp.toFixed(1),i,mE)+cell(d.icepst,mxI,'var(--col-pump)',fmt(d.icepst),i,mI)+'</div>';
  });
  h+=`<div class="pan__foot"><span></span><span>Scale 0–${mxE}</span><span>Scale 0–${fmt(mxI)}</span></div></div>`;
  h+=`<p class="mini-note" style="margin-top:var(--sp-3);font-size:12px;color:var(--txt-muted);">† Fuel stations are convenience stores selling fuel only (a floor), so the US value is overstated. ‡ Registry fleet not purged of scrapped vehicles, so overstated.</p>`;
  $('v06').innerHTML=h;
}

/* ================= V07 — points per station, diverging from 1 on a log scale ================= */
function renderPPS(){
  const P=DATA.pps, lo=Math.log2(.25), hi=Math.log2(64), X=v=>(Math.log2(v)-lo)/(hi-lo), x1=X(1), W=44;
  const pos=f=>`calc((100% - ${W}px)*${f})`;
  let h=`<div class="v07-key"><span></span><div class="v07-key__z" style="--x:${pos(x1)}"><span class="l">← Pumps<br>outnumber plugs</span><span class="r">Plugs outnumber<br>pumps →</span></div></div>`;
  h+=`<div class="rows" role="img" aria-label="Public charging points per fuel station: ${P.map(d=>`${d.m} ${d.v.toFixed(1)}`).join('; ')}">`;
  P.forEach((d,i)=>{
    const x=X(d.v), a=Math.min(x,x1), w=Math.abs(x-x1), under=d.v<1;
    const lab=d.v.toFixed(1);
    const vlab=under?`<span class="row__v" style="position:absolute;right:calc(100% - ${pos(a)} + 6px)">${lab}</span>`:`<span class="row__v" style="position:absolute;left:calc(${pos(a+w)} + 6px)">${lab}</span>`;
    h+=`<div class="row${under?' row--hi':''}"><div class="row__m">${mlab(d.m,null,`${fmt(d.points)} / ${fmt(d.stations)}`)}</div>`+
       `<div class="row__bar" style="height:20px"><span class="ref" style="left:${pos(x1)}"></span>`+
       `<span class="row__fill" style="--i:${i};position:absolute;left:${pos(a)};width:${pos(w)};background:${under?'var(--col-pump)':'var(--col-plug)'};${under?'transform-origin:right;':''}"></span>${vlab}</div></div>`;
  });
  h+='</div>';
  const tk=[.25,.5,1,2,5,10,20,50];
  h+=`<div class="rows__axis"><span></span><div class="rows__ticks" style="margin-right:${W}px">${tk.map(v=>`<span style="left:${X(v)*100}%">${v}</span>`).join('')}</div></div>`;
  h+=`<p class="mini-note" style="margin-top:var(--sp-2);font-size:12px;color:var(--txt-muted);">Log scale. Under each market: public points / fuel stations.</p>`;
  $('v07').innerHTML=h;
}

/* ================= V08 — map ================= */
const BINS=[[0,1,'#FFB935','Below 1: more pumps than plugs'],[1,5,'#3F6FA8','1–5'],[5,15,'#5E98D2','5–15'],[15,30,'#93C9F4','15–30'],[30,Infinity,'#DDF1FF','30 or more']];
const binOf=v=>BINS.find(b=>v>=b[0]&&v<b[1]);
let mapView='world';
function renderMap(){
  const w=960, h=mapView==='world'?480:540;
  const topo=window.WORLD_110M; if(!topo){ $('v08').innerHTML='<p class="mini-note">Map data unavailable.</p>'; return; }
  const feats=topojson.feature(topo,topo.objects.countries).features.filter(f=>f.id!=='010');
  const byId=new Map(DATA.map.map(d=>[d.id,d])), pps=new Map(DATA.pps.map(d=>[d.m,d]));
  const proj=mapView==='world'
    ? d3.geoNaturalEarth1().fitExtent([[6,6],[w-6,h-6]],{type:'Feature',geometry:{type:'MultiPoint',coordinates:[[-168,72],[180,72],[-168,-52],[180,-52]]}})
    : d3.geoConicConformal().rotate([-12,0]).center([0,54]).parallels([40,65]).fitExtent([[6,6],[w-6,h-6]],{type:'Feature',geometry:{type:'MultiPoint',coordinates:[[-11,36],[34,36],[-11,71.5],[34,71.5]]}});
  const path=d3.geoPath(proj);
  let s=`<svg viewBox="0 0 ${w} ${h}" class="map-svg" role="img" aria-label="Map of public charging points per fuel station. ${DATA.map.map(d=>`${d.m}: ${d.v==null?'no data':d.v.toFixed(1)}`).join('; ')}">`;
  s+=`<defs><pattern id="ndhatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#3A3F66"/><line x1="0" y1="0" x2="0" y2="6" stroke="#6C7A9C" stroke-width="2"/></pattern><clipPath id="mclip"><rect width="${w}" height="${h}" rx="12"/></clipPath></defs>`;
  s+=`<rect class="sphere" width="${w}" height="${h}" rx="12"/><g clip-path="url(#mclip)">`;
  feats.forEach(f=>{
    const d=byId.get(f.id), p=path(f); if(!p) return;
    if(!d){ s+=`<path class="land" d="${p}"/>`; return; }
    const fill=d.v==null?'url(#ndhatch)':binOf(d.v)[2];
    s+=`<path class="mk" tabindex="0" data-id="${f.id}" d="${p}" fill="${fill}"><title>${esc(d.m)}: ${d.v==null?'no data':d.v.toFixed(1)+' public points per fuel station'}</title></path>`;
  });
  s+='</g></svg>';
  $('v08').innerHTML=s;
  // tooltip
  const tip=$('v08-tip'), wrap=tip.parentElement;
  const show=(e,el)=>{
    const d=byId.get(el.dataset.id), q=pps.get(d.m);
    tip.innerHTML=`<b>${flag(d.m)} ${esc(d.m)}</b>`+(d.v==null?'No data (ND)':`${d.v.toFixed(1)} public points per fuel station`+(q?`<br>${fmt(q.points)} points · ${fmt(q.stations)} stations (${esc(q.sdate)})`:''));
    tip.hidden=false;
    const r=wrap.getBoundingClientRect(), b=el.getBoundingClientRect();
    const x=(e&&e.clientX!=null?e.clientX:b.left+b.width/2)-r.left, y=(e&&e.clientY!=null?e.clientY:b.top+b.height/2)-r.top;
    tip.style.left=Math.min(Math.max(x+12,0),r.width-tip.offsetWidth)+'px'; tip.style.top=Math.max(y-tip.offsetHeight-12,0)+'px';
  };
  $('v08').querySelectorAll('.mk').forEach(el=>{
    el.querySelector('title').remove();
    el.addEventListener('mousemove',e=>show(e,el)); el.addEventListener('focus',()=>show(null,el));
    el.addEventListener('mouseleave',()=>tip.hidden=true); el.addEventListener('blur',()=>tip.hidden=true);
  });
}
function renderMapChrome(){
  $('v08-legend').innerHTML=BINS.map(b=>`<span><i style="background:${b[2]}"></i>${b[3]}</span>`).join('')+
    `<span><i style="background:repeating-linear-gradient(45deg,#3A3F66 0 3px,#6C7A9C 3px 5px)"></i>No data (ND)</span>`;
  const L=[...DATA.map].sort((a,b)=>(b.v??-1)-(a.v??-1)||a.m.localeCompare(b.m));
  const list=document.createElement('ul'); list.className='map-list';
  list.innerHTML=L.map(d=>`<li class="${d.v==null?'nd':''}"><span>${flag(d.m)} ${esc(d.m)}</span><b>${d.v==null?'ND':d.v.toFixed(1)}</b></li>`).join('');
  $('v08').parentElement.after(list);
  document.querySelectorAll('.seg__b').forEach(b=>b.addEventListener('click',()=>{
    mapView=b.dataset.view;
    document.querySelectorAll('.seg__b').forEach(x=>{ const on=x===b; x.classList.toggle('is-on',on); x.setAttribute('aria-pressed',on); });
    $('v08-tip').hidden=true; renderMap();
  }));
}

/* ================= V09 — scatter ================= */
const REG={'Europe':'#8BCDFF','Asia-Pacific':'#3EC6C6','North America':'#B79CFF','Latin America':'#FFB935'};
function renderScatter(){
  // phones get a narrower viewBox so that labels stay legible once the SVG is scaled down
  const narrow=$('v09').clientWidth<560, S=DATA.scatter, w=narrow?400:760, h=narrow?380:440, m={t:18,r:narrow?12:24,b:52,l:52};
  const x=d3.scaleLinear().domain([0,.42]).range([m.l,w-m.r]);
  const y=d3.scaleLog().domain([1,100]).range([h-m.b,m.t]);
  const LBL={'Norway':[8,4,'start'],'South Korea':[8,4,'start'],'Netherlands':[8,4,'start'],'China':[8,-6,'start'],'United States':[8,4,'start'],'New Zealand':[8,4,'start']};
  let s=`<svg viewBox="0 0 ${w} ${h}" class="sc-svg" role="img" aria-label="Scatter of EV share of the fleet against EVs per public point. ${S.map(d=>`${d.m}: ${pct(d.x)} EV share, ${d.y.toFixed(1)} EVs per point`).join('; ')}">`;
  s+='<g class="grid">'+[0,.1,.2,.3,.4].map(v=>`<line x1="${x(v)}" x2="${x(v)}" y1="${m.t}" y2="${h-m.b}"/>`).join('')+[1,2,5,10,20,50,100].map(v=>`<line x1="${m.l}" x2="${w-m.r}" y1="${y(v)}" y2="${y(v)}"/>`).join('')+'</g>';
  s+='<g class="ax">'+[0,.1,.2,.3,.4].map(v=>`<text x="${x(v)}" y="${h-m.b+18}" text-anchor="middle">${v*100}%</text>`).join('')+[1,2,5,10,20,50,100].map(v=>`<text x="${m.l-8}" y="${y(v)+4}" text-anchor="end">${v}</text>`).join('')+'</g>';
  s+=`<text class="axt" x="${w-m.r}" y="${h-10}" text-anchor="end">EV share of the fleet →</text>`;
  s+=`<text class="axt" x="${m.l-40}" y="${m.t-4}" text-anchor="start" transform="rotate(-90 ${m.l-40} ${m.t-4})" dx="-${h-m.b-m.t}">EVs per public point (log) →</text>`;
  S.forEach(d=>{ s+=`<circle class="dot" tabindex="0" data-m="${esc(d.m)}" cx="${x(d.x)}" cy="${y(d.y)}" r="${narrow?6:7}" fill="${REG[d.region]||'#DCE5ED'}" fill-opacity=".9" stroke="#292A4E" stroke-width="1.5"/>`; });
  S.filter(d=>LBL[d.m]).forEach(d=>{ const [dx,dy,a]=narrow&&d.m==='Norway'?[-9,-10,'end']:LBL[d.m]; s+=`<text class="lbl" x="${x(d.x)+dx}" y="${y(d.y)+dy}" text-anchor="${a}">${esc(d.m)}</text>`; });
  s+='</svg>';
  $('v09').innerHTML=s;
  $('v09-legend').innerHTML=Object.entries(REG).filter(([k])=>S.some(d=>d.region===k)).map(([k,c])=>`<span><i style="background:${c}"></i>${k}</span>`).join('');
  const tip=$('v09-tip'), wrap=tip.parentElement, by=new Map(S.map(d=>[d.m,d]));
  const show=(e,el)=>{
    const d=by.get(el.dataset.m);
    tip.innerHTML=`<b>${flag(d.m)} ${esc(d.m)}</b>EV share ${pct(d.x)} (${esc(d.date)})<br>${d.y.toFixed(1)} EVs per public point`;
    tip.hidden=false;
    const r=wrap.getBoundingClientRect(), b=el.getBoundingClientRect();
    const cx=b.left+b.width/2-r.left, cy=b.top-r.top;
    tip.style.left=Math.min(Math.max(cx-tip.offsetWidth/2,0),r.width-tip.offsetWidth)+'px'; tip.style.top=Math.max(cy-tip.offsetHeight-8,0)+'px';
  };
  $('v09').querySelectorAll('.dot').forEach(el=>{
    el.addEventListener('mouseenter',e=>show(e,el)); el.addEventListener('focus',()=>show(null,el));
    el.addEventListener('mouseleave',()=>tip.hidden=true); el.addEventListener('blur',()=>tip.hidden=true);
  });
}

/* ================= boot ================= */
renderRatioViz();
renderUnits();
renderPoints();
renderChina();
renderStations();
renderFleets();
renderRatios();
renderPPS();
renderMapChrome();
renderMap();
renderScatter();
let narrowNow=$('v09').clientWidth<560;
window.addEventListener('resize',()=>{ const n=$('v09').clientWidth<560; if(n!==narrowNow){ narrowNow=n; renderScatter(); } });

const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduce||!('IntersectionObserver' in window)){ document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible')); }
else{
  const obs=new IntersectionObserver(e=>{e.forEach(x=>{if(x.isIntersecting){x.target.classList.add('visible');obs.unobserve(x.target);}});},{threshold:0.06});
  document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));
}

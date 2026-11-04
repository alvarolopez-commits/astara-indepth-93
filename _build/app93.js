const DATA = /*__DATA__*/null;
const I18N = /*__I18N__*/null;   // {en: {key: text}, es: {key: text}}, built from _build/i18n/*.json, the docx and the Excel

/* ================= language (EN | ES) =================
   Every text on the page is a key of the catalog: elements carry data-i18n="key" (and data-i18n-attr="attr:key"),
   chart code calls t(key) for html and tp(key) for plain text. A missing key falls back to English and is
   listed in window.__i18nMiss. Keys under doc.* and mover.* hold plain text and are escaped here. */
let LANG = 'en';
const MISS = window.__i18nMiss = new Set();
const PLAIN = /^(doc|mover)\./;
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const tp = (k, a) => {
  let s = I18N[LANG][k];
  if(s === undefined){ MISS.add(k); s = I18N.en[k]; if(s === undefined) return k; }
  if(a) for(const [n, v] of Object.entries(a)) s = s.split(`{${n}}`).join(v);
  return s;
};
const t = (k, a) => PLAIN.test(k) ? esc(tp(k, a)) : tp(k, a);
const lead = s => { const i = s.indexOf(': '); return i < 0 ? esc(s) : `<b>${esc(s.slice(0, i + 1))}</b> ${esc(s.slice(i + 2))}`; };   // "Label: text" -> bold label
const dec = s => LANG === 'es' ? String(s).replace('.', ',') : String(s);                         // decimal comma in Spanish

const $ = id => document.getElementById(id);
const fmt = v => Math.round(v).toLocaleString(LANG === 'es' ? 'es-ES' : 'en-US');
const cotf = v => dec(v<.01 ? v.toFixed(4) : v<1 ? v.toFixed(3) : v<10 ? v.toFixed(2) : v.toFixed(1));   // 0.0031 · 0.060 · 0.172 · 2.27 · 15.0
const whf = v => v<10 ? dec(v.toFixed(1)) : fmt(v);
const ndNote = (text) => `<span class="nd-note">${text}</span>`;
const LAB = 'var(--lab)';   // space reserved at the end of a bar row for its value label (CSS: 92px, 70px on phones)
const at = f => `calc((100% - ${LAB})*${f})`;
const log10 = Math.log10;

const GRP = {'Living beings':['var(--g-live)','group.living'],'Human body':['var(--g-human)','group.human'],'Robots':['var(--g-robot)','group.robots'],'Moving people':['var(--g-people)','group.people'],'Moving goods':['var(--g-goods)','group.goods']};
const byId = L => Object.fromEntries(L.map(d => [d.id, d]));
const LAD = byId(DATA.ladder);
const BYNAME = {};   // mover name in the data -> id (the name shown comes from the catalog: mover.<id>)
for(const s of ['ladder','living','human','robots','people','goods','goods_whole']) for(const d of DATA[s]) if(!d.mover.endsWith('(reference)')) BYNAME[d.mover] = d.id;

/* gridlines behind a row of bars: [fraction, colour, width] -> one CSS background (read by .lr__bar) */
const grid = (list) => list.map(([f,c='var(--gl)',w=1]) => `linear-gradient(${c},${c}) calc((100% - var(--lab))*${f}) 0/${w}px 100% no-repeat`).join(',');
const lrow = (name, sub, bar, cls='') => `<div class="row lr ${cls}"><div class="row__m"><span class="row__mt">${name}${sub?`<small>${sub}</small>`:''}</span></div><div class="row__bar lr__bar">${bar}</div></div>`;
const axis = (vals, X, f) => `<div class="rows__axis"><span></span><div class="rows__ticks" style="margin-right:${LAB}">${vals.map(v => `<span style="left:${X(v)*100}%">${f(v)}</span>`).join('')}</div></div>`;
const whisker = (lo, hi, X) => `<span class="lr__wh" style="left:${at(X(lo))};width:calc((100% - ${LAB})*${X(hi)-X(lo)})"></span>`;
const valLabel = (f, txt) => `<span class="row__v lr__v" style="left:calc((100% - ${LAB})*${f} + 10px)">${txt}</span>`;
/* the energy boundary of a row, as the short phrase shown under its name */
const BKEY = {'Electricity at the vehicle':'boundary.electricity','Electricity at the vessel':'boundary.electricity','Electricity at the aircraft':'boundary.electricity','Electricity at the drone':'boundary.electricity',
  'Metabolic (food energy)':'boundary.food','Final energy':'boundary.final','Fuel energy':'boundary.fuel','Fuel':'boundary.fuel','Operating energy':'boundary.operating','Total electrical':'boundary.totalElectrical',
  'Metabolic, estimated from breathing rate':'boundary.breathing','Metabolic, measured oxygen use':'boundary.oxygen','Metabolic, net (above standing)':'boundary.netStanding','Metabolic, gross':'boundary.gross'};
const boundaryOf = b => b === 'Metabolic' ? '' : BKEY[b] ? t(BKEY[b]) : (MISS.add('boundary:' + b), b.toLowerCase());
/* the tag that flags how firm a row is: derived, claim, model, scenario */
const flagOf = d => { const k=[], x=(d.detail||'');
  if(d.id==='L01') k.push('flag.derived');
  if(d.id==='V01') k.push('flag.physicsLimit');
  if(d.grade==='C') k.push('flag.claim');
  if(/allometric/i.test(x)) k.push('flag.modelLine'); else if(/scenario|design model/i.test(x)) k.push('flag.scenario');
  return k.map(x => t(x)); };

/* ================= summary — the lift figure (a COT of 0.1 lifts 1 kg by 10 cm per metre) ================= */
function renderLift(){
  // on phones the drawing is laid out at the container's own width (1 unit = 1 px), so text keeps its CSS size; every other name sits on a second line
  const box = $('lift').clientWidth, narrow = box < 560, w = narrow ? Math.max(260, Math.round(box)) : 760, h = narrow ? 420 : 410;
  const m = {l:narrow?40:52, r:8, t:36, b:narrow?92:62}, y0 = h-m.b;
  const I = [['L01','short.whale'],['V01','short.ecoCar'],['F01','short.ship'],['L02','short.eel'],['H04','short.cyclist'],['H01','short.walker'],['B04','short.asimo'],['F07','short.drone']];
  const Y = cm => y0 - (log10(cm)-log10(.1))/(log10(3000)-log10(.1))*(y0-m.t);
  const hf = cm => cm<10 ? dec(cm.toFixed(1))+' cm' : cm<100 ? Math.round(cm)+' cm' : dec(cm/100<10 ? (cm/100).toFixed(1) : Math.round(cm/100))+' m';
  const cw = (w-m.l-m.r)/I.length, bw = narrow ? 28 : 36, bh = narrow ? 19 : 22;
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(tp('chart.lift.aria'))} ${I.map(([id])=>`${esc(tp('mover.'+id))} ${hf(LAD[id].cot*100)}`).join('; ')}">`;
  s += '<g class="lf__ax">'+[[.1,'1 mm'],[1,'1 cm'],[10,'10 cm'],[100,'1 m'],[1000,'10 m']].map(([v,l])=>`<line x1="${m.l}" x2="${w-m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${m.l-8}" y="${Y(v)+4}" text-anchor="end">${l}</text>`).join('')+'</g>';
  I.forEach(([id,nk],i) => {
    const d = LAD[id], c = GRP[d.group][0], own = d.basis.startsWith('own'), cx = m.l+cw*(i+.5), yv = Y(d.cot*100);
    s += `<line class="lf__stem" style="--i:${i}" x1="${cx}" x2="${cx}" y1="${y0}" y2="${yv+bh/2}" stroke="${c}"/>`;
    s += `<g class="lf__w" style="--i:${i};--dy:${y0-yv}px"><rect x="${cx-bw/2}" y="${yv-bh/2}" width="${bw}" height="${bh}" rx="4" fill="${own?c:'var(--bg-card)'}" stroke="${c}"/>`+
         `<text x="${cx}" y="${yv+4}" fill="${own?'var(--ink)':c}">1 kg</text><text class="lf__v" x="${cx}" y="${yv-bh/2-7}">${hf(d.cot*100)}</text></g>`;
    const st = narrow && i % 2 ? 34 : 0;
    s += `<circle cx="${cx}" cy="${y0}" r="3.5" fill="${c}"/><text class="lf__n" x="${cx}" y="${y0+22+st}" fill="${c}">${t(nk)}</text><text class="lf__c" x="${cx}" y="${y0+39+st}">${narrow?'':t('abbr.cot')+' '}${cotf(d.cot)}</text>`;
  });
  $('lift').innerHTML = s+'</svg>';
}

/* ================= ch01 — the equation (V09) ================= */
function renderCot(){
  const IC = {bolt:'<svg viewBox="0 0 24 24"><path d="M13 2 5 13.5h6L10 22l9-12h-6.5Z"/></svg>', kg:'<svg viewBox="0 0 24 24"><path d="M7 8h10l3 12H4Z"/><circle cx="12" cy="5" r="2"/></svg>', d:'<svg viewBox="0 0 24 24"><path d="M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/></svg>'};
  const E = 3.6e6, km = 538, m = DATA.formula.passenger_kg, g = dec(DATA.formula.g.toFixed(2)), res = E/(m*DATA.formula.g*km*1000);
  $('cot').innerHTML =
    `<div class="cot__eq" role="img" aria-label="${esc(tp('chart.equation.aria'))}"><span class="cot__k">${t('abbr.cot')}</span><span class="cot__op">=</span><span class="cot__frac"><span class="cot__num"><i>${IC.bolt}</i>E</span><span class="cot__den"><i>${IC.kg}</i>m × g<span style="color:var(--txt-muted)">×</span><i>${IC.d}</i>d</span></span></div>`+
    `<div class="cot__ex"><h4>${t('chart.equation.exampleTitle')}</h4><p>${t('chart.equation.example', {m})}</p><div class="cot__calc"><span class="fr"><span>${fmt(E)} J</span><span>${m} kg × ${g} m/s² × ${fmt(km*1000)} m</span></span><span class="eq">=</span><span class="res">${cotf(res)}</span></div></div>`+
    `<ul class="cot__terms"><li><b>E</b>${t('chart.equation.termE')}</li><li><b>m</b>${t('chart.equation.termM')}</li><li><b>g</b>${t('chart.equation.termG', {g})}</li><li><b>d</b>${t('chart.equation.termD')}</li></ul>`;
}

/* ================= V02 — every mover on one log axis ================= */
function renderLadder(){
  const L = DATA.ladder, X = v => (log10(v)+3)/5, T = [.001,.01,.1,1,10,100];
  let h = `<div class="rows lr--wide lr--ladder" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tp('chart.ladder.aria', {n:L.length}))} ${L.map(d=>`${esc(tp('mover.'+d.id))} ${cotf(d.cot)}`).join('; ')}">`;
  L.forEach((d,i) => {
    const c = GRP[d.group][0], own = d.basis.startsWith('own'), x = X(d.cot);
    let bar = d.high > d.low ? `<span class="lr__rng" style="left:${at(X(d.low))};width:calc((100% - ${LAB})*${X(d.high)-X(d.low)});background:${c}"></span>` : '';
    bar += `<span class="lr__dot" style="--i:${i};left:${at(x)};border-color:${c};background:${own?c:'var(--bg-card)'}"></span>`;
    bar += valLabel(Math.max(X(d.high),x), cotf(d.cot));
    h += lrow(t('mover.'+d.id), flagOf(d).join(' · '), bar);
  });
  $('v02').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
  $('v02-legend').innerHTML = Object.values(GRP).map(([c,k]) => `<span><i style="background:${c}"></i>${t(k)}</span>`).join('')+
    `<span><i style="background:var(--txt)"></i>${t('chart.ladder.legendFilled')}</span><span><i class="ring"></i>${t('chart.ladder.legendHollow')}</span>`;
  $('v02-nd').innerHTML = ndNote(`<b>${t('chart.nd.none')}</b> ${DATA.ladder_nd.map(n => t('mover.'+BYNAME[n])).join(', ')}. ${t('chart.nd.meaning')}`);
}

/* ================= V04 — the living podium ================= */
function renderPodium(){
  const A = byId(DATA.living), Hm = byId(DATA.human);
  const R = [A.L01, A.L02, A.L03, A.L04, Hm.H02, Hm.H01, Hm.H03].sort((a,b) => a.cot-b.cot);
  const X = v => (log10(v)+3)/3, T = [.001,.01,.1,1];
  const NAME = {L01:'chart.podium.name.L01', L02:'chart.podium.name.L02', L03:'chart.podium.name.L03', L04:'chart.podium.name.L04', H02:'chart.podium.name.H02', H01:'chart.podium.name.H01', H03:'chart.podium.name.H03'};
  const SUB = d => d.id==='L01' ? t('flag.derived') : boundaryOf(d.boundary||'');
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tp('chart.podium.aria'))} ${R.map(d=>`${esc(tp(NAME[d.id]))} ${cotf(d.cot)}`).join('; ')}">`;
  R.forEach((d,i) => {
    const c = d.group==='Human body' ? 'var(--g-human)' : 'var(--g-live)', x = X(d.cot);
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:${c}"></span>`;
    if(d.high > d.low) bar += whisker(d.low, d.high, X);
    bar += valLabel(Math.max(X(d.high),x), cotf(d.cot));
    h += lrow(t(NAME[d.id]), SUB(d), bar);
  });
  $('v04').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
  $('v04-nd').innerHTML = ndNote(t('chart.podium.jellyfish'));
}

/* ================= V03 — size line, log-log ================= */
function renderSize(){
  const box = $('v03').clientWidth, narrow = box < 560, S = DATA.size, w = narrow ? Math.max(260, Math.round(box)) : 760, h = narrow ? Math.round(w * 1.05) : 420, m = {t:22, r:narrow?46:74, b:54, l:52};   // phones: 1 unit = 1 px
  const x = d3.scaleLog().domain([.01,10000]).range([m.l, w-m.r]), y = d3.scaleLog().domain([.05,5]).range([h-m.b, m.t]);
  const XT = [[.01,'10 g'],[.1,'100 g'],[1,'1 kg'],[10,'10 kg'],[100,'100 kg'],[1000,'1 t'],[10000,'10 t']].filter((_,i) => !narrow || i%2===0);
  const YT = [.05,.1,.2,.5,1,2,5];
  const line = d3.line().x(d => x(d.kg)).y(d => y(d.cot)).curve(d3.curveMonotoneX)(S);
  const L = S.filter(d => d.label), mo = L.find(d => d.label==='Mouse'), el = L.find(d => d.label==='Elephant');
  const KG = {Mouse:'20 g',Dog:'20 kg',Human:'70 kg',Horse:'500 kg',Elephant:fmt(4000)+' kg'};
  const SIZEK = {Mouse:'size.mouse', Dog:'size.dog', Human:'size.human', Horse:'size.horse', Elephant:'size.elephant'};
  let s = `<svg viewBox="0 0 ${w} ${h}" class="sc-svg" role="img" aria-label="${esc(tp('chart.size.aria'))} ${L.map(d=>`${esc(tp(SIZEK[d.label]))} (${KG[d.label]}) ${cotf(d.cot)}`).join('; ')}">`;
  s += '<g class="grid">'+XT.map(([v]) => `<line x1="${x(v)}" x2="${x(v)}" y1="${m.t}" y2="${h-m.b}"/>`).join('')+YT.map(v => `<line x1="${m.l}" x2="${w-m.r}" y1="${y(v)}" y2="${y(v)}"/>`).join('')+'</g>';
  s += '<g class="ax">'+XT.map(([v,l]) => `<text x="${x(v)}" y="${h-m.b+18}" text-anchor="middle">${l}</text>`).join('')+YT.map(v => `<text x="${m.l-8}" y="${y(v)+4}" text-anchor="end">${dec(v)}</text>`).join('')+'</g>';
  s += `<text class="axt" x="${w-m.r}" y="${h-10}" text-anchor="end">${t('chart.size.axisX')}</text>`;
  s += `<text class="axt" x="${m.l-40}" y="${m.t-4}" text-anchor="start" transform="rotate(-90 ${m.l-40} ${m.t-4})" dx="-${h-m.b-m.t}">${t('chart.size.axisY')}</text>`;
  s += `<line class="gl" x1="${x(mo.kg)}" x2="${w-m.r+10}" y1="${y(mo.cot)}" y2="${y(mo.cot)}"/><line class="gl" x1="${x(el.kg)}" x2="${w-m.r+10}" y1="${y(el.cot)}" y2="${y(el.cot)}"/>`;
  const bx = w-m.r+16;
  s += `<path class="brk" d="M${bx-5} ${y(mo.cot)}H${bx}V${y(el.cot)}H${bx-5}"/><text class="brkt" x="${bx+7}" y="${(y(mo.cot)+y(el.cot))/2+5}">${Math.round(DATA.size_ratio)}×</text>`;
  s += `<path class="line" d="${line}"/>`;
  L.forEach(d => { const last = d.label==='Elephant', left = narrow && !last && d.label!=='Mouse';   // phones: labels sit to the left of the line, clear of the 47x bracket
    const dx = last ? -8 : left ? -12 : 10, dy = last ? 24 : left ? 4 : -10;
    s += `<circle cx="${x(d.kg)}" cy="${y(d.cot)}" r="6.5" fill="var(--g-live)" stroke="#292A4E" stroke-width="1.5"/><text class="lbl" x="${x(d.kg)+dx}" y="${y(d.cot)+dy}" text-anchor="${last||left?'end':'start'}">${t(SIZEK[d.label])} ${narrow?'':KG[d.label]+' · '}${cotf(d.cot)}</text>`; });
  $('v03').innerHTML = s+'</svg>';
}

/* ================= V05 — walk, run, cycle: two panels, same order ================= */
function renderHuman(){
  const H = byId(DATA.human), P = byId(DATA.people), W = 54;
  const R = [{n:'chart.human.walkFast', s:'chart.human.walkFastSub', d:H.H01, w:P.V04}, {n:'chart.human.walkNet', s:'chart.human.walkNetSub', d:H.H02}, {n:'chart.human.running', s:'chart.human.runningSub', d:H.H03},
             {n:'chart.human.cycling', s:'chart.human.cyclingSub', d:H.H04, w:{wh:H.H04.practical, wh_low:H.H04.practical, wh_high:H.H04.practical}}];
  const mxC = .5, mxW = 90;
  const cell = (v, mx, bg, txt, i, lo, hi) => `<div class="pan__cell"><span class="row__fill" style="--i:${i};width:calc((100% - ${W}px)*${v/mx});background:${bg}"></span>`+
    (hi > lo ? `<span class="pan__wh" style="left:calc((100% - ${W}px)*${lo/mx});width:calc((100% - ${W}px)*${(hi-lo)/mx})"></span>` : '')+
    `<span class="row__v" style="left:calc((100% - ${W}px)*${Math.max(v,hi||0)/mx} + 8px)">${txt}</span></div>`;
  let h = `<div class="pan pan--human" role="img" aria-label="${R.map(r=>`${esc(tp(r.n))}: ${esc(tp('abbr.cot'))} ${cotf(r.d.cot)}, ${r.w?whf(r.w.wh)+' '+esc(tp('chart.human.ariaFood')):esc(tp('chart.human.ariaNd'))}`).join('; ')}">`;
  h += `<div class="pan__head"><span></span><div class="pan__h pan__h--ev">${t('chart.human.colCot')}<small>${t('chart.human.colCotSub', {max:dec(mxC)})}</small></div><div class="pan__h pan__h--ice">${t('chart.human.colWh')}<small>${t('chart.human.colWhSub', {max:mxW})}</small></div></div>`;
  R.forEach((r,i) => {
    h += `<div class="pan__row"><div class="row__m"><span class="row__mt">${t(r.n)}<small>${t(r.s)}</small></span></div>`+
      cell(r.d.cot, mxC, 'var(--g-human)', cotf(r.d.cot), i, r.d.low, r.d.high)+
      (r.w ? cell(r.w.wh, mxW, 'var(--hatch-people)', whf(r.w.wh), i, r.w.wh_low, r.w.wh_high) : `<div class="pan__cell"><span class="pan__nd">${t('abbr.nd')}</span></div>`)+'</div>';
  });
  $('v05').innerHTML = h+'</div>';
}

/* ================= V06 — robots against biology, log axis with two reference lines ================= */
function renderRobots(){
  const R = DATA.robots, X = v => (log10(v)+1)/(log10(30)+1), T = [.1,.3,1,3,10,30];
  const bots = R.filter(d => d.id.startsWith('B')).sort((a,b) => (a.cot??1e9)-(b.cot??1e9)), hw = R.find(d => d.id==='H02'), ho = R.find(d => d.id==='L04');
  const gl = grid([...T.map(v => [X(v)]), [X(ho.cot),'var(--g-live)',2], [X(hw.cot),'var(--g-human)',2]]);
  let h = `<div class="rows lr--wide" style="--grid:${gl}" role="img" aria-label="${esc(tp('chart.robots.aria'))} ${bots.map(d=>`${esc(tp('mover.'+d.id))} ${d.cot==null?esc(tp('abbr.nd')):cotf(d.cot)}`).join('; ')}. ${esc(tp('chart.robots.ariaRefs', {h:cotf(hw.cot), o:cotf(ho.cot)}))}">`;
  h += `<div class="rows__axis"><span></span><div class="refl" style="margin-right:${LAB}"><span style="left:${X(ho.cot)*100}%;transform:translateX(-100%);padding-right:7px;color:var(--g-live);text-align:right">${t('chart.robots.refHorse')}<br>${cotf(ho.cot)}</span><span style="left:${X(hw.cot)*100}%;padding-left:7px;color:var(--g-human)">${t('chart.robots.refHuman')}<br>${cotf(hw.cot)}</span></div></div>`;
  bots.forEach((d,i) => {
    let bar;
    if(d.cot == null) bar = `<span class="row__v lr__v" style="left:calc((100% - ${LAB})*${X(.32)});color:var(--txt-muted);font-weight:500"><i class="ndo"></i>${t(innerWidth<640 ? 'chart.robots.noData' : 'chart.robots.noDataLong')}</span>`;
    else bar = `<span class="lr__dot" style="--i:${i};left:${at(X(d.cot))};border-color:var(--g-robot);background:var(--g-robot)"></span>`+valLabel(X(d.cot), cotf(d.cot));
    h += lrow(t('mover.'+d.id), d.cot==null ? t('chart.robots.g1Source') : boundaryOf(d.boundary), bar, d.cot==null ? 'row--nd' : '');
  });
  $('v06').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
}

/* ================= V07 — moving people: Wh per person-km, linear, with whiskers ================= */
function renderPeople(){
  const P = DATA.people, MX = 900, X = v => v/MX, T = [0,300,600,900];
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tp('chart.people.aria'))} ${P.map(d=>`${esc(tp('mover.'+d.id))} ${whf(d.wh)} Wh`).join('; ')}">`;
  P.forEach((d,i) => {
    const food = /Metabolic/.test(d.boundary), x = X(d.wh), hi = Math.max(X(d.wh_high), x);
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:${food?'var(--hatch-people)':'var(--g-people)'}"></span>`;
    if(d.wh_high > d.wh_low*1.001) bar += whisker(d.wh_low, d.wh_high, X);
    bar += valLabel(hi, whf(d.wh));
    const sub = [boundaryOf(d.boundary), t('abbr.cot')+' '+cotf(d.cot), ...flagOf(d)].join(' · ');
    h += lrow(t('mover.'+d.id), sub, bar);
  });
  $('v07').innerHTML = h+'</div>'+axis(T, X, v => fmt(v)+(v===900?' Wh':''));
}

/* ================= V08 — moving goods: Wh per tonne-km, log axis ================= */
function renderGoods(){
  const G = DATA.goods, X = v => (log10(v)-1)/4, T = [10,100,1000,1e4,1e5];
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tp('chart.goods.aria'))} ${G.map(d=>`${esc(tp('mover.'+d.id))} ${fmt(d.wh)} Wh`).join('; ')}">`;
  G.forEach((d,i) => {
    const x = X(d.wh), hi = Math.max(X(d.wh_high), x), tight = d.wh_high/d.wh_low < 1.0001;
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:var(--g-goods)"></span>`;
    if(!tight) bar += whisker(d.wh_low, d.wh_high, X);
    bar += valLabel(hi, fmt(d.wh));
    const sub = [boundaryOf(d.boundary), t('abbr.cot')+' '+cotf(d.cot), ...flagOf(d)].join(' · ');
    h += lrow(t('mover.'+d.id), sub, bar);
  });
  $('v08').innerHTML = h+'</div>'+axis(T, X, v => v>=1000 ? (v/1000)+'k' : v);
  const w = DATA.goods_whole[0];
  $('v08-nd').innerHTML = ndNote(`<b>${t('chart.goods.notCharted')}</b> ${t('mover.'+w.id)}. ${t('chart.goods.wholeVehicle', {c:cotf(w.cot)})}`);
}

/* ================= render, language switch ================= */
function renderAll(){
  renderLift(); renderCot(); renderLadder(); renderPodium(); renderSize(); renderHuman(); renderRobots(); renderPeople(); renderGoods();
}
function applyText(){
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.dataset.i18n;
    el.innerHTML = el.dataset.i18nFmt === 'lead' ? lead(tp(k)) : t(k, el.dataset.i18nArgs ? JSON.parse(el.dataset.i18nArgs) : undefined);
  });
  document.querySelectorAll('[data-i18n-attr]').forEach(el => el.dataset.i18nAttr.split(';').forEach(p => { const [a, k] = p.split(':'); el.setAttribute(a, tp(k)); }));
  document.querySelectorAll('[data-num]').forEach(el => { el.textContent = dec(el.dataset.num); });
}
function setLang(l, remember = true){
  LANG = l === 'es' ? 'es' : 'en';
  document.documentElement.lang = LANG;
  document.title = tp('meta.title');
  const md = document.querySelector('meta[name="description"]');
  if(md) md.content = tp('meta.description');
  applyText();
  renderAll();
  document.querySelectorAll('.lang__b').forEach(b => { const on = b.dataset.lang === LANG; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
  if(remember){
    try{ localStorage.setItem('lang', LANG); }catch(e){}
    try{ const u = new URL(location.href); if(LANG === 'es') u.searchParams.set('lang','es'); else u.searchParams.delete('lang'); history.replaceState(null, '', u); }catch(e){}
  }
}

/* ================= boot ================= */
let startLang = 'en';
try{ const q = new URLSearchParams(location.search).get('lang'); const s = localStorage.getItem('lang'); startLang = (q === 'es' || q === 'en') ? q : (s === 'es' ? 'es' : 'en'); }catch(e){}
document.querySelectorAll('.lang__b').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang)));
setLang(startLang, false);
let boxNow = $('v03').clientWidth, rz;
window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(() => { const n = $('v03').clientWidth; if(n !== boxNow){ boxNow = n; renderSize(); renderLift(); renderRobots(); } }, 120); });

const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduce || !('IntersectionObserver' in window)){ document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible')); }
else{
  const obs = new IntersectionObserver(e => { e.forEach(x => { if(x.isIntersecting){ x.target.classList.add('visible'); obs.unobserve(x.target); } }); }, {threshold:0.06});
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

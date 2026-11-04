const DATA = /*__DATA__*/null;
const I18N = /*__I18N__*/null;   // {p: {docx block key: Spanish html}, ui: {English text: Spanish text}}

/* ================= language (EN | ES) ================= */
let LANG = 'en';
const MISS = window.__i18nMiss = new Set();   // English texts that have no Spanish yet (checked while testing)
const tr = s => { if(LANG !== 'es') return s; if(I18N.ui[s] !== undefined) return I18N.ui[s]; if(/[A-Za-z]{3}/.test(s)) MISS.add(s); return s; };
const trf = (s, o) => Object.entries(o).reduce((a, [k, v]) => a.split(`{${k}}`).join(v), tr(s));   // tr + {placeholders}
const dec = s => LANG === 'es' ? String(s).replace('.', ',') : String(s);                         // decimal comma in Spanish

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const $ = id => document.getElementById(id);
const fmt = v => Math.round(v).toLocaleString(LANG === 'es' ? 'es-ES' : 'en-US');
const cotf = v => dec(v<.01 ? v.toFixed(4) : v<1 ? v.toFixed(3) : v<10 ? v.toFixed(2) : v.toFixed(1));   // 0.0031 · 0.060 · 0.172 · 2.27 · 15.0
const whf = v => v<10 ? dec(v.toFixed(1)) : fmt(v);
const ndNote = (text) => `<span class="nd-note">${text}</span>`;
const LAB = 'var(--lab)';   // space reserved at the end of a bar row for its value label (CSS: 92px, 70px on phones)
const at = f => `calc((100% - ${LAB})*${f})`;
const log10 = Math.log10;

const GRP = {'Living beings':'var(--g-live)','Human body':'var(--g-human)','Robots':'var(--g-robot)','Moving people':'var(--g-people)','Moving goods':'var(--g-goods)'};
const byId = L => Object.fromEntries(L.map(d => [d.id, d]));
const LAD = byId(DATA.ladder);

/* gridlines behind a row of bars: [fraction, colour, width] -> one CSS background (read by .lr__bar) */
const grid = (list) => list.map(([f,c='var(--gl)',w=1]) => `linear-gradient(${c},${c}) calc((100% - var(--lab))*${f}) 0/${w}px 100% no-repeat`).join(',');
const lrow = (name, sub, bar, cls='') => `<div class="row lr ${cls}"><div class="row__m"><span class="row__mt">${name}${sub?`<small>${sub}</small>`:''}</span></div><div class="row__bar lr__bar">${bar}</div></div>`;
const axis = (vals, X, f) => `<div class="rows__axis"><span></span><div class="rows__ticks" style="margin-right:${LAB}">${vals.map(v => `<span style="left:${X(v)*100}%">${f(v)}</span>`).join('')}</div></div>`;
const whisker = (lo, hi, X) => `<span class="lr__wh" style="left:${at(X(lo))};width:calc((100% - ${LAB})*${X(hi)-X(lo)})"></span>`;
const valLabel = (f, txt) => `<span class="row__v lr__v" style="left:calc((100% - ${LAB})*${f} + 10px)">${txt}</span>`;
const SHORT_B = {'Electricity at the vehicle':'electricity','Electricity at the vessel':'electricity','Electricity at the aircraft':'electricity','Electricity at the drone':'electricity',
  'Metabolic (food energy)':'food energy','Final energy':'final energy','Fuel energy':'fuel','Operating energy':'operating energy'};
/* the tag that flags how firm a row is: derived, claim, model, scenario */
const flagOf = d => { const t=[], x=(d.detail||'');
  if(d.id==='L01') t.push('derived from breathing');
  if(d.id==='V01') t.push('physics limit');
  if(d.grade==='C') t.push('manufacturer claim');
  if(/allometric/i.test(x)) t.push('model line'); else if(/scenario|design model/i.test(x)) t.push('scenario / model');
  return t.map(s => tr(s)); };

/* ================= summary — the lift figure (a COT of 0.1 lifts 1 kg by 10 cm per metre) ================= */
function renderLift(){
  const narrow = $('lift').clientWidth < 560, w = narrow ? 400 : 760, h = narrow ? 390 : 410;
  const m = {l:narrow?42:52, r:8, t:36, b:62}, y0 = h-m.b;
  const I = [['L01','Whale'],['V01','Eco car'],['F01','Ship'],['L02','Eel'],['H04','Cyclist'],['H01','Walker'],['B04','ASIMO'],['F07','Drone']];
  const Y = cm => y0 - (log10(cm)-log10(.1))/(log10(3000)-log10(.1))*(y0-m.t);
  const hf = cm => cm<10 ? dec(cm.toFixed(1))+' cm' : cm<100 ? Math.round(cm)+' cm' : dec(cm/100<10 ? (cm/100).toFixed(1) : Math.round(cm/100))+' m';
  const cw = (w-m.l-m.r)/I.length, bw = narrow ? 28 : 36, bh = narrow ? 19 : 22;
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(tr('Height by which each mover lifts 1 kg per metre travelled:'))} ${I.map(([id,n])=>`${esc(tr(LAD[id].mover))} ${hf(LAD[id].cot*100)}`).join('; ')}">`;
  s += '<g class="lf__ax">'+[[.1,'1 mm'],[1,'1 cm'],[10,'10 cm'],[100,'1 m'],[1000,'10 m']].map(([v,t])=>`<line x1="${m.l}" x2="${w-m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${m.l-8}" y="${Y(v)+4}" text-anchor="end">${t}</text>`).join('')+'</g>';
  I.forEach(([id,n],i) => {
    const d = LAD[id], c = GRP[d.group], own = d.basis.startsWith('own'), cx = m.l+cw*(i+.5), yv = Y(d.cot*100);
    s += `<line class="lf__stem" style="--i:${i}" x1="${cx}" x2="${cx}" y1="${y0}" y2="${yv+bh/2}" stroke="${c}"/>`;
    s += `<g class="lf__w" style="--i:${i};--dy:${y0-yv}px"><rect x="${cx-bw/2}" y="${yv-bh/2}" width="${bw}" height="${bh}" rx="4" fill="${own?c:'var(--bg-card)'}" stroke="${c}"/>`+
         `<text x="${cx}" y="${yv+4}" fill="${own?'var(--ink)':c}">1 kg</text><text class="lf__v" x="${cx}" y="${yv-bh/2-7}">${hf(d.cot*100)}</text></g>`;
    s += `<circle cx="${cx}" cy="${y0}" r="3.5" fill="${c}"/><text class="lf__n" x="${cx}" y="${y0+22}" fill="${c}">${esc(tr(n))}</text><text class="lf__c" x="${cx}" y="${y0+39}">${narrow?'':'COT '}${cotf(d.cot)}</text>`;
  });
  $('lift').innerHTML = s+'</svg>';
}

/* ================= ch01 — the equation (V09) ================= */
function renderCot(){
  const IC = {bolt:'<svg viewBox="0 0 24 24"><path d="M13 2 5 13.5h6L10 22l9-12h-6.5Z"/></svg>', kg:'<svg viewBox="0 0 24 24"><path d="M7 8h10l3 12H4Z"/><circle cx="12" cy="5" r="2"/></svg>', d:'<svg viewBox="0 0 24 24"><path d="M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/></svg>'};
  const E = 3.6e6, km = 538, m = DATA.formula.passenger_kg, g = dec(DATA.formula.g.toFixed(2)), res = E/(m*DATA.formula.g*km*1000);
  $('cot').innerHTML =
    `<div class="cot__eq" role="img" aria-label="${esc(tr('COT equals E divided by m times g times d'))}"><span class="cot__k">COT</span><span class="cot__op">=</span><span class="cot__frac"><span class="cot__num"><i>${IC.bolt}</i>E</span><span class="cot__den"><i>${IC.kg}</i>m × g<span style="color:var(--txt-muted)">×</span><i>${IC.d}</i>d</span></span></div>`+
    `<div class="cot__ex"><h4>${tr('Worked example')}</h4><p>${trf('Shell Eco-marathon prototype: 1 kWh (3.6 million J) for 538 km, one occupant counted as {m} kg.', {m})}</p><div class="cot__calc"><span class="fr"><span>${fmt(E)} J</span><span>${m} kg × ${g} m/s² × ${fmt(km*1000)} m</span></span><span class="eq">=</span><span class="res">${cotf(res)}</span></div></div>`+
    `<ul class="cot__terms"><li><b>E</b>${tr('Energy put in, in joules: food, electricity or fuel.')}</li><li><b>m</b>${tr('The mass moved, in kg: the mover itself, or its passenger or cargo.')}</li><li><b>g</b>${trf('Gravity, {g} m/s².', {g})}</li><li><b>d</b>${tr('The distance travelled, in metres.')}</li></ul>`;
}

/* ================= V02 — every mover on one log axis ================= */
function renderLadder(){
  const L = DATA.ladder, X = v => (log10(v)+3)/5, T = [.001,.01,.1,1,10,100];
  let h = `<div class="rows lr--wide lr--ladder" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(trf('Cost of transport of {n} movers on a log scale:', {n:L.length}))} ${L.map(d=>`${esc(tr(d.mover))} ${cotf(d.cot)}`).join('; ')}">`;
  L.forEach((d,i) => {
    const c = GRP[d.group], own = d.basis.startsWith('own'), x = X(d.cot);
    let bar = d.high > d.low ? `<span class="lr__rng" style="left:${at(X(d.low))};width:calc((100% - ${LAB})*${X(d.high)-X(d.low)});background:${c}"></span>` : '';
    bar += `<span class="lr__dot" style="--i:${i};left:${at(x)};border-color:${c};background:${own?c:'var(--bg-card)'}"></span>`;
    bar += valLabel(Math.max(X(d.high),x), cotf(d.cot));
    h += lrow(esc(tr(d.mover)), esc(flagOf(d).join(' · ')), bar);
  });
  $('v02').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
  $('v02-legend').innerHTML = Object.entries(GRP).map(([k,c]) => `<span><i style="background:${c}"></i>${esc(tr(k))}</span>`).join('')+
    `<span><i style="background:var(--txt)"></i>${tr('Filled: per kg of itself')}</span><span><i class="ring"></i>${tr('Hollow: per kg of passenger or cargo')}</span>`;
  $('v02-nd').innerHTML = ndNote(`<b>${tr('No comparable number (ND):')}</b> ${DATA.ladder_nd.map(n => esc(tr(n))).join(', ')}. ${tr('ND means no defensible figure was found; it never means zero.')}`);
}

/* ================= V04 — the living podium ================= */
function renderPodium(){
  const A = byId(DATA.living), Hm = byId(DATA.human);
  const R = [A.L01, A.L02, A.L03, A.L04, Hm.H02, Hm.H01, Hm.H03].sort((a,b) => a.cot-b.cot);
  const X = v => (log10(v)+3)/3, T = [.001,.01,.1,1];
  const NAME = {L01:'Humpback whale', L02:'European eel', L03:'Beluga whale', L04:'Horse, trotting', H02:'Human walking, net', H01:'Human walking, fast', H03:'Human running'};
  const SUB = d => d.id==='L01' ? 'derived from breathing' : (d.boundary||'').replace(/^Metabolic,? ?/,'');
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tr('Cost of transport of living beings:'))} ${R.map(d=>`${esc(tr(NAME[d.id]))} ${cotf(d.cot)}`).join('; ')}">`;
  R.forEach((d,i) => {
    const c = d.group==='Human body' ? 'var(--g-human)' : 'var(--g-live)', x = X(d.cot);
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:${c}"></span>`;
    if(d.high > d.low) bar += whisker(d.low, d.high, X);
    bar += valLabel(Math.max(X(d.high),x), cotf(d.cot));
    h += lrow(esc(tr(NAME[d.id])), esc(tr(SUB(d))), bar);
  });
  $('v04').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
  $('v04-nd').innerHTML = ndNote(tr('<b>Not charted (ND): moon jellyfish.</b> It is reported as the cheapest swimmer in its comparison, but the value appears only in a chart, and its body is mostly water, which flatters a per-kg metric.'));
}

/* ================= V03 — size line, log-log ================= */
function renderSize(){
  const narrow = $('v03').clientWidth < 560, S = DATA.size, w = narrow ? 400 : 760, h = narrow ? 360 : 420, m = {t:22, r:narrow?46:74, b:54, l:52};
  const x = d3.scaleLog().domain([.01,10000]).range([m.l, w-m.r]), y = d3.scaleLog().domain([.05,5]).range([h-m.b, m.t]);
  const XT = [[.01,'10 g'],[.1,'100 g'],[1,'1 kg'],[10,'10 kg'],[100,'100 kg'],[1000,'1 t'],[10000,'10 t']].filter((_,i) => !narrow || i%2===0);
  const YT = [.05,.1,.2,.5,1,2,5];
  const line = d3.line().x(d => x(d.kg)).y(d => y(d.cot)).curve(d3.curveMonotoneX)(S);
  const L = S.filter(d => d.label), mo = L.find(d => d.label==='Mouse'), el = L.find(d => d.label==='Elephant');
  const KG = {Mouse:'20 g',Dog:'20 kg',Human:'70 kg',Horse:'500 kg',Elephant:fmt(4000)+' kg'};
  let s = `<svg viewBox="0 0 ${w} ${h}" class="sc-svg" role="img" aria-label="${esc(tr('Net cost of running against body mass, model line:'))} ${L.map(d=>`${esc(tr(d.label))} (${KG[d.label]}) ${cotf(d.cot)}`).join('; ')}">`;
  s += '<g class="grid">'+XT.map(([v]) => `<line x1="${x(v)}" x2="${x(v)}" y1="${m.t}" y2="${h-m.b}"/>`).join('')+YT.map(v => `<line x1="${m.l}" x2="${w-m.r}" y1="${y(v)}" y2="${y(v)}"/>`).join('')+'</g>';
  s += '<g class="ax">'+XT.map(([v,t]) => `<text x="${x(v)}" y="${h-m.b+18}" text-anchor="middle">${t}</text>`).join('')+YT.map(v => `<text x="${m.l-8}" y="${y(v)+4}" text-anchor="end">${dec(v)}</text>`).join('')+'</g>';
  s += `<text class="axt" x="${w-m.r}" y="${h-10}" text-anchor="end">${tr('Body mass →')}</text>`;
  s += `<text class="axt" x="${m.l-40}" y="${m.t-4}" text-anchor="start" transform="rotate(-90 ${m.l-40} ${m.t-4})" dx="-${h-m.b-m.t}">${tr('Net cost of running, COT (log) →')}</text>`;
  s += `<line class="gl" x1="${x(mo.kg)}" x2="${w-m.r+10}" y1="${y(mo.cot)}" y2="${y(mo.cot)}"/><line class="gl" x1="${x(el.kg)}" x2="${w-m.r+10}" y1="${y(el.cot)}" y2="${y(el.cot)}"/>`;
  const bx = w-m.r+16;
  s += `<path class="brk" d="M${bx-5} ${y(mo.cot)}H${bx}V${y(el.cot)}H${bx-5}"/><text class="brkt" x="${bx+7}" y="${(y(mo.cot)+y(el.cot))/2+5}">${Math.round(DATA.size_ratio)}×</text>`;
  s += `<path class="line" d="${line}"/>`;
  L.forEach(d => { const last = d.label==='Elephant', dx = last ? -8 : 10, dy = last ? 24 : -10;
    s += `<circle cx="${x(d.kg)}" cy="${y(d.cot)}" r="6.5" fill="var(--g-live)" stroke="#292A4E" stroke-width="1.5"/><text class="lbl" x="${x(d.kg)+dx}" y="${y(d.cot)+dy}" text-anchor="${last?'end':'start'}">${esc(tr(d.label))} ${narrow?'':KG[d.label]+' · '}${cotf(d.cot)}</text>`; });
  $('v03').innerHTML = s+'</svg>';
}

/* ================= V05 — walk, run, cycle: two panels, same order ================= */
function renderHuman(){
  const H = byId(DATA.human), P = byId(DATA.people), W = 54;
  const R = [{n:'Walking, fast', s:'70 kg, ~6 km/h', d:H.H01, w:P.V04}, {n:'Walking, net of standing', s:'190 adults, 1.34 m/s', d:H.H02}, {n:'Running', s:'~1 kcal per kg per km', d:H.H03},
             {n:'Cycling', s:'~16 km/h, 62 kg rider', d:H.H04, w:{wh:H.H04.practical, wh_low:H.H04.practical, wh_high:H.H04.practical}}];
  const mxC = .5, mxW = 90;
  const cell = (v, mx, bg, txt, i, lo, hi) => `<div class="pan__cell"><span class="row__fill" style="--i:${i};width:calc((100% - ${W}px)*${v/mx});background:${bg}"></span>`+
    (hi > lo ? `<span class="pan__wh" style="left:calc((100% - ${W}px)*${lo/mx});width:calc((100% - ${W}px)*${(hi-lo)/mx})"></span>` : '')+
    `<span class="row__v" style="left:calc((100% - ${W}px)*${Math.max(v,hi||0)/mx} + 8px)">${txt}</span></div>`;
  let h = `<div class="pan pan--human" role="img" aria-label="${R.map(r=>`${esc(tr(r.n))}: COT ${cotf(r.d.cot)}, ${r.w?whf(r.w.wh)+' '+esc(tr('Wh per km of food energy')):esc(tr('no Wh per km figure (ND)'))}`).join('; ')}">`;
  h += `<div class="pan__head"><span></span><div class="pan__h pan__h--ev">${tr('Cost of transport')}<small>${tr('per kg of the person')} · ${tr('scale')} 0–${dec(mxC)}</small></div><div class="pan__h pan__h--ice">${tr('Food energy per km, Wh')}<small>${tr('scale')} 0–${mxW}</small></div></div>`;
  R.forEach((r,i) => {
    h += `<div class="pan__row"><div class="row__m"><span class="row__mt">${esc(tr(r.n))}<small>${esc(tr(r.s))}</small></span></div>`+
      cell(r.d.cot, mxC, 'var(--g-human)', cotf(r.d.cot), i, r.d.low, r.d.high)+
      (r.w ? cell(r.w.wh, mxW, 'var(--hatch-people)', whf(r.w.wh), i, r.w.wh_low, r.w.wh_high) : `<div class="pan__cell"><span class="pan__nd">ND</span></div>`)+'</div>';
  });
  $('v05').innerHTML = h+'</div>';
}

/* ================= V06 — robots against biology, log axis with two reference lines ================= */
function renderRobots(){
  const R = DATA.robots, X = v => (log10(v)+1)/(log10(30)+1), T = [.1,.3,1,3,10,30];
  const bots = R.filter(d => d.id.startsWith('B')).sort((a,b) => (a.cot??1e9)-(b.cot??1e9)), hw = R.find(d => d.id==='H02'), ho = R.find(d => d.id==='L04');
  const gl = grid([...T.map(v => [X(v)]), [X(ho.cot),'var(--g-live)',2], [X(hw.cot),'var(--g-human)',2]]);
  let h = `<div class="rows lr--wide" style="--grid:${gl}" role="img" aria-label="${esc(tr('Robot cost of transport:'))} ${bots.map(d=>`${esc(tr(d.mover))} ${d.cot==null?'ND':cotf(d.cot)}`).join('; ')}. ${esc(tr('References:'))} ${esc(tr('human walking'))} ${cotf(hw.cot)}, ${esc(tr('horse trotting'))} ${cotf(ho.cot)}">`;
  h += `<div class="rows__axis"><span></span><div class="refl" style="margin-right:${LAB}"><span style="left:${X(ho.cot)*100}%;transform:translateX(-100%);padding-right:7px;color:var(--g-live);text-align:right">${tr('Horse, trotting')}<br>${cotf(ho.cot)}</span><span style="left:${X(hw.cot)*100}%;padding-left:7px;color:var(--g-human)">${tr('Human walking, net')}<br>${cotf(hw.cot)}</span></div></div>`;
  bots.forEach((d,i) => {
    let bar;
    if(d.cot == null) bar = `<span class="row__v lr__v" style="left:calc((100% - ${LAB})*${X(.32)});color:var(--txt-muted);font-weight:500"><i class="ndo"></i>${tr('no distance data')}${innerWidth<640?'':' · '+tr('cost of transport ND')}</span>`;
    else bar = `<span class="lr__dot" style="--i:${i};left:${at(X(d.cot))};border-color:var(--g-robot);background:var(--g-robot)"></span>`+valLabel(X(d.cot), cotf(d.cot));
    h += lrow(esc(tr(d.mover)), d.cot==null ? esc(tr('Fraunhofer IPA, May 2026')) : esc(tr(d.boundary.toLowerCase())), bar, d.cot==null ? 'row--nd' : '');
  });
  $('v06').innerHTML = h+'</div>'+axis(T, X, v => dec(v));
}

/* ================= V07 — moving people: Wh per person-km, linear, with whiskers ================= */
function renderPeople(){
  const P = DATA.people, MX = 900, X = v => v/MX, T = [0,300,600,900];
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tr('Energy per person-km:'))} ${P.map(d=>`${esc(tr(d.mover))} ${whf(d.wh)} Wh`).join('; ')}">`;
  P.forEach((d,i) => {
    const food = /Metabolic/.test(d.boundary), x = X(d.wh), hi = Math.max(X(d.wh_high), x);
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:${food?'var(--hatch-people)':'var(--g-people)'}"></span>`;
    if(d.wh_high > d.wh_low*1.001) bar += whisker(d.wh_low, d.wh_high, X);
    bar += valLabel(hi, whf(d.wh));
    const sub = [tr(SHORT_B[d.boundary]||d.boundary.toLowerCase()), 'COT '+cotf(d.cot), ...flagOf(d)].join(' · ');
    h += lrow(esc(tr(d.mover)), esc(sub), bar);
  });
  $('v07').innerHTML = h+'</div>'+axis(T, X, v => fmt(v)+(v===900?' Wh':''));
}

/* ================= V08 — moving goods: Wh per tonne-km, log axis ================= */
function renderGoods(){
  const G = DATA.goods, X = v => (log10(v)-1)/4, T = [10,100,1000,1e4,1e5];
  let h = `<div class="rows lr--wide" style="--grid:${grid(T.map(v => [X(v)]))}" role="img" aria-label="${esc(tr('Energy per tonne-km:'))} ${G.map(d=>`${esc(tr(d.mover))} ${fmt(d.wh)} Wh`).join('; ')}">`;
  G.forEach((d,i) => {
    const x = X(d.wh), hi = Math.max(X(d.wh_high), x), tight = d.wh_high/d.wh_low < 1.0001;
    let bar = `<span class="row__fill" style="--i:${i};width:calc((100% - ${LAB})*${x});background:var(--g-goods)"></span>`;
    if(!tight) bar += whisker(d.wh_low, d.wh_high, X);
    bar += valLabel(hi, fmt(d.wh));
    const sub = [tr(SHORT_B[d.boundary]||d.boundary.toLowerCase()), 'COT '+cotf(d.cot), ...flagOf(d)].join(' · ');
    h += lrow(esc(tr(d.mover)), esc(sub), bar);
  });
  $('v08').innerHTML = h+'</div>'+axis(T, X, v => v>=1000 ? (v/1000)+'k' : v);
  const w = DATA.goods_whole[0];
  $('v08-nd').innerHTML = ndNote(`<b>${tr('Not charted (ND):')}</b> ${esc(tr(w.mover))}. ${trf('It is a whole-vehicle value (COT {c} per kg of truck plus load) with no tonne-km figure.', {c:cotf(w.cot)})}`);
}

/* ================= render, language switch ================= */
function renderAll(){
  renderLift(); renderCot(); renderLadder(); renderPodium(); renderSize(); renderHuman(); renderRobots(); renderPeople(); renderGoods();
}
function applyText(){
  document.querySelectorAll('[data-t]').forEach(el => {
    if(el.dataset.en === undefined) el.dataset.en = el.innerHTML;
    el.innerHTML = tr(el.dataset.en);
  });
  document.querySelectorAll('[data-num]').forEach(el => { el.textContent = dec(el.dataset.num); });
  document.querySelectorAll('[data-src]').forEach(el => {
    if(el.dataset.en === undefined) el.dataset.en = el.innerHTML;
    el.innerHTML = (LANG === 'es' && I18N.p[el.dataset.src] !== undefined) ? I18N.p[el.dataset.src] : el.dataset.en;
  });
  document.querySelectorAll('[data-aria]').forEach(el => el.setAttribute('aria-label', tr(el.dataset.aria)));
  document.querySelectorAll('[data-alt]').forEach(el => el.setAttribute('alt', tr(el.dataset.alt)));
}
function setLang(l, remember = true){
  LANG = l === 'es' ? 'es' : 'en';
  document.documentElement.lang = LANG;
  document.title = tr('The Cheapest Kilometre on Earth | Astara Intelligence In Depth #93');
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
let narrowNow = $('v03').clientWidth < 560;
window.addEventListener('resize', () => { const n = $('v03').clientWidth < 560; if(n !== narrowNow){ narrowNow = n; renderSize(); renderLift(); } });

const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduce || !('IntersectionObserver' in window)){ document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible')); }
else{
  const obs = new IntersectionObserver(e => { e.forEach(x => { if(x.isIntersecting){ x.target.classList.add('visible'); obs.unobserve(x.target); } }); }, {threshold:0.06});
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}


:root{--ink-0:#08090b;--ink-1:#0d0e11;--ink-2:#13151a;--ink-3:#1a1d23;--line:#26282f;--line-2:#1d1f25;
--fg-0:#f1ece1;--fg-1:#cfc7b6;--fg-2:#8a8378;--fg-3:#5a554c;--gold:#c9a96a;--gold-2:#a5854a;--gold-3:#6a5530;
--up:#7fb88a;--down:#c97a72;--hot:#d18a5a;--cold:#6a8fa8}
*{box-sizing:border-box}
html,body{margin:0;background:var(--ink-0);color:var(--fg-0);font-family:"Inter","Noto Serif SC",sans-serif;font-size:13px;line-height:1.55}
body{background-image:radial-gradient(1200px 520px at 78% -4%,rgba(201,169,106,.06),transparent 60%),radial-gradient(900px 620px at -8% 42%,rgba(106,143,168,.04),transparent 55%);background-repeat:no-repeat}
.mono{font-family:"JetBrains Mono",ui-monospace,monospace;font-feature-settings:"tnum" 1}
.serif{font-family:"Cormorant Garamond","Noto Serif SC",serif}
.cn{font-family:"Noto Serif SC",serif}
.wrap{max-width:1240px;margin:0 auto;padding:30px 20px 80px}
a{color:var(--gold);text-decoration:none}
h1{font-family:"Noto Serif SC",serif;font-weight:600;font-size:26px;margin:0;letter-spacing:.01em}
.sub{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold);font-size:16px}
.meta{font-family:"JetBrains Mono",monospace;font-size:10.5px;color:var(--fg-3);margin-top:6px}
.tag{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--gold-2);letter-spacing:.28em;margin:30px 0 5px}
.hs{font-family:"Noto Serif SC",serif;font-weight:600;font-size:18px;margin:2px 0 14px}
.blurb{background:var(--ink-1);border:1px solid var(--line-2);border-left:2px solid var(--gold-3);border-radius:3px;padding:14px 18px;margin:14px 0;font-size:13px;color:var(--fg-1);line-height:1.85}
/* master domain grid */
.dgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}
.dcard{position:relative;display:block;background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:16px 17px;transition:border-color .2s,transform .12s,box-shadow .2s;min-height:172px}
.dcard::before{content:"";position:absolute;left:-1px;top:-1px;width:9px;height:9px;border-top:1px solid var(--gold-3);border-left:1px solid var(--gold-3)}
.dcard::after{content:"";position:absolute;right:-1px;bottom:-1px;width:9px;height:9px;border-bottom:1px solid var(--gold-3);border-right:1px solid var(--gold-3)}
.dcard:hover{border-color:var(--gold);transform:translateY(-2px);box-shadow:0 8px 26px rgba(201,169,106,.10)}
.dcard .no{font-family:"JetBrains Mono",monospace;font-size:11px;color:var(--fg-3)}
.dcard .dn{font-family:"Noto Serif SC",serif;font-size:17px;color:var(--fg-0);margin:5px 0 1px}
.dcard .den{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:11px;color:var(--fg-3)}
.dcard .mat{position:absolute;top:15px;right:16px;font-size:10px;font-family:"JetBrains Mono",monospace;padding:2px 7px;border-radius:2px;border:1px solid currentColor}
.dcard .bl{font-size:11.5px;color:var(--fg-2);margin:8px 0 10px;line-height:1.6}
.dcard .lyr{display:flex;gap:5px;margin-top:8px}
.dcard .lyr .seg{flex:1;height:5px;border-radius:2px;background:var(--ink-3);overflow:hidden}
.dcard .lyr .seg i{display:block;height:100%}
.dcard .foot{display:flex;justify-content:space-between;font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--fg-3);margin-top:9px}
/* domain page matrix */
.mx{display:grid;grid-template-columns:118px 1fr;gap:9px}
.lyrow-h{display:flex;flex-direction:column;justify-content:center;padding:8px 6px;border-right:1px solid var(--line-2)}
.lyrow-h .d{font-family:"Noto Serif SC",serif;font-size:14px;color:var(--gold);font-weight:600}
.lyrow-h .e{font-size:9.5px;color:var(--fg-3);margin-top:3px;line-height:1.4}
.lyrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:9px}
.cell{position:relative;background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:11px 12px;cursor:pointer;transition:border-color .2s,transform .12s,box-shadow .2s;min-height:92px}
.cell.gap{border-style:dashed;border-color:var(--gold-3)}
.cell::after{content:"";position:absolute;right:-1px;bottom:-1px;width:8px;height:8px;border-bottom:1px solid var(--gold-3);border-right:1px solid var(--gold-3)}
.cell:hover{border-color:var(--gold);transform:translateY(-2px);box-shadow:0 6px 22px rgba(201,169,106,.09)}
.cell .id{font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--fg-3)}
.cell .nm{font-family:"Noto Serif SC",serif;font-size:13px;color:var(--fg-0);margin:4px 0 7px;line-height:1.4}
.cell .ax{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--fg-2);display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.pill{display:inline-block;padding:1px 6px;border-radius:2px;font-size:9.5px;border:1px solid currentColor}
.gapflag{position:absolute;top:9px;right:11px;font-size:9px;color:var(--down);font-family:"JetBrains Mono",monospace}
.nav{position:sticky;top:0;z-index:50;display:flex;gap:2px;align-items:center;flex-wrap:wrap;background:var(--ink-0);border-bottom:1px solid var(--line-2);margin:0 0 22px;padding:9px max(20px,calc((100vw - 1200px)/2))}
.nav a{font-family:"Noto Serif SC",serif;font-size:11.5px;color:var(--fg-2);padding:4px 9px;border-radius:2px;letter-spacing:.08em}
.nav a:hover,.nav a.on{color:var(--gold);background:var(--ink-2)}
.nav .brand{font-family:"Cormorant Garamond",serif;font-style:italic;color:var(--gold);font-size:15px;margin-right:12px}
.nav .right{margin-left:auto;font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--fg-3)}
#dr{position:fixed;inset:0;z-index:100;display:none;background:rgba(4,5,7,.72)}
#dr.on{display:flex;justify-content:flex-end}
.panel{width:min(560px,92vw);height:100%;background:var(--ink-1);border-left:1px solid var(--gold-3);padding:30px 30px 60px;overflow-y:auto}
.panel h3{font-family:"Noto Serif SC",serif;font-size:19px;color:var(--gold);margin:0 0 4px}
.panel .cid{font-family:"JetBrains Mono",monospace;font-size:11px;color:var(--fg-3)}
.panel .k{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--gold-2);letter-spacing:.18em;margin:20px 0 5px}
.panel .v{font-size:13.5px;color:var(--fg-1);line-height:1.75}
.panel .close{position:absolute;top:22px;right:26px;color:var(--fg-2);cursor:pointer;font-size:20px;font-family:monospace}
.axbig{display:flex;gap:10px;margin-top:6px}
.axbox{flex:1;background:var(--ink-2);border:1px solid var(--line-2);border-radius:3px;padding:8px 10px;text-align:center}
.axbox .l{font-size:9.5px;color:var(--fg-3);font-family:"JetBrains Mono",monospace}
.axbox .b{font-size:17px;color:var(--gold);font-family:"JetBrains Mono",monospace;margin-top:3px}
.big-link{display:inline-block;margin-top:14px;padding:10px 20px;background:var(--gold);color:var(--ink-0);border-radius:3px;font-weight:600;font-family:"Noto Serif SC",serif}
/* drawer v2: assets + evidence */
.alink{display:flex;align-items:baseline;gap:8px;padding:7px 10px;margin:4px 0;background:var(--ink-2);border:1px solid var(--line-2);border-radius:3px;font-size:12px;color:var(--fg-1);transition:border-color .15s}
a.alink:hover{border-color:var(--gold);color:var(--gold)}
.alink.local{cursor:default}
.alink .ak{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--gold-2);letter-spacing:.14em;border:1px solid var(--gold-3);padding:1px 5px;border-radius:2px;flex-shrink:0}
.alink .at{font-family:"JetBrains Mono",monospace;font-size:11.5px}
.alink .asub{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-3);margin-left:auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:46%}
.ev{font-size:12px;color:var(--fg-1);line-height:1.7;padding:7px 10px;margin:4px 0;background:var(--ink-2);border-left:2px solid var(--gold-3);border-radius:2px}
.ev b{font-family:"JetBrains Mono",monospace;color:var(--gold);margin-right:6px}
.fwrap{margin-top:5px;display:flex;gap:5px;flex-wrap:wrap}
.fchip{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-2);border:1px solid var(--line);padding:1px 6px;border-radius:2px}
.scmeta{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-3);margin-top:6px}
.cand{border-left:2px solid var(--down);background:var(--ink-2);padding:8px 11px;border-radius:2px;font-size:12.5px}
/* v3: proof + loop + verdict + deliverables */
.pitem{display:block;padding:8px 11px;margin:4px 0;background:var(--ink-2);border:1px solid var(--line-2);border-left:2px solid var(--gold);border-radius:3px;font-size:12px;color:var(--fg-1);transition:border-color .15s}
a.pitem:hover{border-color:var(--gold);color:var(--gold)}
.pitem .ak{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--gold-2);letter-spacing:.14em;border:1px solid var(--gold-3);padding:1px 5px;border-radius:2px;margin-right:7px}
.pitem .at{font-family:"Noto Serif SC",serif;font-size:12.5px;color:var(--fg-0)}
.pitem .pnum{font-family:"JetBrains Mono",monospace;font-size:11px;color:var(--gold);margin-top:4px;line-height:1.6}
.pitem .psrc{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--fg-3);margin-top:3px}
.pitem.noproof{border-left-color:var(--fg-3);color:var(--fg-3);font-size:11.5px}
.lprow{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.lseg{display:inline-flex;align-items:center;gap:5px;font-family:"JetBrains Mono",monospace;font-size:9.5px;padding:4px 8px;border-radius:2px;border:1px solid var(--line-2);background:var(--ink-2);color:var(--fg-2)}
.lseg i{width:7px;height:7px;border-radius:50%;display:inline-block}
.lseg.auto{color:var(--up);border-color:rgba(127,184,138,.35)}.lseg.auto i{background:var(--up)}
.lseg.manual{color:var(--hot);border-color:rgba(209,138,90,.35)}.lseg.manual i{background:var(--hot)}
.lseg.none{color:var(--fg-3);border-style:dashed}.lseg.none i{background:var(--fg-3)}
.larr{color:var(--fg-3);font-size:10px}
.hint{border-left:2px solid var(--cold);background:var(--ink-2);padding:8px 11px;border-radius:2px;font-size:12.5px}
.vd{font-size:12px;color:var(--fg-1);line-height:1.7;margin:8px 0 2px;padding:8px 11px;background:rgba(201,169,106,.05);border-left:2px solid var(--gold);border-radius:2px}
.dcard .vd{font-size:11px;margin:6px 0 4px;padding:6px 9px}
.dcard .lc{display:flex;align-items:center;gap:6px;font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-3);margin-top:7px}
.dcard .lc .bar{flex:1;height:4px;border-radius:2px;background:var(--ink-3);overflow:hidden}
.dcard .lc .bar i{display:block;height:100%;background:var(--up)}
.cellloop{display:flex;gap:2px;margin-top:7px}
.cellloop b{flex:1;height:3px;border-radius:1px}
/* deliverables page */
.dltable{width:100%;border-collapse:collapse;font-size:12px}
.dltable th{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--gold-2);letter-spacing:.14em;text-align:left;padding:7px 9px;border-bottom:1px solid var(--gold-3)}
.dltable td{padding:8px 9px;border-bottom:1px solid var(--line-2);color:var(--fg-1);vertical-align:top;line-height:1.6}
.dltable td.mono{font-family:"JetBrains Mono",monospace;font-size:10.5px}
.dltable tr:hover td{background:var(--ink-1)}
.dlnum{font-family:"JetBrains Mono",monospace;font-size:10.5px;color:var(--gold)}
.dlsrc{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--fg-3);display:block;margin-top:2px}
.cellchip{display:inline-block;font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--cold);border:1px solid rgba(106,143,168,.4);padding:1px 6px;border-radius:2px;margin:1px 3px 1px 0}
.cellchip:hover{color:var(--gold);border-color:var(--gold)}
.orphanbox{border:1px dashed var(--down);border-radius:3px;padding:14px 18px;margin:14px 0;background:rgba(201,122,114,.04)}
/* maps-audit */
.ascore{display:inline-block;min-width:22px;text-align:center;font-family:"JetBrains Mono",monospace;font-size:11px;padding:2px 6px;border-radius:2px;border:1px solid var(--line);cursor:help}
.ascore.a5,.ascore.a4{color:var(--up);border-color:rgba(127,184,138,.4)}
.ascore.a3{color:var(--gold);border-color:var(--gold-3)}
.ascore.a2{color:var(--hot);border-color:rgba(209,138,90,.4)}
.ascore.a1,.ascore.a0{color:var(--down);border-color:rgba(201,122,114,.4)}
.tbl-scroll{overflow-x:auto}
/* master: weekly focus strip */
.focus{display:flex;gap:9px;overflow-x:auto;padding-bottom:6px}
.fcell{flex:0 0 200px;background:var(--ink-1);border:1px solid var(--gold-3);border-radius:3px;padding:10px 12px;transition:border-color .15s,transform .12s}
.fcell:hover{border-color:var(--gold);transform:translateY(-2px)}
.fcell .fid{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-3)}
.fcell .fnm{font-family:"Noto Serif SC",serif;font-size:12.5px;color:var(--fg-0);margin:4px 0 3px;line-height:1.35}
.fcell .fpri{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--gold)}
.stamp{font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--fg-3);margin-left:auto;align-self:center;white-space:nowrap}
/* master: pmo bridge grid */
.bg-wrap{overflow-x:auto}
.bgrid{display:grid;grid-template-columns:110px repeat(8,minmax(64px,1fr));gap:3px;min-width:680px}
.bgh{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--gold-2);text-align:center;padding:5px 2px;letter-spacing:.05em}
.bgr{font-family:"Noto Serif SC",serif;font-size:11px;color:var(--fg-1);padding:6px 8px;background:var(--ink-1);border-radius:2px}
.bgc{border-radius:2px;background:var(--ink-2);min-height:26px;border:1px solid var(--line-2)}
.bgc.hit{background:rgba(201,169,106,.16);border-color:var(--gold-3)}
.bgc.void{background:repeating-linear-gradient(45deg,var(--ink-2),var(--ink-2) 4px,var(--ink-1) 4px,var(--ink-1) 8px)}
footer{margin-top:44px;border-top:1px solid var(--line-2);padding-top:14px;font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--fg-3);line-height:1.9}
/* 全信息量地图 + 详情页（版式语法源自企业大脑地图，配色守绿皮书 token） */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:9px;margin:14px 0 4px}
.metric{background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:9px 11px}
.metric .n{font-family:"JetBrains Mono",monospace;font-size:19px;color:var(--gold)}
.metric .l{font-size:10.5px;color:var(--fg-2);margin-top:4px}
.mg-wrap{overflow-x:auto;padding-bottom:8px}
.mapgrid{display:grid;gap:8px}
.mgh{font-family:"Noto Serif SC",serif;font-size:12px;color:var(--gold);text-align:center;padding:6px 4px;border-bottom:1px solid var(--gold-3)}
.mgh .sub{display:block;font-family:"JetBrains Mono",monospace;font-style:normal;font-size:8.5px;color:var(--fg-3);margin-top:2px;letter-spacing:.04em}
.mgl{display:flex;flex-direction:column;justify-content:center;padding:6px;border-right:1px solid var(--line-2)}
.mgl .d{font-family:"Noto Serif SC",serif;font-size:13px;color:var(--gold);font-weight:600}
.mgl .e{font-size:9px;color:var(--fg-3);margin-top:3px;line-height:1.4}
.mcell{position:relative;background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:10px 11px;cursor:pointer;transition:border-color .2s,transform .12s,box-shadow .2s;min-height:104px}
.mcell:hover{border-color:var(--gold);transform:translateY(-1px);box-shadow:0 6px 22px rgba(201,169,106,.09)}
.mcell::after{content:"";position:absolute;right:-1px;bottom:-1px;width:8px;height:8px;border-bottom:1px solid var(--gold-3);border-right:1px solid var(--gold-3)}
.mcell .top{display:flex;justify-content:space-between;align-items:baseline;gap:6px}
.mcell .mcid{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--fg-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mcell h3{font-family:"Noto Serif SC",serif;font-size:12.5px;color:var(--fg-0);margin:4px 0 4px;line-height:1.4;font-weight:600}
.mcell p{font-size:10.5px;color:var(--fg-2);margin:0 0 7px;line-height:1.55}
.mstat{font-family:"JetBrains Mono",monospace;font-size:8.5px;padding:1px 6px;border-radius:2px;border:1px solid currentColor;flex-shrink:0}
.mstat.ok{color:var(--up)}.mstat.part{color:var(--hot)}.mstat.gap{color:var(--down)}.mstat.dry{color:var(--cold)}
.mcell.gap{border-style:dashed;border-color:rgba(201,122,114,.45)}
.mchips{display:flex;gap:4px;flex-wrap:wrap}
.mchip{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--fg-2);border:1px solid var(--line);padding:1px 5px;border-radius:2px}
.mchip.gold{color:var(--gold);border-color:var(--gold-3)}
.mchip.ok{color:var(--up);border-color:rgba(127,184,138,.4)}
.mchip.gap{color:var(--down);border-color:rgba(201,122,114,.4)}
.vapill{font-family:"JetBrains Mono",monospace;font-size:9px;border:1px solid currentColor;padding:1px 6px;border-radius:2px;flex-shrink:0}
/* CBM-OSA-IPO v2：IPO 药丸（与 V·A 并列的第二读数轴）+ 四道门 + 距100分清单 */
.ipopill{font-family:"JetBrains Mono",monospace;font-size:8.5px;border:1px dashed currentColor;padding:1px 5px;border-radius:2px;flex-shrink:0;opacity:.92}
.iporow{display:flex;gap:8px;align-items:baseline;padding:5px 0;border-bottom:1px dotted var(--line-2)}
.iporow .ipoax{flex:0 0 96px;font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--fg-2)}
.iporow .ipsc{flex:0 0 46px;font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:600}
.iporow .ipoev{flex:1;font-size:10.5px;color:var(--fg-1);line-height:1.55}
.gaterow{display:flex;gap:8px;align-items:baseline;padding:4px 0}
.gate{flex:0 0 auto;font-family:"JetBrains Mono",monospace;font-size:9px;padding:2px 7px;border-radius:2px;border:1px solid currentColor}
.gate.pass{color:var(--up)}.gate.partial{color:var(--gold)}.gate.fail{color:var(--down)}
.gaterow .greason{flex:1;font-size:10.5px;color:var(--fg-1);line-height:1.55}
.gaplist{display:flex;flex-direction:column;gap:0;margin:8px 0}
.gaprow{display:flex;gap:10px;align-items:baseline;padding:6px 0;border-bottom:1px dotted var(--line-2)}
.gaprow .gid{flex:0 0 190px;font-family:"JetBrains Mono",monospace;font-size:9.5px;color:var(--gold-2)}
.gaprow .gg{flex:1;font-size:10.5px;color:var(--fg-1);line-height:1.55}
.scoreband{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0;align-items:stretch}
.sax{flex:1;min-width:130px;background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:10px 12px;cursor:help}
.sax .l{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--fg-3);letter-spacing:.14em}
.sax .b{font-family:"JetBrains Mono",monospace;font-size:22px;margin-top:4px}
.sax .d{font-size:9.5px;color:var(--fg-2);margin-top:4px;line-height:1.5}
.smin{flex:0 0 150px;background:rgba(201,169,106,.07);border:1px solid var(--gold-3);border-radius:3px;padding:10px 12px;text-align:center}
.smin .b{font-family:"JetBrains Mono",monospace;font-size:26px;color:var(--gold);margin-top:2px}
.judgegrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.judge{background:var(--ink-1);border:1px solid var(--line-2);border-radius:3px;padding:13px 15px}
.judge h3{font-family:"Noto Serif SC",serif;font-size:13.5px;color:var(--gold);margin:0 0 6px;font-weight:600}
.judge p{font-size:11.5px;color:var(--fg-1);margin:0;line-height:1.7}
.judge .jtag{font-family:"JetBrains Mono",monospace;font-size:8.5px;color:var(--gold-2);letter-spacing:.18em;margin-bottom:5px}
/* 8 图横向切换条（详情页/全信息页互跳，补全连通图）*/
.mapsw{display:flex;gap:6px;overflow-x:auto;padding:4px 0 10px;margin:2px 0 4px}
.mapsw a{flex:0 0 auto;font-family:"Noto Serif SC",serif;font-size:11px;color:var(--fg-2);padding:5px 11px;border:1px solid var(--line-2);border-radius:2px;background:var(--ink-1);white-space:nowrap;transition:border-color .15s,color .15s}
.mapsw a:hover{border-color:var(--gold);color:var(--gold)}
.mapsw a.on{color:var(--gold);border-color:var(--gold-3);background:rgba(201,169,106,.08)}
.mapsw a .mn{font-family:"JetBrains Mono",monospace;font-size:9px;color:var(--gold-2);margin-left:5px}
/* 首页全信息量地图凸显入口 */
.atlascta{display:block;position:relative;background:linear-gradient(100deg,rgba(201,169,106,.10),rgba(106,143,168,.05));border:1px solid var(--gold-3);border-radius:4px;padding:16px 20px;margin:16px 0;transition:border-color .2s,transform .12s}
.atlascta:hover{border-color:var(--gold);transform:translateY(-1px)}
.atlascta .t{font-family:"Noto Serif SC",serif;font-size:16px;color:var(--gold);font-weight:600}
.atlascta .d{font-size:11.5px;color:var(--fg-1);margin-top:5px;line-height:1.7}
.atlascta .go{position:absolute;right:20px;top:50%;transform:translateY(-50%);font-family:"JetBrains Mono",monospace;font-size:11px;color:var(--gold)}
@media(max-width:820px){.dgrid{grid-template-columns:1fr}.mx{grid-template-columns:1fr}.lyrow-h{border-right:none;border-top:1px solid var(--gold-3);padding-top:12px}.nav .right{display:none}.atlascta .go{display:none}}

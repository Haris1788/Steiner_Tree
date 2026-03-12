"""
Proof of Theorem 3.2 — 4 vertices, 3 slides.
Detailed construction: G → metric closure G'.
Run to generate and open the HTML page.
"""
import webbrowser, os

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Proof of Theorem 3.2 — Step by Step</title>
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
:root{--bg:#0f172a;--card:#1e293b;--accent:#3b82f6;--green:#22c55e;--red:#ef4444;
--orange:#f59e0b;--purple:#a855f7;--text:#e2e8f0;--muted:#94a3b8;--border:#334155;}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.72;padding:0}
.slide{min-height:100vh;padding:48px 0 56px;border-bottom:3px solid var(--border);position:relative}
.slide-num{position:absolute;top:18px;right:28px;font-size:.82em;color:#475569;font-weight:700;letter-spacing:1px}
.inner{max-width:980px;margin:0 auto;padding:0 28px}
.slide-title{font-size:1.85em;color:#fff;margin-bottom:6px;font-weight:700}
.slide-sub{font-size:1em;color:var(--muted);margin-bottom:24px}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px 26px;margin-bottom:24px;box-shadow:0 3px 16px rgba(0,0,0,.25);position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;border-radius:14px 0 0 14px}
.card.c-blue::before{background:var(--accent)}.card.c-green::before{background:var(--green)}
.card.c-red::before{background:var(--red)}.card.c-purple::before{background:var(--purple)}
.card.c-orange::before{background:var(--orange)}
.tag{display:inline-block;font-size:.7em;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;padding:3px 12px;border-radius:18px;margin-bottom:10px}
.tag-blue{background:rgba(59,130,246,.14);color:var(--accent)}
.tag-green{background:rgba(34,197,94,.14);color:var(--green)}
.tag-red{background:rgba(239,68,68,.14);color:var(--red)}
.tag-purple{background:rgba(168,85,247,.14);color:var(--purple)}
.tag-orange{background:rgba(245,158,11,.14);color:var(--orange)}
.card h3{font-size:1.22em;color:#fff;margin-bottom:10px}
.card p{margin-bottom:8px;font-size:.95em}
.card ul{padding-left:20px;margin:6px 0 8px}.card li{margin-bottom:4px;font-size:.93em}
.math-box{background:rgba(59,130,246,.05);border:1px solid rgba(59,130,246,.14);border-radius:10px;padding:14px 20px;margin:14px 0;text-align:center;overflow-x:auto}
.svg-wrap{background:#111827;border:1px solid var(--border);border-radius:10px;padding:16px 8px 10px;margin:16px auto;text-align:center;max-width:100%;overflow-x:auto}
.svg-wrap .cap{font-size:.76em;color:#64748b;margin-top:8px;font-style:italic}
svg text{font-family:'Segoe UI',system-ui,sans-serif}
.legend{display:flex;gap:20px;flex-wrap:wrap;margin:10px 0 4px;font-size:.85em}
.legend span{display:flex;align-items:center;gap:5px}
.legend .dot{width:13px;height:13px;border-radius:50%;display:inline-block}
.qed{text-align:right;font-size:1.4em;color:var(--green);margin-top:6px}
.pair-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}
.pair-box{background:#111827;border:1px solid var(--border);border-radius:10px;padding:14px 16px;font-size:.92em}
.pair-box .phead{color:#f59e0b;font-weight:700;margin-bottom:6px;font-size:.95em}
.pair-box .path{color:#94a3b8;margin-bottom:3px;font-size:.88em}
.pair-box .best{color:#22c55e;font-weight:700;font-size:.95em}
@media(max-width:700px){.slide{padding:28px 0 36px}.inner{padding:0 10px}.slide-title{font-size:1.35em}.card{padding:18px 14px}.pair-grid{grid-template-columns:1fr}}
</style>
</head>
<body>

<!-- ================================================================ -->
<!--  SLIDE 1 — THE CONSTRUCTION: G → G'                             -->
<!-- ================================================================ -->
<div class="slide" id="slide1">
<span class="slide-num">SLIDE 1 / 3</span>
<div class="inner">
<div class="slide-title">Slide 1: Constructing the Metric Closure</div>
<div class="slide-sub">Transform instance $I = (G, R, \text{cost})$ into metric instance $I' = (G', R, \text{cost}')$ in polynomial time</div>

<!-- ---- Step A: Given G ---- -->
<div class="card c-blue">
  <span class="tag tag-blue">Given</span>
  <h3>Instance $I$: Graph $G = (V, E)$</h3>
  <p>$V = \{a, b, c, d\}$, &ensp; <strong style="color:#3b82f6">Required</strong> $R = \{a, c, d\}$, &ensp; <strong style="color:#94a3b8">Steiner</strong> $= \{b\}$</p>
  <div class="legend">
    <span><span class="dot" style="background:#3b82f6"></span> Required vertex</span>
    <span><span class="dot" style="background:#64748b"></span> Steiner vertex</span>
    <span style="color:#f59e0b">&#9644; edge with cost</span>
  </div>
  <div class="svg-wrap">
    <svg width="420" height="260" viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">
      <!-- Edges -->
      <line x1="80" y1="70" x2="230" y2="40" stroke="#475569" stroke-width="2.5"/>
      <line x1="230" y1="40" x2="100" y2="200" stroke="#475569" stroke-width="2.5"/>
      <line x1="230" y1="40" x2="340" y2="180" stroke="#475569" stroke-width="2.5"/>
      <line x1="80" y1="70" x2="100" y2="200" stroke="#475569" stroke-width="2.5"/>
      <line x1="100" y1="200" x2="340" y2="180" stroke="#475569" stroke-width="2.5"/>
      <!-- Cost labels -->
      <rect x="138" y="38" width="28" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
      <text x="152" y="53" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="700">3</text>
      <rect x="148" y="112" width="28" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
      <text x="162" y="127" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>
      <rect x="272" y="100" width="28" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
      <text x="286" y="115" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="700">4</text>
      <rect x="66" y="128" width="28" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
      <text x="80" y="143" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="700">7</text>
      <rect x="202" y="200" width="28" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
      <text x="216" y="215" font-size="13" fill="#f59e0b" text-anchor="middle" font-weight="700">8</text>
      <!-- Vertices -->
      <circle cx="80" cy="70" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="80" y="77" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="230" cy="40" r="20" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
      <text x="230" y="47" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="100" cy="200" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="100" y="207" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="340" cy="180" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="340" y="187" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <!-- note: no a-d edge -->
      <text x="210" y="250" font-size="11" fill="#64748b" text-anchor="middle" font-style="italic">5 edges. Note: no direct edge between a and d.</text>
    </svg>
  </div>
</div>

<!-- ---- Step B: THE CONSTRUCTION ---- -->
<div class="card c-orange">
  <span class="tag tag-orange">Construction — Step 1</span>
  <h3>Let $G'$ be the complete graph on $V$. Define $\text{cost}'(u,v) = $ shortest $u$-$v$ path in $G$.</h3>
  <p>We must compute the shortest-path distance for <strong>every pair</strong> of vertices. With 4 vertices we have $\binom{4}{2}=6$ pairs:</p>

  <!-- 6 pair boxes in a 2-column grid -->
  <div class="pair-grid">

    <!-- pair a-b -->
    <div class="pair-box">
      <div class="phead">Pair (a, b)</div>
      <div class="path">&#8226; Direct edge a&#8211;b: cost = <strong>3</strong></div>
      <div class="path">&#8226; Via c: a&#8594;c&#8594;b = 7+2 = 9</div>
      <div class="best">&#10230; cost'(a,b) = min(3, 9) = <span style="color:#22c55e">3</span></div>
    </div>

    <!-- pair a-c -->
    <div class="pair-box">
      <div class="phead">Pair (a, c)</div>
      <div class="path">&#8226; Direct edge a&#8211;c: cost = 7</div>
      <div class="path">&#8226; Via b: a&#8594;b&#8594;c = 3+2 = <strong>5</strong></div>
      <div class="best">&#10230; cost'(a,c) = min(7, 5) = <span style="color:#22c55e">5</span> &ensp;&#11088; shorter!</div>
    </div>

    <!-- pair a-d -->
    <div class="pair-box">
      <div class="phead">Pair (a, d)</div>
      <div class="path">&#8226; No direct edge a&#8211;d in G</div>
      <div class="path">&#8226; Via b: a&#8594;b&#8594;d = 3+4 = <strong>7</strong></div>
      <div class="path">&#8226; Via c,b: a&#8594;c&#8594;b&#8594;d = 7+2+4 = 13</div>
      <div class="best">&#10230; cost'(a,d) = <span style="color:#22c55e">7</span> &ensp;(new edge!)</div>
    </div>

    <!-- pair b-c -->
    <div class="pair-box">
      <div class="phead">Pair (b, c)</div>
      <div class="path">&#8226; Direct edge b&#8211;c: cost = <strong>2</strong></div>
      <div class="path">&#8226; Via a: b&#8594;a&#8594;c = 3+7 = 10</div>
      <div class="best">&#10230; cost'(b,c) = min(2, 10) = <span style="color:#22c55e">2</span></div>
    </div>

    <!-- pair b-d -->
    <div class="pair-box">
      <div class="phead">Pair (b, d)</div>
      <div class="path">&#8226; Direct edge b&#8211;d: cost = <strong>4</strong></div>
      <div class="path">&#8226; Via c: b&#8594;c&#8594;d = 2+8 = 10</div>
      <div class="best">&#10230; cost'(b,d) = min(4, 10) = <span style="color:#22c55e">4</span></div>
    </div>

    <!-- pair c-d -->
    <div class="pair-box">
      <div class="phead">Pair (c, d)</div>
      <div class="path">&#8226; Direct edge c&#8211;d: cost = 8</div>
      <div class="path">&#8226; Via b: c&#8594;b&#8594;d = 2+4 = <strong>6</strong></div>
      <div class="best">&#10230; cost'(c,d) = min(8, 6) = <span style="color:#22c55e">6</span> &ensp;&#11088; shorter!</div>
    </div>
  </div>
</div>

<!-- ---- Step C: Visualise the transformation ---- -->
<div class="card c-green">
  <span class="tag tag-green">Construction — Step 2</span>
  <h3>Result: Metric Closure $G'$ (Complete Graph on $V$)</h3>
  <p>$G'$ has <strong>all $\binom{4}{2}=6$ edges</strong>, each labelled with the shortest-path distance from $G$:</p>

  <div class="svg-wrap">
    <svg width="860" height="300" viewBox="0 0 860 300" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="gl"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <marker id="arr" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto">
          <path d="M0,0 L0,8 L10,4 z" fill="#94a3b8"/>
        </marker>
      </defs>

      <!-- LEFT: Original G -->
      <text x="135" y="24" font-size="14" fill="#3b82f6" text-anchor="middle" font-weight="700">Original G (5 edges)</text>
      <line x1="60" y1="80" x2="180" y2="55" stroke="#475569" stroke-width="2"/>
      <line x1="180" y1="55" x2="80" y2="185" stroke="#475569" stroke-width="2"/>
      <line x1="180" y1="55" x2="245" y2="165" stroke="#475569" stroke-width="2"/>
      <line x1="60" y1="80" x2="80" y2="185" stroke="#475569" stroke-width="2"/>
      <line x1="80" y1="185" x2="245" y2="165" stroke="#475569" stroke-width="2"/>
      <text x="112" y="58" font-size="10" fill="#f59e0b" font-weight="700">3</text>
      <text x="118" y="118" font-size="10" fill="#f59e0b" font-weight="700">2</text>
      <text x="218" y="104" font-size="10" fill="#f59e0b" font-weight="700">4</text>
      <text x="54" y="136" font-size="10" fill="#f59e0b" font-weight="700">7</text>
      <text x="162" y="186" font-size="10" fill="#f59e0b" font-weight="700">8</text>
      <circle cx="60" cy="80" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="60" y="85" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="180" cy="55" r="14" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
      <text x="180" y="60" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="80" cy="185" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="80" y="190" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="245" cy="165" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="245" y="170" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">d</text>

      <!-- Big arrow -->
      <line x1="300" y1="120" x2="395" y2="120" stroke="#94a3b8" stroke-width="2.5" marker-end="url(#arr)"/>
      <text x="348" y="106" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="600">compute shortest</text>
      <text x="348" y="118" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="600">path for every pair</text>
      <text x="348" y="142" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">make complete graph</text>

      <!-- RIGHT: G' complete -->
      <text x="620" y="24" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">Metric Closure G' (6 edges — complete)</text>

      <!-- 6 edges of complete graph -->
      <!-- a(440,100) b(600,60) c(480,230) d(720,200) -->
      <line x1="440" y1="100" x2="600" y2="60"  stroke="#22c55e" stroke-width="2.2" opacity=".6"/>
      <line x1="440" y1="100" x2="480" y2="230" stroke="#22c55e" stroke-width="2.2" opacity=".6"/>
      <line x1="440" y1="100" x2="720" y2="200" stroke="#22c55e" stroke-width="2.2" stroke-dasharray="6,3"/>
      <line x1="600" y1="60"  x2="480" y2="230" stroke="#22c55e" stroke-width="2.2" opacity=".6"/>
      <line x1="600" y1="60"  x2="720" y2="200" stroke="#22c55e" stroke-width="2.2" opacity=".6"/>
      <line x1="480" y1="230" x2="720" y2="200" stroke="#22c55e" stroke-width="2.2" opacity=".6"/>

      <!-- Cost labels in G' -->
      <rect x="502" y="62" width="26" height="18" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width=".8"/>
      <text x="515" y="76" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">3</text>

      <rect x="440" y="157" width="26" height="18" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width=".8"/>
      <text x="453" y="171" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">5</text>

      <!-- a-d dashed = new edge -->
      <rect x="570" y="142" width="26" height="18" rx="4" fill="#0f172a" stroke="#ef4444" stroke-width="1.2"/>
      <text x="583" y="156" font-size="11" fill="#ef4444" text-anchor="middle" font-weight="700">7</text>

      <rect x="524" y="137" width="26" height="18" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width=".8"/>
      <text x="537" y="151" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">2</text>

      <rect x="652" y="118" width="26" height="18" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width=".8"/>
      <text x="665" y="132" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">4</text>

      <rect x="584" y="224" width="26" height="18" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width=".8"/>
      <text x="597" y="238" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">6</text>

      <!-- Vertices of G' -->
      <circle cx="440" cy="100" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
      <text x="440" y="107" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="600" cy="60"  r="18" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
      <text x="600" y="67"  font-size="15" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="480" cy="230" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
      <text x="480" y="237" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="720" cy="200" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
      <text x="720" y="207" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">d</text>

      <!-- annotation: new edge -->
      <text x="620" y="166" font-size="9" fill="#ef4444" font-style="italic">new!</text>

      <!-- Annotations below -->
      <rect x="410" y="262" width="340" height="30" rx="7" fill="rgba(34,197,94,.06)" stroke="rgba(34,197,94,.2)"/>
      <text x="580" y="282" font-size="10" fill="#22c55e" text-anchor="middle" font-weight="600">Triangle inequality holds: cost'(u,w) &#8804; cost'(u,v) + cost'(v,w)</text>
    </svg>
    <div class="cap">G had 5 edges; G' has 6 (one new edge: a&#8211;d with cost 7, computed via shortest path a&#8594;b&#8594;d). Three edges got cheaper costs (a&#8211;c: 7&#8594;5, c&#8211;d: 8&#8594;6, and new a&#8211;d: &#8734;&#8594;7).</div>
  </div>

  <div class="math-box">
    $$G' = \text{complete graph on } V, \quad \text{cost}'(u,v) = \text{dist}_G(u,v)$$
  </div>
  <p>The partition of $V$ into Required and Steiner stays the same: $R' = R = \{a,c,d\}$.</p>
  <p style="color:#f59e0b"><strong>Key property:</strong> For any edge $(u,v) \in E$, its cost in $G'$ is <em>at most</em> its cost in $G$ (the edge itself is one candidate path).</p>
</div>

</div>
</div>


<!-- ================================================================ -->
<!--  SLIDE 2 — PROOF STEPS: LOWER BOUND + MAPPING BACK              -->
<!-- ================================================================ -->
<div class="slide" id="slide2">
<span class="slide-num">SLIDE 2 / 3</span>
<div class="inner">
<div class="slide-title">Slide 2: The Proof — Two Directions</div>
<div class="slide-sub">Show $OPT(I') \leq OPT(I)$, then show how to map any solution back without increasing cost</div>

<!-- ---- Lower Bound ---- -->
<div class="card c-blue">
  <span class="tag tag-blue">Direction 1 — Lower Bound</span>
  <h3>$OPT(I') \leq OPT(I)$</h3>
  <p>"For any edge $(u,v) \in E$, its cost in $G'$ is no more than its cost in $G$."</p>
  <p>Therefore the optimal tree of $G$ can be placed into $G'$ with equal or lower cost:</p>

  <div class="svg-wrap">
    <svg width="760" height="260" viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a1" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker></defs>

      <!-- LEFT: OPT in G -->
      <text x="130" y="22" font-size="13" fill="#3b82f6" text-anchor="middle" font-weight="700">OPT in G = {a-b, b-c, b-d}</text>
      <line x1="55" y1="80" x2="155" y2="58" stroke="#3b82f6" stroke-width="3.5"/>
      <line x1="155" y1="58" x2="85" y2="170" stroke="#3b82f6" stroke-width="3.5"/>
      <line x1="155" y1="58" x2="240" y2="150" stroke="#3b82f6" stroke-width="3.5"/>
      <text x="95" y="60" font-size="12" fill="#f59e0b" font-weight="700">3</text>
      <text x="106" y="118" font-size="12" fill="#f59e0b" font-weight="700">2</text>
      <text x="205" y="100" font-size="12" fill="#f59e0b" font-weight="700">4</text>
      <circle cx="55" cy="80" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="55" y="86" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="155" cy="58" r="16" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
      <text x="155" y="64" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="85" cy="170" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="85" y="176" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="240" cy="150" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="240" y="156" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <rect x="40" y="195" width="220" height="28" rx="7" fill="rgba(59,130,246,.1)" stroke="rgba(59,130,246,.3)"/>
      <text x="150" y="214" font-size="13" fill="#3b82f6" text-anchor="middle" font-weight="700">cost = 3 + 2 + 4 = 9</text>

      <!-- Arrow -->
      <line x1="310" y1="115" x2="405" y2="115" stroke="#94a3b8" stroke-width="2" marker-end="url(#a1)"/>
      <text x="358" y="100" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">same edges exist</text>
      <text x="358" y="112" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">in G' with cost' &#8804; cost</text>

      <!-- RIGHT: Same tree in G' -->
      <text x="570" y="22" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">Same tree in G'</text>
      <line x1="470" y1="80" x2="570" y2="58" stroke="#22c55e" stroke-width="3.5"/>
      <line x1="570" y1="58" x2="500" y2="170" stroke="#22c55e" stroke-width="3.5"/>
      <line x1="570" y1="58" x2="655" y2="150" stroke="#22c55e" stroke-width="3.5"/>
      <text x="510" y="60" font-size="12" fill="#22c55e" font-weight="700">3</text>
      <text x="522" y="118" font-size="12" fill="#22c55e" font-weight="700">2</text>
      <text x="620" y="100" font-size="12" fill="#22c55e" font-weight="700">4</text>

      <!-- edge cost comparison annotation -->
      <text x="540" y="53" font-size="8" fill="#94a3b8">&#8804; 3 &#10003;</text>
      <text x="550" y="126" font-size="8" fill="#94a3b8">&#8804; 2 &#10003;</text>
      <text x="640" y="107" font-size="8" fill="#94a3b8">&#8804; 4 &#10003;</text>

      <circle cx="470" cy="80" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="470" y="86" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="570" cy="58" r="16" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
      <text x="570" y="64" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="500" cy="170" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="500" y="176" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="655" cy="150" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
      <text x="655" y="156" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <rect x="455" y="195" width="225" height="28" rx="7" fill="rgba(34,197,94,.1)" stroke="rgba(34,197,94,.3)"/>
      <text x="568" y="214" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">cost' = 3 + 2 + 4 = 9 &#8804; 9 &#10003;</text>

      <!-- Bottom note -->
      <rect x="170" y="235" width="420" height="22" rx="6" fill="rgba(245,158,11,.08)" stroke="rgba(245,158,11,.2)"/>
      <text x="380" y="251" font-size="11" fill="#f59e0b" text-anchor="middle" font-weight="600">Every edge in G exists in G' with cost' &#8804; cost &#8658; OPT(I') &#8804; OPT(I)</text>
    </svg>
  </div>
  <div class="math-box">$$OPT(I') \leq OPT(I)$$</div>
</div>

<!-- ---- Mapping Back ---- -->
<div class="card c-red">
  <span class="tag tag-red">Direction 2 — Mapping Back</span>
  <h3>Given Steiner tree $T'$ in $I'$, obtain tree $T$ in $I$ with $\text{cost}(T) \leq \text{cost}'(T')$</h3>
  <p>"The cost of an edge $(u,v)$ in $G'$ <em>corresponds to the cost of a path</em> in $G$. Replace each edge of $T'$ by the corresponding path."</p>

  <p style="margin-top:14px"><strong>Step A:</strong> Suppose an $\alpha$-approximation gives Steiner tree $T' = \{a\text{-}c,\; c\text{-}d\}$ in $G'$:</p>

  <div class="svg-wrap">
    <svg width="460" height="150" viewBox="0 0 460 150" xmlns="http://www.w3.org/2000/svg">
      <text x="230" y="18" font-size="12" fill="#ef4444" text-anchor="middle" font-weight="700">Approximate tree T' in G' (connects a, c, d)</text>
      <line x1="70" y1="80" x2="225" y2="80" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="225" y1="80" x2="390" y2="80" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <rect x="130" y="55" width="30" height="20" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
      <text x="145" y="70" font-size="12" fill="#ef4444" text-anchor="middle" font-weight="700">5</text>
      <rect x="290" y="55" width="30" height="20" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
      <text x="305" y="70" font-size="12" fill="#ef4444" text-anchor="middle" font-weight="700">6</text>
      <circle cx="70" cy="80" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="70" y="87" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="225" cy="80" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="225" y="87" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="390" cy="80" r="16" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text x="390" y="87" font-size="14" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <rect x="130" y="110" width="200" height="28" rx="7" fill="rgba(239,68,68,.1)" stroke="rgba(239,68,68,.3)"/>
      <text x="230" y="130" font-size="13" fill="#ef4444" text-anchor="middle" font-weight="700">cost'(T') = 5 + 6 = 11</text>
    </svg>
  </div>

  <p><strong>Step B:</strong> Replace each edge of $T'$ by its <em>corresponding shortest path</em> in $G$:</p>

  <div class="svg-wrap">
    <svg width="720" height="210" viewBox="0 0 720 210" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>

      <!-- Row 1: edge a-c in G' → path a→b→c in G -->
      <rect x="8" y="8" width="200" height="72" rx="8" fill="rgba(239,68,68,.05)" stroke="rgba(239,68,68,.2)"/>
      <text x="108" y="28" font-size="10" fill="#ef4444" text-anchor="middle" font-weight="700">Edge (a,c) in T' — cost' = 5</text>
      <line x1="38" y1="52" x2="168" y2="52" stroke="#ef4444" stroke-width="3.5" stroke-linecap="round"/>
      <circle cx="38" cy="52" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="38" y="56" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="168" cy="52" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="168" y="56" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">c</text>

      <line x1="222" y1="44" x2="295" y2="44" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a2)"/>
      <text x="258" y="38" font-size="9" fill="#94a3b8" text-anchor="middle" font-style="italic">replace</text>

      <rect x="308" y="8" width="400" height="72" rx="8" fill="rgba(59,130,246,.05)" stroke="rgba(59,130,246,.2)"/>
      <text x="508" y="28" font-size="10" fill="#3b82f6" text-anchor="middle" font-weight="700">Shortest path a&#8594;b&#8594;c in G — cost = 3+2 = 5</text>
      <line x1="348" y1="52" x2="508" y2="52" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>
      <line x1="508" y1="52" x2="668" y2="52" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>
      <circle cx="348" cy="52" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="348" y="56" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="508" cy="52" r="11" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="508" y="56" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="668" cy="52" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="668" y="56" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <text x="428" y="46" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="700">3</text>
      <text x="588" y="46" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>

      <!-- Row 2: edge c-d in G' → path c→b→d in G -->
      <rect x="8" y="100" width="200" height="72" rx="8" fill="rgba(239,68,68,.05)" stroke="rgba(239,68,68,.2)"/>
      <text x="108" y="120" font-size="10" fill="#ef4444" text-anchor="middle" font-weight="700">Edge (c,d) in T' — cost' = 6</text>
      <line x1="38" y1="144" x2="168" y2="144" stroke="#ef4444" stroke-width="3.5" stroke-linecap="round"/>
      <circle cx="38" cy="144" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="38" y="148" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="168" cy="144" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="168" y="148" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">d</text>

      <line x1="222" y1="136" x2="295" y2="136" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a2)"/>
      <text x="258" y="130" font-size="9" fill="#94a3b8" text-anchor="middle" font-style="italic">replace</text>

      <rect x="308" y="100" width="400" height="72" rx="8" fill="rgba(59,130,246,.05)" stroke="rgba(59,130,246,.2)"/>
      <text x="508" y="120" font-size="10" fill="#3b82f6" text-anchor="middle" font-weight="700">Shortest path c&#8594;b&#8594;d in G — cost = 2+4 = 6</text>
      <line x1="348" y1="144" x2="508" y2="144" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>
      <line x1="508" y1="144" x2="668" y2="144" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>
      <circle cx="348" cy="144" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="348" y="148" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="508" cy="144" r="11" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="508" y="148" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="668" cy="144" r="11" fill="#3b82f6" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="668" y="148" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <text x="428" y="138" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>
      <text x="588" y="138" font-size="10" fill="#f59e0b" text-anchor="middle" font-weight="700">4</text>

      <!-- Bottom note -->
      <rect x="8" y="184" width="700" height="22" rx="6" fill="rgba(168,85,247,.08)" stroke="rgba(168,85,247,.25)"/>
      <text x="358" y="200" font-size="10" fill="#a855f7" text-anchor="middle" font-weight="700">Union of paths: {a&#8211;b(3), b&#8211;c(2)} &#8746; {c&#8211;b(2), b&#8211;d(4)} = edges {a&#8211;b, b&#8211;c, b&#8211;d} with duplicate b&#8211;c removed</text>
    </svg>
  </div>

  <p><strong>Step C:</strong> "All required vertices are connected. However, this subgraph may contain cycles. If so, remove edges to obtain tree $T$."</p>
  <p>In our example, after removing the duplicate $b$-$c$ edge, the subgraph is already a tree:</p>

  <div class="svg-wrap">
    <svg width="500" height="200" viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg">
      <text x="250" y="20" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">Final Steiner Tree T in G</text>
      <!-- Tree: a-b(3), b-c(2), b-d(4) -->
      <line x1="90" y1="100" x2="250" y2="70" stroke="#22c55e" stroke-width="4" stroke-linecap="round"/>
      <line x1="250" y1="70"  x2="150" y2="160" stroke="#22c55e" stroke-width="4" stroke-linecap="round"/>
      <line x1="250" y1="70"  x2="400" y2="140" stroke="#22c55e" stroke-width="4" stroke-linecap="round"/>
      <text x="158" y="76" font-size="13" fill="#f59e0b" font-weight="700">3</text>
      <text x="185" y="118" font-size="13" fill="#f59e0b" font-weight="700">2</text>
      <text x="333" y="100" font-size="13" fill="#f59e0b" font-weight="700">4</text>
      <circle cx="90"  cy="100" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text   x="90"  y="107" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">a</text>
      <circle cx="250" cy="70"  r="18" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
      <text   x="250" y="77"  font-size="15" fill="#fff" text-anchor="middle" font-weight="700">b</text>
      <circle cx="150" cy="160" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text   x="150" y="167" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">c</text>
      <circle cx="400" cy="140" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
      <text   x="400" y="147" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">d</text>
      <rect x="115" y="180" width="280" height="18" rx="5" fill="rgba(34,197,94,.1)" stroke="rgba(34,197,94,.3)"/>
      <text x="255" y="194" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="700">cost(T) = 3 + 2 + 4 = 9 &#8804; 11 = cost'(T') &#10003;</text>
    </svg>
  </div>

  <div class="math-box">$$\text{cost}(T) \leq \text{cost}'(T')$$</div>
  <p style="color:#94a3b8;font-size:.88em">"Replace each edge of $T'$ by the corresponding path to obtain a subgraph of $G$. All required vertices are connected. Remove edges to get tree $T$."</p>
</div>

</div>
</div>


<!-- ================================================================ -->
<!--  SLIDE 3 — CONCLUSION                                            -->
<!-- ================================================================ -->
<div class="slide" id="slide3">
<span class="slide-num">SLIDE 3 / 3</span>
<div class="inner">
<div class="slide-title">Slide 3: Conclusion — Factor-Preserving Reduction</div>
<div class="slide-sub">Putting it all together</div>

<div class="card c-purple">
  <span class="tag tag-purple">The Reduction Pipeline</span>
  <h3>Overview: $I \to I' \to T' \to T$</h3>

  <div class="svg-wrap">
    <svg width="720" height="260" viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="a4" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#a855f7"/></marker>
        <marker id="a5" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
      </defs>

      <!-- Box: I -->
      <rect x="10" y="25" width="190" height="80" rx="14" fill="rgba(59,130,246,.1)" stroke="#3b82f6" stroke-width="2"/>
      <text x="105" y="55" font-size="15" fill="#3b82f6" text-anchor="middle" font-weight="700">Instance I</text>
      <text x="105" y="76" font-size="11" fill="#94a3b8" text-anchor="middle">General Graph G</text>
      <text x="105" y="92" font-size="10" fill="#64748b" text-anchor="middle">V={a,b,c,d}, R={a,c,d}</text>

      <!-- Arrow right -->
      <line x1="210" y1="65" x2="300" y2="65" stroke="#a855f7" stroke-width="2.5" marker-end="url(#a4)"/>
      <text x="255" y="52" font-size="9" fill="#a855f7" text-anchor="middle" font-weight="600">metric closure</text>
      <text x="255" y="82" font-size="8" fill="#64748b" text-anchor="middle">(poly time)</text>

      <!-- Box: I' -->
      <rect x="310" y="25" width="190" height="80" rx="14" fill="rgba(34,197,94,.1)" stroke="#22c55e" stroke-width="2"/>
      <text x="405" y="55" font-size="15" fill="#22c55e" text-anchor="middle" font-weight="700">Instance I'</text>
      <text x="405" y="76" font-size="11" fill="#94a3b8" text-anchor="middle">Metric Graph G'</text>
      <text x="405" y="92" font-size="10" fill="#64748b" text-anchor="middle">Complete, triangle ineq.</text>

      <!-- Arrow down -->
      <line x1="405" y1="115" x2="405" y2="160" stroke="#22c55e" stroke-width="2.5" marker-end="url(#a5)"/>
      <text x="460" y="142" font-size="9" fill="#22c55e" text-anchor="middle" font-weight="600">&#945;-approx alg.</text>

      <!-- Box: T' -->
      <rect x="310" y="170" width="190" height="65" rx="14" fill="rgba(239,68,68,.1)" stroke="#ef4444" stroke-width="2"/>
      <text x="405" y="197" font-size="14" fill="#ef4444" text-anchor="middle" font-weight="700">Approx Tree T'</text>
      <text x="405" y="218" font-size="11" fill="#94a3b8" text-anchor="middle">cost'(T') &#8804; &#945;&#183;OPT(I')</text>

      <!-- Arrow left -->
      <line x1="300" y1="202" x2="210" y2="202" stroke="#a855f7" stroke-width="2.5" marker-end="url(#a4)"/>
      <text x="255" y="192" font-size="9" fill="#a855f7" text-anchor="middle" font-weight="600">map back</text>
      <text x="255" y="220" font-size="8" fill="#64748b" text-anchor="middle">(replace edges by paths)</text>

      <!-- Box: T -->
      <rect x="10" y="170" width="190" height="65" rx="14" fill="rgba(59,130,246,.1)" stroke="#3b82f6" stroke-width="2"/>
      <text x="105" y="197" font-size="14" fill="#3b82f6" text-anchor="middle" font-weight="700">Steiner Tree T</text>
      <text x="105" y="218" font-size="11" fill="#94a3b8" text-anchor="middle">cost(T) &#8804; &#945;&#183;OPT(I)</text>

      <!-- Chain of inequalities -->
      <rect x="530" y="15" width="180" height="240" rx="14" fill="rgba(168,85,247,.06)" stroke="rgba(168,85,247,.3)"/>
      <text x="620" y="42" font-size="12" fill="#a855f7" text-anchor="middle" font-weight="700">Chain of Inequalities</text>

      <text x="620" y="78" font-size="14" fill="#e2e8f0" text-anchor="middle">cost(T)</text>
      <text x="620" y="100" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">&#8804;  &nbsp; (mapping back)</text>
      <text x="620" y="122" font-size="14" fill="#e2e8f0" text-anchor="middle">cost'(T')</text>
      <text x="620" y="144" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">&#8804;  &nbsp; (&#945;-approx)</text>
      <text x="620" y="166" font-size="14" fill="#e2e8f0" text-anchor="middle">&#945; &#183; OPT(I')</text>
      <text x="620" y="188" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">&#8804;  &nbsp; (lower bound)</text>
      <text x="620" y="210" font-size="14" fill="#e2e8f0" text-anchor="middle">&#945; &#183; OPT(I)</text>

      <text x="620" y="245" font-size="11" fill="#a855f7" text-anchor="middle" font-weight="700">&#8756; T is an &#945;-approximation!</text>
    </svg>
  </div>
</div>

<div class="card c-green">
  <span class="tag tag-green">Numerical Verification</span>
  <h3>Our Example</h3>
  <ul>
    <li><strong>$OPT(I)$</strong> in $G$: tree $\{a\text{-}b(3),\; b\text{-}c(2),\; b\text{-}d(4)\}$, cost $= 9$</li>
    <li><strong>$OPT(I')$</strong> in $G'$: same tree exists with cost$' = 9 \leq 9$ &ensp;&#10003;</li>
    <li><strong>Approx $T'$</strong> in $G'$: $\{a\text{-}c(5),\; c\text{-}d(6)\}$, cost$' = 11$</li>
    <li><strong>Map back $T$</strong> in $G$: replace edges by shortest paths $\to$ $\{a\text{-}b(3),\; b\text{-}c(2),\; b\text{-}d(4)\}$, cost $= 9 \leq 11$ &ensp;&#10003;</li>
  </ul>
  <div class="math-box">
    $$\underbrace{9}_{\text{cost}(T)} \;\leq\; \underbrace{11}_{\text{cost}'(T')} \;\leq\; \alpha\cdot\underbrace{9}_{OPT(I')} \;\leq\; \alpha\cdot\underbrace{9}_{OPT(I)}$$
  </div>
</div>

<div class="card c-purple">
  <span class="tag tag-purple">Theorem 3.2</span>
  <h3>The Reduction is Approximation-Factor Preserving</h3>
  <div class="math-box">
    $$\text{cost}(T) \;\leq\; \text{cost}'(T') \;\leq\; \alpha \cdot OPT(I') \;\leq\; \alpha \cdot OPT(I)$$
  </div>
  <p>"As a consequence of Theorem 3.2, any approximation factor established for the metric Steiner tree problem carries over to the entire Steiner tree problem."</p>
  <div class="qed">&#9632;</div>
</div>

</div>
</div>

</body>
</html>
"""

def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proof_theorem_3_2.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Generated: {out}")
    webbrowser.open("file:///" + out.replace("\\", "/"))

if __name__ == "__main__":
    main()

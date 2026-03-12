"""
Export all proof diagrams as standalone SVG files for PowerPoint.
Each SVG has a dark background (#0f172a) and embedded fonts.
Run this script — files go into  svgs/  subfolder.
"""
import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svgs")
os.makedirs(DIR, exist_ok=True)

FONT = "'Segoe UI', system-ui, sans-serif"
BG = "#0f172a"

def wrap(inner, w, h, extra_defs=""):
    """Wrap raw SVG content in a standalone SVG with dark bg and font."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>svg {{ font-family: {FONT}; }} text {{ font-family: {FONT}; }}</style>
<rect width="{w}" height="{h}" fill="{BG}" rx="12"/>
{extra_defs}
{inner}
</svg>'''

# ─────────────────────────────────────────────────────────
# 1. Original Graph G
# ─────────────────────────────────────────────────────────
svg1 = wrap('''
<!-- Title -->
<text x="240" y="30" font-size="16" fill="#3b82f6" text-anchor="middle" font-weight="700">Original Graph G = (V, E)</text>
<text x="240" y="52" font-size="11" fill="#94a3b8" text-anchor="middle">V = {a, b, c, d}   R = {a, c, d} (Required)   {b} (Steiner)</text>

<!-- Legend -->
<circle cx="60" cy="72" r="6" fill="#3b82f6"/>
<text x="72" y="76" font-size="10" fill="#93c5fd">Required</text>
<circle cx="150" cy="72" r="6" fill="#475569"/>
<text x="162" y="76" font-size="10" fill="#94a3b8">Steiner</text>

<!-- Edges -->
<line x1="100" y1="130" x2="260" y2="100" stroke="#475569" stroke-width="2.8"/>
<line x1="260" y1="100" x2="120" y2="270" stroke="#475569" stroke-width="2.8"/>
<line x1="260" y1="100" x2="380" y2="240" stroke="#475569" stroke-width="2.8"/>
<line x1="100" y1="130" x2="120" y2="270" stroke="#475569" stroke-width="2.8"/>
<line x1="120" y1="270" x2="380" y2="240" stroke="#475569" stroke-width="2.8"/>

<!-- Cost labels -->
<rect x="163" y="98" width="30" height="22" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
<text x="178" y="114" font-size="14" fill="#f59e0b" text-anchor="middle" font-weight="700">3</text>
<rect x="172" y="178" width="30" height="22" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
<text x="187" y="194" font-size="14" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>
<rect x="308" y="162" width="30" height="22" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
<text x="323" y="178" font-size="14" fill="#f59e0b" text-anchor="middle" font-weight="700">4</text>
<rect x="86" y="194" width="30" height="22" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
<text x="101" y="210" font-size="14" fill="#f59e0b" text-anchor="middle" font-weight="700">7</text>
<rect x="232" y="266" width="30" height="22" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
<text x="247" y="282" font-size="14" fill="#f59e0b" text-anchor="middle" font-weight="700">8</text>

<!-- Vertices -->
<circle cx="100" cy="130" r="24" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="100" y="137" font-size="18" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="260" cy="100" r="24" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text x="260" y="107" font-size="18" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="120" cy="270" r="24" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="120" y="277" font-size="18" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="380" cy="240" r="24" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="380" y="247" font-size="18" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<text x="240" y="320" font-size="11" fill="#64748b" text-anchor="middle" font-style="italic">5 edges. No direct edge between a and d.</text>
''', 480, 340)


# ─────────────────────────────────────────────────────────
# 2. G → G' Transformation (side by side)
# ─────────────────────────────────────────────────────────
svg2_defs = '''<defs>
<filter id="gl"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="arr" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#94a3b8"/></marker>
</defs>'''

svg2 = wrap('''
<!-- LEFT: Original G -->
<text x="155" y="30" font-size="15" fill="#3b82f6" text-anchor="middle" font-weight="700">Original G (5 edges)</text>
<line x1="70" y1="100" x2="210" y2="70" stroke="#475569" stroke-width="2.5"/>
<line x1="210" y1="70" x2="95" y2="220" stroke="#475569" stroke-width="2.5"/>
<line x1="210" y1="70" x2="285" y2="195" stroke="#475569" stroke-width="2.5"/>
<line x1="70" y1="100" x2="95" y2="220" stroke="#475569" stroke-width="2.5"/>
<line x1="95" y1="220" x2="285" y2="195" stroke="#475569" stroke-width="2.5"/>
<text x="130" y="76" font-size="12" fill="#f59e0b" font-weight="700">3</text>
<text x="138" y="144" font-size="12" fill="#f59e0b" font-weight="700">2</text>
<text x="254" y="128" font-size="12" fill="#f59e0b" font-weight="700">4</text>
<text x="62" y="164" font-size="12" fill="#f59e0b" font-weight="700">7</text>
<text x="188" y="220" font-size="12" fill="#f59e0b" font-weight="700">8</text>
<circle cx="70" cy="100" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="70" y="107" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="210" cy="70" r="18" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text x="210" y="77" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="95" cy="220" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="95" y="227" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="285" cy="195" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="285" y="202" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<!-- Arrow -->
<line x1="340" y1="145" x2="450" y2="145" stroke="#94a3b8" stroke-width="2.8" marker-end="url(#arr)"/>
<text x="395" y="128" font-size="11" fill="#f59e0b" text-anchor="middle" font-weight="600">compute shortest</text>
<text x="395" y="143" font-size="11" fill="#f59e0b" text-anchor="middle" font-weight="600">path for every pair</text>
<text x="395" y="170" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">make complete graph</text>

<!-- RIGHT: G' complete -->
<text x="680" y="30" font-size="15" fill="#22c55e" text-anchor="middle" font-weight="700">Metric Closure G' (6 edges — complete)</text>
<!-- a(490,120) b(660,75) c(530,260) d(790,230) -->
<line x1="490" y1="120" x2="660" y2="75"  stroke="#22c55e" stroke-width="2.5" opacity=".6"/>
<line x1="490" y1="120" x2="530" y2="260" stroke="#22c55e" stroke-width="2.5" opacity=".6"/>
<line x1="490" y1="120" x2="790" y2="230" stroke="#22c55e" stroke-width="2.5" stroke-dasharray="7,3"/>
<line x1="660" y1="75"  x2="530" y2="260" stroke="#22c55e" stroke-width="2.5" opacity=".6"/>
<line x1="660" y1="75"  x2="790" y2="230" stroke="#22c55e" stroke-width="2.5" opacity=".6"/>
<line x1="530" y1="260" x2="790" y2="230" stroke="#22c55e" stroke-width="2.5" opacity=".6"/>

<!-- Cost labels G' -->
<rect x="558" y="80" width="28" height="20" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="572" y="95" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">3</text>
<rect x="490" y="184" width="28" height="20" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="504" y="199" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">5</text>
<rect x="628" y="168" width="28" height="20" rx="4" fill="#0f172a" stroke="#ef4444" stroke-width="1.4"/>
<text x="642" y="183" font-size="13" fill="#ef4444" text-anchor="middle" font-weight="700">7</text>
<text x="674" y="196" font-size="9" fill="#ef4444" font-style="italic">new!</text>
<rect x="578" y="160" width="28" height="20" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="592" y="175" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">2</text>
<rect x="718" y="142" width="28" height="20" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="732" y="157" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">4</text>
<rect x="644" y="256" width="28" height="20" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="658" y="271" font-size="13" fill="#22c55e" text-anchor="middle" font-weight="700">6</text>

<!-- Vertices G' -->
<circle cx="490" cy="120" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
<text x="490" y="127" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="660" cy="75"  r="20" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text x="660" y="82"  font-size="16" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="530" cy="260" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
<text x="530" y="267" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="790" cy="230" r="20" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5" filter="url(#gl)"/>
<text x="790" y="237" font-size="16" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<!-- Bottom note -->
<rect x="460" y="292" width="370" height="26" rx="7" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.25)"/>
<text x="645" y="310" font-size="11" fill="#22c55e" text-anchor="middle" font-weight="600">Triangle inequality holds: cost'(u,w) ≤ cost'(u,v) + cost'(v,w)</text>
''', 880, 330, svg2_defs)


# ─────────────────────────────────────────────────────────
# 3. OPT(I') ≤ OPT(I)  (lower bound)
# ─────────────────────────────────────────────────────────
svg3_defs = '<defs><marker id="a1" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#94a3b8"/></marker></defs>'
svg3 = wrap('''
<text x="400" y="28" font-size="16" fill="#e2e8f0" text-anchor="middle" font-weight="700">OPT(I') ≤ OPT(I)</text>

<!-- LEFT: OPT in G -->
<text x="150" y="62" font-size="14" fill="#3b82f6" text-anchor="middle" font-weight="700">OPT in G = {a-b, b-c, b-d}</text>
<line x1="70" y1="120" x2="180" y2="95" stroke="#3b82f6" stroke-width="4"/>
<line x1="180" y1="95" x2="100" y2="220" stroke="#3b82f6" stroke-width="4"/>
<line x1="180" y1="95" x2="270" y2="195" stroke="#3b82f6" stroke-width="4"/>
<text x="114" y="98" font-size="13" fill="#f59e0b" font-weight="700">3</text>
<text x="126" y="160" font-size="13" fill="#f59e0b" font-weight="700">2</text>
<text x="232" y="142" font-size="13" fill="#f59e0b" font-weight="700">4</text>
<circle cx="70" cy="120" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="70" y="127" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="180" cy="95" r="18" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text x="180" y="102" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="100" cy="220" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="100" y="227" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="270" cy="195" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="270" y="202" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">d</text>
<rect x="50" y="250" width="250" height="30" rx="7" fill="rgba(59,130,246,.12)" stroke="rgba(59,130,246,.3)"/>
<text x="175" y="270" font-size="14" fill="#3b82f6" text-anchor="middle" font-weight="700">cost = 3 + 2 + 4 = 9</text>

<!-- Arrow -->
<line x1="350" y1="155" x2="460" y2="155" stroke="#94a3b8" stroke-width="2.5" marker-end="url(#a1)"/>
<text x="405" y="140" font-size="11" fill="#94a3b8" text-anchor="middle" font-style="italic">same edges exist in G'</text>
<text x="405" y="154" font-size="11" fill="#94a3b8" text-anchor="middle" font-style="italic">with cost' ≤ cost</text>

<!-- RIGHT: Same tree in G' -->
<text x="620" y="62" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">Same tree in G'</text>
<line x1="520" y1="120" x2="630" y2="95" stroke="#22c55e" stroke-width="4"/>
<line x1="630" y1="95" x2="550" y2="220" stroke="#22c55e" stroke-width="4"/>
<line x1="630" y1="95" x2="720" y2="195" stroke="#22c55e" stroke-width="4"/>
<text x="564" y="98" font-size="13" fill="#22c55e" font-weight="700">3</text>
<text x="576" y="160" font-size="13" fill="#22c55e" font-weight="700">2</text>
<text x="682" y="142" font-size="13" fill="#22c55e" font-weight="700">4</text>
<text x="598" y="92" font-size="9" fill="#94a3b8">≤ 3 ✓</text>
<text x="608" y="166" font-size="9" fill="#94a3b8">≤ 2 ✓</text>
<text x="700" y="149" font-size="9" fill="#94a3b8">≤ 4 ✓</text>
<circle cx="520" cy="120" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="520" y="127" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="630" cy="95" r="18" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text x="630" y="102" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="550" cy="220" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="550" y="227" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="720" cy="195" r="18" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text x="720" y="202" font-size="15" fill="#fff" text-anchor="middle" font-weight="700">d</text>
<rect x="500" y="250" width="250" height="30" rx="7" fill="rgba(34,197,94,.12)" stroke="rgba(34,197,94,.3)"/>
<text x="625" y="270" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">cost' = 3+2+4 = 9 ≤ 9 ✓</text>

<!-- Bottom box -->
<rect x="200" y="295" width="400" height="28" rx="7" fill="rgba(245,158,11,.1)" stroke="rgba(245,158,11,.25)"/>
<text x="400" y="314" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="700">Every edge: cost'(e) ≤ cost(e)  ⟹  OPT(I') ≤ OPT(I)</text>
''', 800, 340, svg3_defs)


# ─────────────────────────────────────────────────────────
# 4. Approx tree T' in G'
# ─────────────────────────────────────────────────────────
svg4 = wrap('''
<text x="280" y="30" font-size="16" fill="#ef4444" text-anchor="middle" font-weight="700">Approximate Tree T' in G' (connects a, c, d)</text>

<line x1="80" y1="120" x2="270" y2="120" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>
<line x1="270" y1="120" x2="470" y2="120" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>

<rect x="155" y="85" width="36" height="24" rx="5" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
<text x="173" y="103" font-size="15" fill="#ef4444" text-anchor="middle" font-weight="700">5</text>
<rect x="352" y="85" width="36" height="24" rx="5" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
<text x="370" y="103" font-size="15" fill="#ef4444" text-anchor="middle" font-weight="700">6</text>

<circle cx="80"  cy="120" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="80"  y="127" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="270" cy="120" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="270" y="127" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="470" cy="120" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="470" y="127" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<rect x="155" y="160" width="240" height="32" rx="8" fill="rgba(239,68,68,.12)" stroke="rgba(239,68,68,.35)"/>
<text x="275" y="182" font-size="15" fill="#ef4444" text-anchor="middle" font-weight="700">cost'(T') = 5 + 6 = 11</text>
''', 560, 210)


# ─────────────────────────────────────────────────────────
# 5. Edge replacement (mapping back)
# ─────────────────────────────────────────────────────────
svg5_defs = '<defs><marker id="a2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>'
svg5 = wrap('''
<text x="400" y="26" font-size="15" fill="#a855f7" text-anchor="middle" font-weight="700">Replace Each Edge of T' by Its Shortest Path in G</text>

<!-- Row 1: a-c → a→b→c -->
<rect x="12" y="44" width="230" height="80" rx="10" fill="rgba(239,68,68,.06)" stroke="rgba(239,68,68,.25)"/>
<text x="127" y="66" font-size="12" fill="#ef4444" text-anchor="middle" font-weight="700">Edge (a, c) in T'  —  cost' = 5</text>
<line x1="46" y1="96" x2="198" y2="96" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
<circle cx="46"  cy="96" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="46"  y="101" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="198" cy="96" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="198" y="101" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">c</text>

<line x1="256" y1="84" x2="340" y2="84" stroke="#94a3b8" stroke-width="2" marker-end="url(#a2)"/>
<text x="298" y="76" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">replace</text>

<rect x="354" y="44" width="430" height="80" rx="10" fill="rgba(59,130,246,.06)" stroke="rgba(59,130,246,.25)"/>
<text x="569" y="66" font-size="12" fill="#3b82f6" text-anchor="middle" font-weight="700">Shortest path a → b → c in G  —  cost = 3 + 2 = 5</text>
<line x1="400" y1="96" x2="569" y2="96" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
<line x1="569" y1="96" x2="738" y2="96" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="400" cy="96" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="400" y="101" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="569" cy="96" r="14" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
<text   x="569" y="101" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="738" cy="96" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="738" y="101" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<text x="484" y="89" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="700">3</text>
<text x="653" y="89" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>

<!-- Row 2: c-d → c→b→d -->
<rect x="12" y="148" width="230" height="80" rx="10" fill="rgba(239,68,68,.06)" stroke="rgba(239,68,68,.25)"/>
<text x="127" y="170" font-size="12" fill="#ef4444" text-anchor="middle" font-weight="700">Edge (c, d) in T'  —  cost' = 6</text>
<line x1="46" y1="200" x2="198" y2="200" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
<circle cx="46"  cy="200" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="46"  y="205" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="198" cy="200" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="198" y="205" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<line x1="256" y1="188" x2="340" y2="188" stroke="#94a3b8" stroke-width="2" marker-end="url(#a2)"/>
<text x="298" y="180" font-size="10" fill="#94a3b8" text-anchor="middle" font-style="italic">replace</text>

<rect x="354" y="148" width="430" height="80" rx="10" fill="rgba(59,130,246,.06)" stroke="rgba(59,130,246,.25)"/>
<text x="569" y="170" font-size="12" fill="#3b82f6" text-anchor="middle" font-weight="700">Shortest path c → b → d in G  —  cost = 2 + 4 = 6</text>
<line x1="400" y1="200" x2="569" y2="200" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
<line x1="569" y1="200" x2="738" y2="200" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="400" cy="200" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="400" y="205" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="569" cy="200" r="14" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
<text   x="569" y="205" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="738" cy="200" r="14" fill="#3b82f6" stroke="#93c5fd" stroke-width="2"/>
<text   x="738" y="205" font-size="12" fill="#fff" text-anchor="middle" font-weight="700">d</text>
<text x="484" y="193" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="700">2</text>
<text x="653" y="193" font-size="12" fill="#f59e0b" text-anchor="middle" font-weight="700">4</text>

<!-- Bottom note -->
<rect x="50" y="242" width="700" height="28" rx="7" fill="rgba(168,85,247,.1)" stroke="rgba(168,85,247,.3)"/>
<text x="400" y="262" font-size="12" fill="#a855f7" text-anchor="middle" font-weight="700">Union: {a–b(3), b–c(2)} ∪ {c–b(2), b–d(4)} → edge b–c appears twice → remove duplicate</text>
''', 800, 284, svg5_defs)


# ─────────────────────────────────────────────────────────
# 6. Final Steiner Tree T in G
# ─────────────────────────────────────────────────────────
svg6 = wrap('''
<text x="280" y="30" font-size="16" fill="#22c55e" text-anchor="middle" font-weight="700">Final Steiner Tree T in G</text>
<text x="280" y="52" font-size="11" fill="#94a3b8" text-anchor="middle">Remove duplicates / cycles → obtain tree T</text>

<line x1="100" y1="140" x2="280" y2="105" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
<line x1="280" y1="105" x2="170" y2="230" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
<line x1="280" y1="105" x2="440" y2="200" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>

<text x="176" y="112" font-size="15" fill="#f59e0b" font-weight="700">3</text>
<text x="208" y="172" font-size="15" fill="#f59e0b" font-weight="700">2</text>
<text x="368" y="148" font-size="15" fill="#f59e0b" font-weight="700">4</text>

<circle cx="100" cy="140" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="100" y="147" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">a</text>
<circle cx="280" cy="105" r="22" fill="#475569" stroke="#94a3b8" stroke-width="2.5"/>
<text   x="280" y="112" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">b</text>
<circle cx="170" cy="230" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="170" y="237" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">c</text>
<circle cx="440" cy="200" r="22" fill="#3b82f6" stroke="#93c5fd" stroke-width="2.5"/>
<text   x="440" y="207" font-size="17" fill="#fff" text-anchor="middle" font-weight="700">d</text>

<rect x="110" y="266" width="340" height="32" rx="8" fill="rgba(34,197,94,.12)" stroke="rgba(34,197,94,.35)"/>
<text x="280" y="288" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">cost(T) = 3 + 2 + 4 = 9  ≤  11 = cost'(T')  ✓</text>
''', 560, 314)


# ─────────────────────────────────────────────────────────
# 7. Reduction Pipeline + Chain of Inequalities
# ─────────────────────────────────────────────────────────
svg7_defs = '''<defs>
<marker id="a4" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#a855f7"/></marker>
<marker id="a5" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
</defs>'''
svg7 = wrap('''
<text x="400" y="28" font-size="16" fill="#e2e8f0" text-anchor="middle" font-weight="700">Approximation-Factor Preserving Reduction</text>

<!-- Box I -->
<rect x="20" y="55" width="210" height="90" rx="14" fill="rgba(59,130,246,.1)" stroke="#3b82f6" stroke-width="2"/>
<text x="125" y="85" font-size="16" fill="#3b82f6" text-anchor="middle" font-weight="700">Instance I</text>
<text x="125" y="106" font-size="12" fill="#94a3b8" text-anchor="middle">General Graph G</text>
<text x="125" y="125" font-size="11" fill="#64748b" text-anchor="middle">V={a,b,c,d}, R={a,c,d}</text>

<!-- Arrow right -->
<line x1="240" y1="100" x2="340" y2="100" stroke="#a855f7" stroke-width="2.8" marker-end="url(#a4)"/>
<text x="290" y="88" font-size="10" fill="#a855f7" text-anchor="middle" font-weight="700">metric closure</text>
<text x="290" y="118" font-size="9" fill="#64748b" text-anchor="middle">(poly time)</text>

<!-- Box I' -->
<rect x="350" y="55" width="210" height="90" rx="14" fill="rgba(34,197,94,.1)" stroke="#22c55e" stroke-width="2"/>
<text x="455" y="85" font-size="16" fill="#22c55e" text-anchor="middle" font-weight="700">Instance I'</text>
<text x="455" y="106" font-size="12" fill="#94a3b8" text-anchor="middle">Metric Graph G'</text>
<text x="455" y="125" font-size="11" fill="#64748b" text-anchor="middle">Complete, triangle ineq.</text>

<!-- Arrow down -->
<line x1="455" y1="155" x2="455" y2="205" stroke="#22c55e" stroke-width="2.8" marker-end="url(#a5)"/>
<text x="518" y="185" font-size="10" fill="#22c55e" text-anchor="middle" font-weight="700">α-approx alg.</text>

<!-- Box T' -->
<rect x="350" y="215" width="210" height="70" rx="14" fill="rgba(239,68,68,.1)" stroke="#ef4444" stroke-width="2"/>
<text x="455" y="245" font-size="15" fill="#ef4444" text-anchor="middle" font-weight="700">Approx Tree T'</text>
<text x="455" y="268" font-size="12" fill="#94a3b8" text-anchor="middle">cost'(T') ≤ α·OPT(I')</text>

<!-- Arrow left -->
<line x1="340" y1="250" x2="240" y2="250" stroke="#a855f7" stroke-width="2.8" marker-end="url(#a4)"/>
<text x="290" y="238" font-size="10" fill="#a855f7" text-anchor="middle" font-weight="700">map back</text>
<text x="290" y="270" font-size="9" fill="#64748b" text-anchor="middle">(replace edges by paths)</text>

<!-- Box T -->
<rect x="20" y="215" width="210" height="70" rx="14" fill="rgba(59,130,246,.1)" stroke="#3b82f6" stroke-width="2"/>
<text x="125" y="245" font-size="15" fill="#3b82f6" text-anchor="middle" font-weight="700">Steiner Tree T</text>
<text x="125" y="268" font-size="12" fill="#94a3b8" text-anchor="middle">cost(T) ≤ α·OPT(I)</text>

<!-- Chain of inequalities -->
<rect x="590" y="48" width="195" height="250" rx="14" fill="rgba(168,85,247,.06)" stroke="rgba(168,85,247,.3)"/>
<text x="687" y="78" font-size="13" fill="#a855f7" text-anchor="middle" font-weight="700">Chain of Inequalities</text>

<text x="687" y="115" font-size="15" fill="#e2e8f0" text-anchor="middle">cost(T)</text>
<text x="687" y="140" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">≤  (mapping back)</text>
<text x="687" y="163" font-size="15" fill="#e2e8f0" text-anchor="middle">cost'(T')</text>
<text x="687" y="188" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">≤  (α-approx)</text>
<text x="687" y="211" font-size="15" fill="#e2e8f0" text-anchor="middle">α · OPT(I')</text>
<text x="687" y="236" font-size="14" fill="#22c55e" text-anchor="middle" font-weight="700">≤  (lower bound)</text>
<text x="687" y="259" font-size="15" fill="#e2e8f0" text-anchor="middle">α · OPT(I)</text>

<text x="687" y="290" font-size="12" fill="#a855f7" text-anchor="middle" font-weight="700">∴ T is an α-approximation!</text>
''', 800, 310, svg7_defs)


# ─────────────────────────────────────────────────────────
# Write all files
# ─────────────────────────────────────────────────────────
files = {
    "01_original_graph_G.svg": svg1,
    "02_G_to_metric_closure_G_prime.svg": svg2,
    "03_lower_bound_OPT.svg": svg3,
    "04_approx_tree_T_prime.svg": svg4,
    "05_edge_replacement_mapping_back.svg": svg5,
    "06_final_steiner_tree_T.svg": svg6,
    "07_reduction_pipeline.svg": svg7,
}

for name, content in files.items():
    path = os.path.join(DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {name}")

print(f"\nDone! {len(files)} SVG files saved in:\n  {DIR}")
print("\nTo use in PowerPoint: Insert → Pictures → select the .svg file")

"""
Generate PowerPoint presentation for Proof of Theorem 3.2
(Reduction from Steiner Tree to Metric Steiner Tree — Vazirani Ch. 3)

Draws all diagrams with matplotlib + networkx. No external SVG conversion needed.
"""

import os, io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_PPT = os.path.join(BASE, "Proof_Theorem_3_2_white.pptx")

# ── PPT colours (white theme) ──
BG_PPT   = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG  = RGBColor(0xF1, 0xF5, 0xF9)
TITLE_C  = RGBColor(0x0F, 0x17, 0x2A)
C_BLUE   = RGBColor(0x25, 0x63, 0xEB)
C_GREEN  = RGBColor(0x16, 0xA3, 0x4A)
C_RED    = RGBColor(0xDC, 0x26, 0x26)
C_ORANGE = RGBColor(0xD9, 0x77, 0x06)
C_PURPLE = RGBColor(0x7C, 0x3A, 0xED)
C_MUTED  = RGBColor(0x64, 0x74, 0x8B)
TEXT_CLR = RGBColor(0x33, 0x41, 0x55)

# ── matplotlib colours (white theme) ──
BLUE   = '#2563eb'
GRAY_V = '#64748b'
GREEN  = '#16a34a'
RED    = '#dc2626'
ORANGE = '#d97706'
PURPLE = '#7c3aed'
MUTED  = '#64748b'
EDGE_C = '#94a3b8'
BG_FIG = '#ffffff'
CARD_F = '#f1f5f9'
TEXT_D = '#1e293b'

# ── graph data ──
pos = {'a': (0, 1.2), 'b': (1.5, 2), 'c': (0.5, 0), 'd': (2.8, 0.3)}
edges_G = [('a','b',3), ('b','c',2), ('b','d',4), ('a','c',7), ('c','d',8)]
edges_Gp = [('a','b',3), ('a','c',5), ('a','d',7), ('b','c',2), ('b','d',4), ('c','d',6)]
required = {'a','c','d'}
tree_Tp = [('a','c',5), ('c','d',6)]
tree_T = [('a','b',3), ('b','c',2), ('b','d',4)]


def fig_to_png(fig, dpi=200):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.15)
    buf.seek(0)
    plt.close(fig)
    return buf.read()


def draw_graph(ax, positions, edges, title, edge_color=EDGE_C, new_edge=None):
    ax.set_facecolor(CARD_F)
    ax.set_xlim(-0.6, 3.5)
    ax.set_ylim(-0.6, 2.7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, color=TEXT_D, fontsize=14, fontweight='bold', pad=10)

    for u, v, w in edges:
        x = [positions[u][0], positions[v][0]]
        y = [positions[u][1], positions[v][1]]
        ec = edge_color
        ls = '-'
        if new_edge and (u, v) == new_edge:
            ls = '--'
            ec = RED
        ax.plot(x, y, color=ec, linewidth=2.5, linestyle=ls, zorder=1)
        mx, my = (x[0]+x[1])/2, (y[0]+y[1])/2
        dx, dy = y[1]-y[0], -(x[1]-x[0])
        norm = max(np.sqrt(dx**2 + dy**2), 0.01)
        ox, oy = dx/norm * 0.18, dy/norm * 0.18
        ax.text(mx+ox, my+oy, str(w), fontsize=11, color=ORANGE,
                fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=ORANGE, lw=0.8))

    for v_name, (x, y) in positions.items():
        is_req = v_name in required
        fc = BLUE if is_req else GRAY_V
        ec = '#1d4ed8' if is_req else '#475569'
        circle = plt.Circle((x, y), 0.22, facecolor=fc, edgecolor=ec,
                            linewidth=2.5, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, v_name, fontsize=14, color='white', fontweight='bold',
                ha='center', va='center', zorder=6)


# ──────────────────────────────────────
#  7 FIGURES
# ──────────────────────────────────────

def make_fig1():
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    fig.patch.set_facecolor(BG_FIG)
    draw_graph(ax, pos, edges_G, "Original Graph G  —  V = {a,b,c,d},  R = {a,c,d}")
    handles = [
        mpatches.Patch(color=BLUE, label='Required vertex'),
        mpatches.Patch(color=GRAY_V, label='Steiner vertex'),
        mpatches.Patch(color=ORANGE, label='Edge cost'),
    ]
    ax.legend(handles=handles, loc='lower center', ncol=3, fontsize=8,
              facecolor='white', edgecolor=EDGE_C, labelcolor=TEXT_D,
              bbox_to_anchor=(0.5, -0.02))
    ax.text(1.5, -0.5, "5 edges.  No direct edge between a and d.",
            fontsize=9, color=MUTED, ha='center', style='italic')
    return fig_to_png(fig)


def make_fig2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor(BG_FIG)
    draw_graph(ax1, pos, edges_G, "Original G (5 edges)")
    draw_graph(ax2, pos, edges_Gp, "Metric Closure G' (6 edges — complete)",
               edge_color=GREEN, new_edge=('a','d'))
    fig.text(0.48, 0.55, "→", fontsize=30, color=MUTED, ha='center', va='center')
    fig.text(0.48, 0.45, "compute shortest\npath for every pair",
             fontsize=9, color=ORANGE, ha='center', va='center')
    fig.text(0.75, 0.06, "Triangle inequality: cost'(u,w) ≤ cost'(u,v) + cost'(v,w)",
             fontsize=9, color=GREEN, ha='center',
             bbox=dict(boxstyle='round,pad=0.3', fc='#f0fdf4', ec=GREEN, lw=0.8))
    return fig_to_png(fig)


def make_fig3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor(BG_FIG)
    draw_graph(ax1, pos, tree_T, "OPT in G = {a-b, b-c, b-d}", edge_color=BLUE)
    ax1.text(1.5, -0.5, "cost = 3 + 2 + 4 = 9", fontsize=12, color=BLUE,
             ha='center', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#eff6ff', ec=BLUE, lw=0.8))
    draw_graph(ax2, pos, tree_T, "Same tree in G'", edge_color=GREEN)
    ax2.text(1.5, -0.5, "cost' = 3 + 2 + 4 = 9 ≤ 9  ✓", fontsize=12, color=GREEN,
             ha='center', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#f0fdf4', ec=GREEN, lw=0.8))
    fig.text(0.48, 0.55, "→", fontsize=30, color=MUTED, ha='center', va='center')
    fig.text(0.48, 0.45, "same edges exist\nin G' with cost' ≤ cost",
             fontsize=9, color=MUTED, ha='center', va='center')
    fig.text(0.5, 0.06, "Every edge in G exists in G' with cost' ≤ cost  ⟹  OPT(I') ≤ OPT(I)",
             fontsize=10, color=ORANGE, ha='center', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#fffbeb', ec=ORANGE, lw=0.8))
    return fig_to_png(fig)


def make_fig4():
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    fig.patch.set_facecolor(BG_FIG)
    ax.set_facecolor(CARD_F)
    pos_linear = {'a': (0, 0), 'c': (2, 0), 'd': (4, 0)}
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-1.0, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Approximate Tree T' in G'  (connects a, c, d)", color=TEXT_D,
                 fontsize=14, fontweight='bold', pad=10)
    for u, v, w in tree_Tp:
        x = [pos_linear[u][0], pos_linear[v][0]]
        y = [pos_linear[u][1], pos_linear[v][1]]
        ax.plot(x, y, color=RED, linewidth=5, zorder=1, solid_capstyle='round')
        mx = (x[0]+x[1])/2
        ax.text(mx, 0.35, str(w), fontsize=14, color=RED, fontweight='bold',
                ha='center', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=RED, lw=1))
    for v_name, (x, y) in pos_linear.items():
        c = plt.Circle((x, y), 0.25, facecolor=BLUE, edgecolor='#1d4ed8',
                        linewidth=2.5, zorder=5)
        ax.add_patch(c)
        ax.text(x, y, v_name, fontsize=16, color='white', fontweight='bold',
                ha='center', va='center', zorder=6)
    ax.text(2, -0.7, "cost'(T') = 5 + 6 = 11", fontsize=14, color=RED,
            ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#fef2f2', ec=RED, lw=1))
    return fig_to_png(fig)


def make_fig5():
    fig, axes = plt.subplots(2, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})
    fig.patch.set_facecolor(BG_FIG)

    def draw_row(row, u, v, w, path_nodes, path_weights, path_colors):
        ax_left = axes[row, 0]
        ax_left.set_facecolor('#fef2f2')
        ax_left.set_xlim(-0.5, 2.5)
        ax_left.set_ylim(-0.5, 0.8)
        ax_left.set_aspect('equal')
        ax_left.axis('off')
        ax_left.set_title(f"Edge ({u},{v}) in T' — cost'={w}", color=RED, fontsize=11, fontweight='bold')
        ax_left.plot([0, 2], [0, 0], color=RED, linewidth=4, solid_capstyle='round')
        for vn, vx in [(u, 0), (v, 2)]:
            c = plt.Circle((vx, 0), 0.2, facecolor=BLUE, edgecolor='#1d4ed8', lw=2, zorder=5)
            ax_left.add_patch(c)
            ax_left.text(vx, 0, vn, fontsize=12, color='white', fontweight='bold', ha='center', va='center', zorder=6)

        ax_right = axes[row, 1]
        ax_right.set_facecolor('#eff6ff')
        n = len(path_nodes)
        ax_right.set_xlim(-0.5, (n-1)*2 + 0.5)
        ax_right.set_ylim(-0.5, 0.8)
        ax_right.set_aspect('equal')
        ax_right.axis('off')
        path_str = '→'.join(path_nodes)
        weight_str = '+'.join(str(w) for w in path_weights)
        total = sum(path_weights)
        ax_right.set_title(f"Shortest path {path_str} in G — cost = {weight_str} = {total}",
                          color=BLUE, fontsize=11, fontweight='bold')
        for i in range(n - 1):
            ax_right.plot([i*2, (i+1)*2], [0, 0], color=BLUE, linewidth=3, solid_capstyle='round')
            ax_right.text(i*2+1, 0.25, str(path_weights[i]), fontsize=11, color=ORANGE, fontweight='bold', ha='center')
        for i, vn in enumerate(path_nodes):
            vc = path_colors[i]
            ec = '#1d4ed8' if vc == BLUE else '#475569'
            c = plt.Circle((i*2, 0), 0.2, facecolor=vc, edgecolor=ec, lw=2, zorder=5)
            ax_right.add_patch(c)
            ax_right.text(i*2, 0, vn, fontsize=12, color='white', fontweight='bold', ha='center', va='center', zorder=6)

    draw_row(0, 'a', 'c', 5, ['a', 'b', 'c'], [3, 2], [BLUE, GRAY_V, BLUE])
    draw_row(1, 'c', 'd', 6, ['c', 'b', 'd'], [2, 4], [BLUE, GRAY_V, BLUE])

    fig.text(0.5, 0.02,
             "Union: {a-b(3), b-c(2)} ∪ {c-b(2), b-d(4)} = {a-b, b-c, b-d}  (duplicate b-c removed)",
             fontsize=10, color=PURPLE, ha='center', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#f5f3ff', ec=PURPLE, lw=0.8))

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    return fig_to_png(fig)


def make_fig6():
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    fig.patch.set_facecolor(BG_FIG)
    draw_graph(ax, pos, tree_T, "Final Steiner Tree T in G", edge_color=GREEN)
    ax.text(1.5, -0.5, "cost(T) = 3 + 2 + 4 = 9  ≤  11 = cost'(T')  ✓",
            fontsize=12, color=GREEN, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#f0fdf4', ec=GREEN, lw=1))
    return fig_to_png(fig)


def make_fig7():
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    fig.patch.set_facecolor(BG_FIG)
    ax.set_facecolor(BG_FIG)
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-0.5, 6)
    ax.axis('off')
    ax.set_title("Approximation-Factor Preserving Reduction", color=TEXT_D,
                 fontsize=16, fontweight='bold', pad=15)

    boxes = [
        (0.5, 3.5, 3.5, 1.8, BLUE, "Instance I\nGeneral Graph G\nV={a,b,c,d}, R={a,c,d}"),
        (5.5, 3.5, 3.5, 1.8, GREEN, "Instance I'\nMetric Graph G'\nComplete, triangle ineq."),
        (5.5, 0.5, 3.5, 1.5, RED, "Approx Tree T'\ncost'(T') ≤ α·OPT(I')"),
        (0.5, 0.5, 3.5, 1.5, BLUE, "Steiner Tree T\ncost(T) ≤ α·OPT(I)"),
    ]

    for x, y, w, h, color, text in boxes:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              facecolor=color+'15', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            fy = y + h - 0.4 - i * 0.45
            fs = 13 if i == 0 else 10
            fw = 'bold' if i == 0 else 'normal'
            fc = color if i == 0 else '#475569'
            ax.text(x + w/2, fy, line, fontsize=fs, color=fc, fontweight=fw,
                    ha='center', va='center')

    arrow_kw = dict(arrowstyle='->,head_width=0.3,head_length=0.15', lw=2.5)
    ax.annotate('', xy=(5.5, 4.4), xytext=(4.0, 4.4),
                arrowprops=dict(**arrow_kw, color=PURPLE))
    ax.text(4.75, 4.85, "metric closure", fontsize=10, color=PURPLE,
            ha='center', fontweight='bold')
    ax.text(4.75, 4.55, "(poly time)", fontsize=8, color=MUTED, ha='center')

    ax.annotate('', xy=(7.25, 2.0), xytext=(7.25, 3.5),
                arrowprops=dict(**arrow_kw, color=GREEN))
    ax.text(8.2, 2.75, "α-approx\nalgorithm", fontsize=10, color=GREEN,
            ha='center', fontweight='bold')

    ax.annotate('', xy=(4.0, 1.25), xytext=(5.5, 1.25),
                arrowprops=dict(**arrow_kw, color=PURPLE))
    ax.text(4.75, 1.7, "map back", fontsize=10, color=PURPLE,
            ha='center', fontweight='bold')
    ax.text(4.75, 0.85, "(replace edges by paths)", fontsize=8, color=MUTED, ha='center')

    rect_chain = FancyBboxPatch((10, 0.2), 3.5, 5.5, boxstyle="round,pad=0.15",
                                 facecolor='#f5f3ff', edgecolor=PURPLE+'80', linewidth=1.5)
    ax.add_patch(rect_chain)
    ax.text(11.75, 5.3, "Chain of Inequalities", fontsize=12, color=PURPLE,
            ha='center', fontweight='bold')

    chain = [
        ("cost(T)", TEXT_D),
        ("≤   (mapping back)", GREEN),
        ("cost'(T')", TEXT_D),
        ("≤   (α-approximation)", GREEN),
        ("α · OPT(I')", TEXT_D),
        ("≤   (lower bound)", GREEN),
        ("α · OPT(I)", TEXT_D),
    ]
    for i, (text, color) in enumerate(chain):
        ax.text(11.75, 4.7 - i * 0.6, text, fontsize=13 if '≤' not in text else 11,
                color=color, fontweight='bold', ha='center')

    ax.text(11.75, 0.5, "∴ T is an α-approximation!", fontsize=12, color=PURPLE,
            ha='center', fontweight='bold')
    return fig_to_png(fig)


# ══════════════════════════════════════════════════════
#  PPT HELPERS
# ══════════════════════════════════════════════════════

def set_slide_bg(slide, color=BG_PPT):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=TEXT_CLR, bold=False, alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = "Segoe UI"
    p.alignment = alignment
    return tf


def add_para(tf, text, font_size=14, color=TEXT_CLR, bold=False,
             alignment=PP_ALIGN.LEFT):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = "Segoe UI"
    p.alignment = alignment
    p.space_before = Pt(3)
    p.space_after = Pt(2)
    return p


def add_image_centered(slide, png_bytes, top, max_w=Inches(10), max_h=Inches(4.5)):
    from PIL import Image
    img = Image.open(io.BytesIO(png_bytes))
    w_px, h_px = img.size
    ppi = 200
    w_emu = int(w_px * 914400 / ppi)
    h_emu = int(h_px * 914400 / ppi)
    scale = min(max_w / w_emu, max_h / h_emu, 1.0)
    fw = int(w_emu * scale)
    fh = int(h_emu * scale)
    left = (Inches(13.333) - fw) // 2
    slide.shapes.add_picture(io.BytesIO(png_bytes), left, top, fw, fh)


def add_quote_box(slide, text, y=Inches(6.65)):
    """Add a styled textbook quote strip at the bottom of a slide."""
    x, w, h = Inches(0.3), Inches(12.7), Inches(0.7)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0xF5, 0xF3, 0xFF)
    box.line.color.rgb = C_PURPLE
    box.line.width = Pt(0.75)
    txBox = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.05),
                                      w - Inches(0.3), h - Inches(0.1))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = '\U0001f4d6 Vazirani:  \u201c' + text + '\u201d'
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    p.font.italic = True
    p.font.name = "Segoe UI"


# ══════════════════════════════════════════════════════
#  BUILD PRESENTATION
# ══════════════════════════════════════════════════════
print("Generating figures...")
figs = [make_fig1(), make_fig2(), make_fig3(), make_fig4(),
        make_fig5(), make_fig6(), make_fig7()]
print("  All 7 figures generated.")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# ── TITLE ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(1), Inches(1.5), Inches(11), Inches(1),
            "Proof of Theorem 3.2", 40, TITLE_C, True, PP_ALIGN.CENTER)
add_textbox(sl, Inches(1), Inches(2.8), Inches(11), Inches(1),
            "Reduction: Steiner Tree  →  Metric Steiner Tree",
            24, C_BLUE, False, PP_ALIGN.CENTER)
add_textbox(sl, Inches(1), Inches(3.8), Inches(11), Inches(0.6),
            "Vazirani — Approximation Algorithms, Chapter 3",
            16, C_MUTED, False, PP_ALIGN.CENTER)
tf = add_textbox(sl, Inches(2), Inches(5), Inches(9), Inches(1.5),
                 "Example:  V = {a, b, c, d},   R = {a, c, d} (Required),   Steiner = {b}",
                 14, C_MUTED, False, PP_ALIGN.CENTER)
add_para(tf, "Edges:  a-b(3),  b-c(2),  b-d(4),  a-c(7),  c-d(8)",
         14, C_ORANGE, False, PP_ALIGN.CENTER)
add_quote_box(sl,
    "Proof: We will transform, in polynomial time, an instance I of the Steiner "
    "tree problem, consisting of graph G = (V, E), to an instance I\u2032 of the "
    "metric Steiner tree problem as follows.")

# ── SLIDE 1: Original Graph G ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(8), Inches(0.6),
            "Slide 1 / 7 — Instance I: Graph G = (V, E)", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.5),
                 "V = {a, b, c, d}     Required R = {a, c, d}     Steiner = {b}",
                 15, TEXT_CLR)
add_image_centered(sl, figs[0], Inches(1.6), max_h=Inches(4.6))
add_quote_box(sl,
    "We will transform, in polynomial time, an instance I of the Steiner tree "
    "problem, consisting of graph G = (V, E), to an instance I\u2032 of the metric "
    "Steiner tree problem as follows.")

# ── SLIDE 2: Pair-by-pair shortest paths ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 2 / 7 — Construction: Shortest Path for Every Pair",
            26, TITLE_C, True)
add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.4),
            "Let G' be the complete graph on V.  cost'(u,v) = shortest u-v path in G.",
            15, TEXT_CLR)

pairs = [
    ("Pair (a, b)", "• Direct a-b: 3\n• Via c: 7+2 = 9", "⟹ cost'(a,b) = 3"),
    ("Pair (a, c)", "• Direct a-c: 7\n• Via b: 3+2 = 5", "⟹ cost'(a,c) = 5 ⭐"),
    ("Pair (a, d)", "• No direct edge\n• Via b: 3+4 = 7", "⟹ cost'(a,d) = 7 (new!)"),
    ("Pair (b, c)", "• Direct b-c: 2\n• Via a: 3+7 = 10", "⟹ cost'(b,c) = 2"),
    ("Pair (b, d)", "• Direct b-d: 4\n• Via c: 2+8 = 10", "⟹ cost'(b,d) = 4"),
    ("Pair (c, d)", "• Direct c-d: 8\n• Via b: 2+4 = 6", "⟹ cost'(c,d) = 6 ⭐"),
]
cx = [Inches(0.4), Inches(4.55), Inches(8.7)]
ry = [Inches(1.5), Inches(3.9)]
for i, (h, p, r) in enumerate(pairs):
    x, y = cx[i%3], ry[i//3]
    w, ht = Inches(3.9), Inches(2.2)
    card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, ht)
    card.fill.solid(); card.fill.fore_color.rgb = RGBColor(0xF8, 0xFA, 0xFC)
    card.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1); card.line.width = Pt(1)
    add_textbox(sl, x+Inches(0.15), y+Inches(0.1), w-Inches(0.3), Inches(0.35), h, 14, C_ORANGE, True)
    add_textbox(sl, x+Inches(0.15), y+Inches(0.45), w-Inches(0.3), Inches(1.0), p, 11, C_MUTED)
    add_textbox(sl, x+Inches(0.15), y+Inches(1.6), w-Inches(0.3), Inches(0.5), r, 13, C_GREEN, True)
add_quote_box(sl,
    "Let G\u2032 be the complete undirected graph on vertex set V. Define the cost "
    "of edge (u, v) in G\u2032 to be the cost of a shortest u\u2013v path in G.")

# ── SLIDE 3: G → G' ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 3 / 7 — Metric Closure G' (Complete Graph)", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.5),
                 "G' has C(4,2)=6 edges.  cost'(u,v)=dist_G(u,v).  R'=R={a,c,d}.", 14, TEXT_CLR)
add_image_centered(sl, figs[1], Inches(1.6), max_h=Inches(4.6))
add_quote_box(sl,
    "G\u2032 is called the metric closure of G. The partition of V into required "
    "and Steiner vertices in I\u2032 is the same as in I.")

# ── SLIDE 4: Lower Bound ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 4 / 7 — Direction 1: OPT(I') ≤ OPT(I)", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.5),
                 "For any edge (u,v) ∈ E, cost in G' ≤ cost in G  ⟹  OPT(I') ≤ OPT(I).",
                 14, TEXT_CLR)
add_image_centered(sl, figs[2], Inches(1.6), max_h=Inches(4.6))
add_quote_box(sl,
    "For any edge (u, v) \u2208 E, its cost in G\u2032 is no more than its cost in G. "
    "Therefore, the cost of an optimal solution in I\u2032 does not exceed the cost "
    "of an optimal solution in I.")

# ── SLIDE 5: Approx Tree T' ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 5 / 7 — Direction 2, Step A: Approx Tree T' in G'", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.8),
                 "Suppose an α-approximation gives T' = {a-c, c-d} in G'.", 15, TEXT_CLR)
add_para(tf, "cost'(T') = 5 + 6 = 11  (connects all required vertices a, c, d)",
         14, C_ORANGE, True)
add_image_centered(sl, figs[3], Inches(2.2), max_h=Inches(4.0))
add_quote_box(sl,
    "Next, given a Steiner tree T\u2032 in I\u2032, we will show how to obtain, in "
    "polynomial time, a Steiner tree T in I of at most the same cost.")

# ── SLIDE 6: Edge Replacement ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 6 / 7 — Step B: Replace Edges by Shortest Paths", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.5),
                 "Replace each edge of T' by its corresponding shortest path in G:", 14, TEXT_CLR)
add_image_centered(sl, figs[4], Inches(1.8), max_h=Inches(4.4))
add_quote_box(sl,
    "The cost of an edge (u, v) in G\u2032 corresponds to the cost of a path in G. "
    "Replace each edge of T\u2032 by the corresponding path to obtain a subgraph of G.")

# ── SLIDE 7: Final Tree ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Slide 7 / 7 — Step C: Final Steiner Tree T in G", 26, TITLE_C, True)
tf = add_textbox(sl, Inches(0.5), Inches(0.9), Inches(12), Inches(0.8),
                 "After removing duplicates, the subgraph is already a tree.", 15, TEXT_CLR)
add_para(tf, "T = {a-b(3), b-c(2), b-d(4)}    cost(T) = 3 + 2 + 4 = 9  ≤  11 = cost'(T')  ✓",
         15, C_GREEN, True)
add_image_centered(sl, figs[5], Inches(2.2), max_h=Inches(4.0))
add_quote_box(sl,
    "Clearly, in this subgraph, all the required vertices are connected. However, "
    "this subgraph may, in general, contain cycles. If so, remove edges to obtain tree T.")

# ── SLIDE 8: Reduction Pipeline ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Conclusion — Factor-Preserving Reduction", 26, TITLE_C, True)
add_image_centered(sl, figs[6], Inches(1.0), max_h=Inches(5.2))
add_quote_box(sl,
    "This completes the approximation factor preserving reduction.")

# ── SLIDE 9: Theorem + Verification ──
sl = prs.slides.add_slide(blank); set_slide_bg(sl)
add_textbox(sl, Inches(0.5), Inches(0.3), Inches(12), Inches(0.6),
            "Theorem 3.2 — Numerical Verification", 26, TITLE_C, True)

c1 = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.2), Inches(6), Inches(4.2))
c1.fill.solid(); c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
tf = add_textbox(sl, Inches(0.7), Inches(1.4), Inches(5.5), Inches(3.8),
                 "Numerical Verification", 18, C_GREEN, True)
for lbl, det, clr in [
    ("OPT(I) in G:", "tree {a-b(3), b-c(2), b-d(4)}, cost = 9", C_BLUE),
    ("OPT(I') in G':", "same tree with cost' = 9 ≤ 9  ✓", C_GREEN),
    ("Approx T' in G':", "{a-c(5), c-d(6)}, cost' = 11", C_RED),
    ("Map back T in G:", "{a-b, b-c, b-d}, cost = 9 ≤ 11  ✓", C_GREEN),
]:
    add_para(tf, "", 4, TEXT_CLR)
    add_para(tf, lbl, 14, clr, True)
    add_para(tf, det, 12, TEXT_CLR)

c2 = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7), Inches(1.2), Inches(5.8), Inches(4.2))
c2.fill.solid(); c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
tf2 = add_textbox(sl, Inches(7.2), Inches(1.4), Inches(5.3), Inches(3.8),
                  "Theorem 3.2", 20, C_PURPLE, True)
add_para(tf2, "", 4, TEXT_CLR)
add_para(tf2, "The reduction from the Steiner tree problem", 13, TEXT_CLR)
add_para(tf2, "to the metric Steiner tree problem is", 13, TEXT_CLR)
add_para(tf2, "approximation factor preserving.", 13, TEXT_CLR, True)
add_para(tf2, "", 6, TEXT_CLR)
add_para(tf2, "Chain of Inequalities:", 15, C_PURPLE, True)
add_para(tf2, "cost(T)", 14, TEXT_CLR, False, PP_ALIGN.CENTER)
add_para(tf2, "≤  cost'(T')       (mapping back)", 13, C_GREEN, True, PP_ALIGN.CENTER)
add_para(tf2, "≤  α · OPT(I')     (α-approximation)", 13, C_GREEN, True, PP_ALIGN.CENTER)
add_para(tf2, "≤  α · OPT(I)      (lower bound)", 13, C_GREEN, True, PP_ALIGN.CENTER)
add_para(tf2, "", 6, TEXT_CLR)
add_para(tf2, "∴  T is an α-approximation for I", 15, C_PURPLE, True, PP_ALIGN.CENTER)

add_textbox(sl, Inches(0.5), Inches(5.6), Inches(12), Inches(0.6),
            "9  ≤  11  ≤  α · 9  ≤  α · 9", 22, C_ORANGE, True, PP_ALIGN.CENTER)
add_textbox(sl, Inches(11.5), Inches(6.15), Inches(1), Inches(0.5),
            "■", 28, C_GREEN, False, PP_ALIGN.RIGHT)
add_quote_box(sl,
    "As a consequence of Theorem 3.2, any approximation factor established for "
    "the metric Steiner tree problem carries over to the entire Steiner tree problem.",
    y=Inches(6.55))

# ── SAVE ──
prs.save(OUT_PPT)
print(f"\n✅ Presentation saved to: {OUT_PPT}")
print(f"   {len(prs.slides)} slides generated.")

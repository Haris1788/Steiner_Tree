"""
Steiner Tree — Interactive Step-by-Step Simulation
====================================================
Interactive Streamlit app (like the other 4 Python demos).
Place required vertices, see distances & metric closure,
add Steiner vertices, build the Steiner tree, then walk
through the Theorem 3.3 proof chain step by step.

Based on Vazirani Chapter 3 — Theorems 3.2, 3.3, Example 3.4

Run:  streamlit run steiner_simulation.py
"""

import streamlit as st
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# ─────────────── Page ───────────────
st.set_page_config(page_title="Steiner Tree Simulation", page_icon="🌳", layout="wide")

# ─────────────── Helpers ───────────────
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def build_complete(pts):
    G = nx.Graph()
    for i, p in enumerate(pts):
        G.add_node(i, pos=p)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            G.add_edge(i, j, weight=dist(pts[i], pts[j]))
    return G

def steiner_tree(rp, sp):
    """MST on R∪S then prune S-only leaves → approximates OPT."""
    all_p = rp + sp
    nr = len(rp)
    if len(all_p) < 2:
        return None, 0, set()
    G = build_complete(all_p)
    T = nx.minimum_spanning_tree(G)
    changed = True
    while changed:
        changed = False
        for n in list(T.nodes()):
            if n >= nr and T.degree(n) == 1:
                T.remove_node(n)
                changed = True
    return T, T.size(weight="weight"), {n for n in T.nodes() if n >= nr}

def dfs_walk(T, start):
    path = []
    def go(u, par):
        path.append(u)
        for nb in sorted(T.neighbors(u)):
            if nb != par:
                go(nb, u)
                path.append(u)
    go(start, -1)
    return path

# ─────────────── Session State ───────────────
for key, default in [("rp", []), ("sp", []), ("mode", "required")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────── Sidebar ───────────────
with st.sidebar:
    st.title("🌳 Steiner Tree Simulation")
    st.caption("Vazirani Ch 3 — Interactive Demo")
    st.markdown("---")

    # ── Point placement mode ──
    st.subheader("1 · Place Points")
    mode = st.radio("Click mode:", ["Required (R) — blue", "Steiner (S) — red"],
                    index=0 if st.session_state.mode == "required" else 1,
                    key="mode_radio")
    st.session_state.mode = "required" if "Required" in mode else "steiner"

    # Manual coordinate input
    with st.expander("Manual coordinate input"):
        cx, cy = st.columns(2)
        with cx:
            mx = st.number_input("X", 10, 590, 300, key="mx")
        with cy:
            my = st.number_input("Y", 10, 490, 250, key="my")
        ac, sc = st.columns(2)
        with ac:
            if st.button("➕ Add R"):
                st.session_state.rp.append((mx, my))
        with sc:
            if st.button("➕ Add S"):
                st.session_state.sp.append((mx, my))

    # Presets
    st.subheader("Quick Start")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("📎 5R + 2S Example"):
            st.session_state.rp = [(120, 80), (420, 60), (520, 280), (320, 420), (80, 340)]
            st.session_state.sp = [(280, 200), (400, 180)]
    with col_p2:
        if st.button("⭐ Star (Ex 3.4)"):
            cx_, cy_, rad = 300, 250, 160
            st.session_state.rp = [
                (cx_ + rad * math.cos(math.radians(a)),
                 cy_ + rad * math.sin(math.radians(a)))
                for a in range(0, 360, 60)]
            st.session_state.sp = [(cx_, cy_)]
    if st.button("🗑️ Clear All"):
        st.session_state.rp = []
        st.session_state.sp = []

    st.markdown("---")

    # ── Visualization layers ──
    st.subheader("2 · Visualization Layers")

    st.markdown("**Step 1 — Setup**")
    show_distances = st.checkbox("Show all distances", value=False,
        help="Complete graph with all pairwise edges & distances")

    st.markdown("**Step 2 — Thm 3.2: Metric Closure G'**")
    show_closure = st.checkbox("Metric Closure on R (purple)", value=False,
        help="Complete graph on R only. Edge weight = Euclidean distance.")

    st.markdown("**Step 3 — Steiner Tree (≈ OPT)**")
    show_steiner = st.checkbox("Steiner Tree R∪S (red)", value=False,
        help="MST on R∪S, pruned S-leaves. Approximates OPT.")

    st.markdown("**Step 4 — Proof of Thm 3.3**")
    show_doubled = st.checkbox("4a · Doubled edges (indigo)", value=False,
        help="Double all Steiner tree edges → Eulerian. Cost = 2·OPT")
    show_euler = st.checkbox("4b · Euler tour (orange)", value=False,
        help="DFS walk on doubled Steiner tree. Visits R & S vertices.")
    show_shortcut = st.checkbox("4c · Shortcut to R (green)", value=False,
        help="Skip S & repeats → HC on R. Triangle ineq: cost ≤ 2·OPT")

    st.markdown("**Step 5 — Algorithm Output**")
    show_mst_r = st.checkbox("MST on R only (blue)", value=True,
        help="The 2-Approximation result. MST_R ≤ 2·OPT.")

    st.markdown("---")

    # ── Example 3.4 (tight instance) ──
    st.subheader("3 · Example 3.4 (Tight)")
    show_star = st.checkbox("Show star-graph analysis", value=False)

    st.markdown("---")
    st.subheader("Point Count")
    st.write(f"**Required (R):** {len(st.session_state.rp)}")
    st.write(f"**Steiner  (S):** {len(st.session_state.sp)}")

    st.markdown("---")
    st.markdown("""
**Theorems**

**Thm 3.2** — Metric Closure G' preserves approx factor.

**Thm 3.3** — MST on R ≤ 2 · OPT.

**Proof:** OPT → ×2 → Euler → shortcut R → HC ≤ 2·OPT
→ remove edge → span. tree ≤ 2·OPT → MST_R ≤ 2·OPT ∎
    """)

# ─────────────── Shorthand ───────────────
rp = st.session_state.rp
sp = st.session_state.sp
all_p = rp + sp
n_r = len(rp)

# ─────────────── Canvas (clickable matplotlib via form) ───────────────
st.markdown("## Steiner Tree — Interactive Graph")

# Click-to-add via columns of buttons (grid approach)
# We use a matplotlib figure with click coordinates entered via the sidebar

# ─────────────── MAIN FIGURE ───────────────
if len(rp) == 0 and len(sp) == 0:
    st.info("👈 Add Required and Steiner points from the sidebar, or load a preset example.")
else:
    # Compute everything needed
    mst_r_cost = 0
    st_cost = 0
    shortcut_cost = 0
    st_tree = None
    used_s = set()
    euler_path = []

    if n_r >= 2:
        G_r = build_complete(rp)
        mst_r_obj = nx.minimum_spanning_tree(G_r)
        mst_r_cost = mst_r_obj.size(weight="weight")

    if sp and n_r >= 1:
        st_tree, st_cost, used_s = steiner_tree(rp, sp)

    if st_tree and len(st_tree.nodes()) > 1:
        start = min(st_tree.nodes())
        for nd in st_tree.nodes():
            if nd < n_r:
                start = nd
                break
        euler_path = dfs_walk(st_tree, start)

    # ─── Build Figure ───
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(-20, 620)
    ax.set_ylim(520, -20)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#fafafa')
    fig.patch.set_facecolor('#fafafa')

    def edge_label(ax_, p1, p2, color, bg, fs=7, zo=6, off=(0, 0)):
        mx = (p1[0] + p2[0]) / 2 + off[0]
        my = (p1[1] + p2[1]) / 2 + off[1]
        d = dist(p1, p2)
        ax_.text(mx, my, f"{d:.0f}", fontsize=fs, color=color,
                 ha='center', va='center', zorder=zo,
                 bbox=dict(facecolor=bg, edgecolor=color, alpha=0.9,
                           boxstyle='round,pad=0.15'))

    # ──── Layer 1: Complete graph / all distances ────
    if show_distances and len(all_p) > 1:
        for i in range(len(all_p)):
            for j in range(i + 1, len(all_p)):
                p1, p2 = all_p[i], all_p[j]
                clr = "#e5e7eb"
                if i >= n_r or j >= n_r:
                    clr = "#fce7f3"
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        color=clr, lw=0.6, alpha=0.4, zorder=2)
                edge_label(ax, p1, p2, '#9ca3af', '#f9fafb', fs=6, zo=3)

    # ──── Layer 2: Metric Closure on R (purple) ────
    if show_closure and n_r > 1:
        for i in range(n_r):
            for j in range(i + 1, n_r):
                p1, p2 = rp[i], rp[j]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                        color='#a78bfa', lw=1.5, alpha=0.6, zorder=4)
                edge_label(ax, p1, p2, '#5b21b6', '#ede9fe', fs=7, zo=5)

    # ──── Layer 3: Steiner Tree (≈ OPT) — red ────
    if show_steiner and st_tree:
        for u, v, d in st_tree.edges(data=True):
            p1, p2 = all_p[u], all_p[v]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                    color='#dc2626', lw=3.5, alpha=0.8, zorder=6)
            edge_label(ax, p1, p2, '#991b1b', '#fee2e2', fs=8, zo=7)

    # ──── Layer 4a: Doubled edges (indigo) ────
    if show_doubled and st_tree:
        for u, v, d in st_tree.edges(data=True):
            p1, p2 = all_p[u], all_p[v]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            ln = math.hypot(dx, dy)
            if ln > 0:
                px, py = -dy / ln * 4, dx / ln * 4
                ax.plot([p1[0]+px, p2[0]+px], [p1[1]+py, p2[1]+py],
                        color='#6366f1', lw=2.5, ls='--', alpha=0.7, zorder=8)
                ax.plot([p1[0]-px, p2[0]-px], [p1[1]-py, p2[1]-py],
                        color='#818cf8', lw=2.5, ls='--', alpha=0.7, zorder=8)

    # ──── Layer 4b: Euler tour (orange) ────
    if show_euler and euler_path:
        for i_e in range(len(euler_path) - 1):
            u, v = euler_path[i_e], euler_path[i_e + 1]
            ax.plot([all_p[u][0], all_p[v][0]], [all_p[u][1], all_p[v][1]],
                    color='#f59e0b', lw=2, ls=':', alpha=0.8, zorder=9)
        for idx_e, nd in enumerate(euler_path):
            ax.text(all_p[nd][0] + 10, all_p[nd][1] - 10, str(idx_e),
                    fontsize=6, color='#b45309', alpha=0.7, zorder=15)

    # ──── Layer 4c: Shortcut to R only (green) ────
    if show_shortcut and euler_path:
        seen = set()
        sc_path = []
        for nd in euler_path:
            if nd < n_r and nd not in seen:
                seen.add(nd)
                sc_path.append(nd)
        if len(sc_path) > 1:
            sc_path.append(sc_path[0])
        shortcut_cost = 0
        for i_sc in range(len(sc_path) - 1):
            u, v = sc_path[i_sc], sc_path[i_sc + 1]
            p1, p2 = rp[u], rp[v]
            ax.annotate("", xy=(p2[0], p2[1]), xytext=(p1[0], p1[1]),
                        arrowprops=dict(arrowstyle='->', color='#10b981',
                                        lw=3, connectionstyle='arc3,rad=0.08'),
                        zorder=10)
            shortcut_cost += dist(p1, p2)
        for idx_sc, nd in enumerate(sc_path[:-1]):
            ax.text(rp[nd][0] - 16, rp[nd][1] + 16, f"→{idx_sc+1}",
                    fontsize=8, color='#059669', fontweight='bold', zorder=16)

    # ──── Layer 5: MST on R (blue) — algorithm output ────
    if show_mst_r and n_r > 1:
        for u, v, d in mst_r_obj.edges(data=True):
            p1, p2 = rp[u], rp[v]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                    color='#2563eb', lw=3, alpha=0.85, zorder=11)
            edge_label(ax, p1, p2, '#1e40af', '#dbeafe', fs=8, zo=12)

    # ──── Draw points (always on top) ────
    for i, p in enumerate(rp):
        ax.plot(p[0], p[1], 'o', ms=14, color='#2563eb', zorder=20)
        ax.text(p[0], p[1], f"R{i+1}", color='white', ha='center', va='center',
                fontsize=7, fontweight='bold', zorder=21)
    for i, p in enumerate(sp):
        is_used = (n_r + i) in used_s
        col = '#dc2626' if is_used else '#f87171'
        sz = 12 if is_used else 9
        ax.plot(p[0], p[1], '^', ms=sz, color=col, zorder=20)
        lbl = f"S{i+1}" if is_used else f"s{i+1}"
        ax.text(p[0], p[1] - 14, lbl, color=col, ha='center',
                fontsize=7, fontweight='bold', zorder=21)
        if show_shortcut and is_used:
            ax.plot(p[0], p[1], 'x', ms=16, color='#ef4444',
                    markeredgewidth=3, zorder=22)

    # ──── Legend ────
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2563eb',
                   ms=10, label='Required (R)'),
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#dc2626',
                   ms=10, label='Steiner (S)'),
    ]
    if show_closure:
        handles.append(plt.Line2D([0], [0], color='#a78bfa', lw=2, label='Metric Closure G′'))
    if show_steiner:
        handles.append(plt.Line2D([0], [0], color='#dc2626', lw=3, label='Steiner Tree (≈OPT)'))
    if show_doubled:
        handles.append(plt.Line2D([0], [0], color='#6366f1', lw=2, ls='--', label='Doubled (2·OPT)'))
    if show_euler:
        handles.append(plt.Line2D([0], [0], color='#f59e0b', lw=2, ls=':', label='Euler Tour'))
    if show_shortcut:
        handles.append(plt.Line2D([0], [0], color='#10b981', lw=3, label='Shortcut HC on R'))
    if show_mst_r:
        handles.append(plt.Line2D([0], [0], color='#2563eb', lw=3, label='MST on R (2-Approx)'))
    ax.legend(handles=handles, loc='upper right', fontsize=8,
              framealpha=0.95, edgecolor='#cbd5e1')

    st.pyplot(fig)

    # ─────────────── Results Panel ───────────────
    st.markdown("---")
    st.markdown("### Results")

    cols = st.columns(4)
    with cols[0]:
        if n_r >= 2:
            st.metric("MST on R (Algorithm)", f"{mst_r_cost:.0f}")
        else:
            st.metric("MST on R", "—")
    with cols[1]:
        if st_cost > 0:
            st.metric("Steiner Tree (≈ OPT)", f"{st_cost:.0f}")
        else:
            st.metric("Steiner Tree", "— (add S pts)")
    with cols[2]:
        if st_cost > 0 and mst_r_cost > 0:
            ratio = mst_r_cost / st_cost
            st.metric("Ratio MST_R / OPT", f"{ratio:.3f}",
                      delta=f"≤ 2.00  {'✓' if ratio <= 2.001 else '!'}")
        else:
            st.metric("Ratio", "—")
    with cols[3]:
        if st_cost > 0 and mst_r_cost > 0:
            saving = mst_r_cost - st_cost
            if saving > 0:
                st.metric("Saving with S hubs", f"{saving:.0f}  ({saving/mst_r_cost*100:.0f}%)")
            else:
                st.metric("Saving", "0")
        else:
            st.metric("Saving", "—")

    # Cost comparison
    if st_cost > 0 and mst_r_cost > 0:
        saving = mst_r_cost - st_cost
        if saving > 0:
            st.success(
                f"✅ Steiner hubs save **{saving:.0f}** ({saving/mst_r_cost*100:.0f}%) — "
                f"OPT ≈ {st_cost:.0f}  vs  MST_R = {mst_r_cost:.0f}")
        else:
            st.info("Steiner points don't reduce cost here. "
                    "Try repositioning them as central hubs between R vertices.")

    if show_shortcut and shortcut_cost > 0:
        st.info(
            f"**Shortcut HC cost:** {shortcut_cost:.0f}  |  "
            f"2·OPT = {2*st_cost:.0f}  |  "
            f"Shortcut ≤ 2·OPT?  {'✓ Yes' if shortcut_cost <= 2*st_cost + 0.1 else '✗ No'}")

    if show_doubled or show_euler or show_shortcut:
        st.markdown("#### Proof Chain (Theorem 3.3)")
        proof_data = {
            "Step": ["1. Steiner tree (OPT)", "2. Double all edges",
                     "3. Euler tour on doubled tree",
                     "4. Shortcut: skip S & repeats",
                     "5. Remove one edge → spanning tree",
                     "6. MST_R ≤ any spanning tree"],
            "Cost": [f"{st_cost:.0f}" if st_cost > 0 else "OPT",
                     f"{2*st_cost:.0f}" if st_cost > 0 else "2·OPT",
                     f"= {2*st_cost:.0f}" if st_cost > 0 else "= 2·OPT",
                     f"≤ {2*st_cost:.0f} (tri. ineq)" if st_cost > 0 else "≤ 2·OPT",
                     f"≤ {2*st_cost:.0f}" if st_cost > 0 else "≤ 2·OPT",
                     f"**MST_R = {mst_r_cost:.0f} ≤ {2*st_cost:.0f}  ∎**" if st_cost > 0 else "MST_R ≤ 2·OPT ∎"],
        }
        st.table(proof_data)

# ─────────────── Example 3.4: Star Graph ───────────────
if show_star:
    st.markdown("---")
    st.markdown("## Example 3.4 — Star Graph (Tight Instance)")
    st.markdown(
        "Star with **n** terminals on a circle + 1 Steiner center. "
        "Each star edge = 1, each perimeter edge = 2. "
        "Ratio = 2(n−1)/n → 2 as n → ∞."
    )
    n_star = st.slider("Number of terminals (n)", 3, 15, 6)

    cx_, cy_, radius_ = 300, 240, 170
    star_r = [(cx_ + radius_ * math.cos(math.radians(a)),
               cy_ + radius_ * math.sin(math.radians(a)))
              for a in np.linspace(0, 360, n_star, endpoint=False)]

    fig2, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for a in axes:
        a.set_xlim(-10, 610); a.set_ylim(500, -10)
        a.set_aspect('equal'); a.axis('off'); a.set_facecolor('#fafafa')

    # Left: OPT (star)
    axes[0].set_title(f"OPT: Star Tree  (cost = n = {n_star})", fontsize=12, color='#b91c1c')
    for i, p in enumerate(star_r):
        axes[0].plot([cx_, p[0]], [cy_, p[1]], color='#ef4444', lw=3, alpha=0.8)
        mx_, my_ = (cx_ + p[0]) / 2, (cy_ + p[1]) / 2
        axes[0].text(mx_, my_, "1", fontsize=8, color='#991b1b', ha='center', va='center',
                     bbox=dict(facecolor='#fee2e2', edgecolor='#fca5a5', alpha=0.9,
                               boxstyle='round,pad=0.15'))
        axes[0].plot(p[0], p[1], 'o', ms=14, color='#2563eb', zorder=20)
        axes[0].text(p[0], p[1], f"R{i+1}", color='white', ha='center', va='center',
                     fontsize=7, fontweight='bold', zorder=21)
    axes[0].plot(cx_, cy_, '*', ms=20, color='#eab308', zorder=20,
                 markeredgecolor='#a16207', markeredgewidth=1)
    axes[0].text(cx_, cy_ - 18, "S", color='#a16207', ha='center', fontsize=9,
                 fontweight='bold', zorder=21)

    # Right: MST on R (perimeter)
    mst_cost_star = 2 * (n_star - 1)
    axes[1].set_title(f"MST on R  (cost = 2(n−1) = {mst_cost_star})", fontsize=12, color='#1d4ed8')
    # Draw perimeter path (MST = chain around circle)
    for i in range(n_star - 1):
        p1, p2 = star_r[i], star_r[i + 1]
        axes[1].plot([p1[0], p2[0]], [p1[1], p2[1]], color='#3b82f6', lw=3, alpha=0.8)
        mx_, my_ = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        axes[1].text(mx_, my_, "2", fontsize=8, color='#1e40af', ha='center', va='center',
                     bbox=dict(facecolor='#dbeafe', edgecolor='#93c5fd', alpha=0.9,
                               boxstyle='round,pad=0.15'))
    for i, p in enumerate(star_r):
        axes[1].plot(p[0], p[1], 'o', ms=14, color='#2563eb', zorder=20)
        axes[1].text(p[0], p[1], f"R{i+1}", color='white', ha='center', va='center',
                     fontsize=7, fontweight='bold', zorder=21)

    fig2.patch.set_facecolor('#fafafa')
    st.pyplot(fig2)

    ratio_star = 2 * (n_star - 1) / n_star
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("n (terminals)", n_star)
    c2.metric("OPT (star)", n_star)
    c3.metric("MST on R", mst_cost_star)
    c4.metric("Ratio", f"{ratio_star:.3f}")

    st.latex(r"\text{Ratio} = \frac{2(n-1)}{n} = \frac{%d}{%d} = %.4f" % (mst_cost_star, n_star, ratio_star))
    st.latex(r"\lim_{n \to \infty} \frac{2(n-1)}{n} = 2")
    st.warning(f"As n → ∞, ratio → 2. **Factor 2 is tight** — MST cannot guarantee better.")

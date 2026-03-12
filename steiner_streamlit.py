import streamlit as st
import math
import networkx as nx
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

# --- Config ---
st.set_page_config(page_title="Metric Steiner Tree Demo", layout="wide")

st.title("🌳 Metric Steiner Tree: 2-Approximation Demo")
st.markdown("""
**Vazirani Chapter 3** — This demo visualizes Theorems 3.2 and 3.3.
Place **Required** (blue) and **Steiner** (red) points on the canvas, then follow the steps.
""")

# --- Sidebar ---
st.sidebar.header("🎮 Controls")
drawing_mode = st.sidebar.radio("Point mode:", ["Required (Blue)", "Steiner (Red)"])
stroke_color = "#0000FF" if "Required" in drawing_mode else "#FF0000"

st.sidebar.markdown("---")
st.sidebar.header("Visualization Steps")

st.sidebar.subheader("Step 1: Problem Setup")
show_complete = st.sidebar.checkbox("Complete graph (all edges)", value=False,
    help="All pairwise edges between R∪S with distances.")

st.sidebar.markdown("---")
st.sidebar.subheader("Step 2: Theorem 3.2 — Metric Closure")
show_closure = st.sidebar.checkbox("Metric Closure G' on R (purple)", value=False,
    help="Complete graph on R vertices. Edge weight = shortest path distance.")
if show_closure:
    st.sidebar.info("G' = complete graph on R. Edge cost(u,v) = shortest path dist between u,v.")

st.sidebar.markdown("---")
st.sidebar.subheader("Step 3: Steiner Tree (≈ OPT)")
show_steiner = st.sidebar.checkbox("Steiner tree R∪S (red)", value=False,
    help="MST on R∪S, pruning S-leaves. Approximates the optimal Steiner tree.")
if show_steiner:
    st.sidebar.warning("OPT connects R through S hubs. We approximate with MST on R∪S, pruning S-only leaves.")

st.sidebar.markdown("---")
st.sidebar.subheader("Step 4: Proof of Theorem 3.3")
st.sidebar.caption("Proof chain: OPT → ×2 → Euler → shortcut to R → HC ≤ 2·OPT")
show_doubled = st.sidebar.checkbox("4a. Doubled edges (indigo)", value=False,
    help="Double all Steiner tree edges. Cost = 2·OPT. Creates Eulerian graph.")
show_euler = st.sidebar.checkbox("4b. Euler tour (orange)", value=False,
    help="Euler tour on doubled Steiner tree. Visits R and S vertices.")
show_shortcut = st.sidebar.checkbox("4c. Shortcut to R only (green)", value=False,
    help="Skip S vertices → Hamiltonian cycle on R. Triangle ineq: cost ≤ 2·OPT.")

st.sidebar.markdown("---")
st.sidebar.subheader("Step 5: Algorithm Output")
show_mst_r = st.sidebar.checkbox("MST on R only (blue)", value=True,
    help="2-Approximation result. MST_R ≤ 2·OPT guaranteed by Theorem 3.3.")

# Canvas clear
if "canvas_key" not in st.session_state:
    st.session_state["canvas_key"] = 0
if st.sidebar.button("🗑️ Clear Canvas"):
    st.session_state["canvas_key"] += 1

# --- Canvas ---
col_canvas, col_plot = st.columns([1, 1])

with col_canvas:
    st.subheader("Canvas — Click to Place Points")
    canvas_result = st_canvas(
        fill_color=stroke_color,
        stroke_width=2,
        stroke_color=stroke_color,
        background_color="#FFFFFF",
        update_streamlit=True,
        height=500, width=650,
        drawing_mode="point",
        point_display_radius=5 if "Required" in drawing_mode else 4,
        key=f"canvas_{st.session_state['canvas_key']}",
    )

# --- Extract points ---
req_pts = []
stein_pts = []
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data.get("objects", []):
        if obj.get("type") == "circle":
            x = obj["left"] + obj.get("radius", 0)
            y = obj["top"]  + obj.get("radius", 0)
            c = (obj.get("stroke") or "").lower()
            if c in ("#0000ff", "blue", "#0000ff"):
                req_pts.append((x, y))
            else:
                stein_pts.append((x, y))

# --- Algorithms ---
def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def build_graph(pts):
    G = nx.Graph()
    for i, p in enumerate(pts):
        G.add_node(i, pos=p)
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            G.add_edge(i, j, weight=dist(pts[i], pts[j]))
    return G

def steiner_tree(rp, sp):
    """MST on R∪S, then prune S-only leaves. Returns (edges_as_idx_tuples, cost, pruned_graph)."""
    all_p = rp + sp
    n_r = len(rp)
    if len(all_p) < 2:
        return [], 0, None
    G = build_graph(all_p)
    T = nx.minimum_spanning_tree(G)
    # Iteratively prune S-only leaves
    changed = True
    while changed:
        changed = False
        leaves = [n for n in T.nodes() if T.degree(n) == 1 and n >= n_r]
        for lf in leaves:
            T.remove_node(lf)
            changed = True
    cost = T.size(weight='weight')
    return list(T.edges(data=True)), cost, T

def dfs_walk(T, start):
    """DFS walk on tree T: returns node visit order (each edge traversed twice)."""
    path = []
    def _dfs(u, par):
        path.append(u)
        for nb in T.neighbors(u):
            if nb != par:
                _dfs(nb, u)
                path.append(u)
    _dfs(start, -1)
    return path

# --- Defaults (before conditional block) ---
mst_r_cost = 0
st_cost = 0
st_graph = None
shortcut_cost = 0

# --- Plotting ---
if len(req_pts) > 0:
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.invert_yaxis()
    all_p = req_pts + stein_pts
    n_r = len(req_pts)
    r_ids = set(range(n_r))

    # Layer 1: Complete graph
    if show_complete and len(all_p) > 1:
        G_all = build_graph(all_p)
        pos = {i: all_p[i] for i in range(len(all_p))}
        for u, v, d in G_all.edges(data=True):
            c = "#f9a8d4" if (u >= n_r or v >= n_r) else "#e5e7eb"
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color=c, lw=0.7, alpha=0.5)

    # Layer 2: Metric Closure on R (purple)
    if show_closure and len(req_pts) > 1:
        for i in range(len(req_pts)):
            for j in range(i+1, len(req_pts)):
                ax.plot([req_pts[i][0], req_pts[j][0]],
                        [req_pts[i][1], req_pts[j][1]],
                        color="#a78bfa", lw=1.2, alpha=0.6)
                mx = (req_pts[i][0]+req_pts[j][0])/2
                my = (req_pts[i][1]+req_pts[j][1])/2
                d = dist(req_pts[i], req_pts[j])
                ax.text(mx, my, f"{d:.0f}", fontsize=7, color="#7c3aed",
                        ha='center', va='center',
                        bbox=dict(facecolor='#ede9fe', edgecolor='#a78bfa',
                                  alpha=0.9, boxstyle='round,pad=0.2'))

    # Step 3: Steiner tree (≈ OPT)
    st_edges, st_cost, st_graph = [], 0, None
    if stein_pts:
        st_edges, st_cost, st_graph = steiner_tree(req_pts, stein_pts)

    if show_steiner and st_edges and st_graph:
        pos = {i: all_p[i] for i in st_graph.nodes()}
        for u, v, d in st_edges:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color="#dc2626", lw=3, alpha=0.8)
            mx = (pos[u][0]+pos[v][0])/2
            my = (pos[u][1]+pos[v][1])/2
            ax.text(mx, my, f"{d['weight']:.0f}", fontsize=8, color="#991b1b",
                    ha='center', va='center',
                    bbox=dict(facecolor='#fee2e2', edgecolor='#fca5a5',
                              alpha=0.95, boxstyle='round,pad=0.2'))

    # Step 4a: Doubled edges (indigo)
    if show_doubled and st_edges and st_graph:
        pos = {i: all_p[i] for i in st_graph.nodes()}
        for u, v, d in st_edges:
            p1, p2 = pos[u], pos[v]
            dx, dy = p2[0]-p1[0], p2[1]-p1[1]
            ln = math.hypot(dx, dy)
            if ln > 0:
                px, py = -dy/ln*3, dx/ln*3
                ax.plot([p1[0]+px, p2[0]+px], [p1[1]+py, p2[1]+py],
                        color="#6366f1", lw=2, ls='--', alpha=0.7)
                ax.plot([p1[0]-px, p2[0]-px], [p1[1]-py, p2[1]-py],
                        color="#818cf8", lw=2, ls='--', alpha=0.7)

    # Step 4b: Euler tour on Steiner tree (orange)
    euler_path = []
    if (show_euler or show_shortcut) and st_graph and len(st_graph.nodes()) > 1:
        # Find an R vertex as start
        start = min(st_graph.nodes())
        for n in st_graph.nodes():
            if n < n_r:
                start = n
                break
        euler_path = dfs_walk(st_graph, start)

    if show_euler and euler_path:
        pos = {i: all_p[i] for i in st_graph.nodes()}
        for i in range(len(euler_path)-1):
            u, v = euler_path[i], euler_path[i+1]
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color="#f59e0b", lw=2, ls=':', alpha=0.8)
        # Walk order numbers
        for idx, n in enumerate(euler_path):
            ax.text(pos[n][0]+8, pos[n][1]-8, str(idx),
                    fontsize=6, color="#b45309", alpha=0.7)

    # Step 4c: Shortcut to R only (green)
    shortcut_cost = 0
    if show_shortcut and euler_path:
        pos = {i: all_p[i] for i in st_graph.nodes()}
        seen = set()
        sc_path = []
        for n in euler_path:
            if n in r_ids and n not in seen:
                seen.add(n)
                sc_path.append(n)
        if len(sc_path) > 1:
            sc_path.append(sc_path[0])
        for i in range(len(sc_path)-1):
            u, v = sc_path[i], sc_path[i+1]
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color="#10b981", lw=3, alpha=0.7)
            shortcut_cost += dist(all_p[u], all_p[v])

    # Step 5: MST on R only (blue) — the algorithm output
    mst_r_cost = 0
    if len(req_pts) > 1:
        G_r = build_graph(req_pts)
        mst_r = nx.minimum_spanning_tree(G_r)
        mst_r_cost = mst_r.size(weight='weight')

        if show_mst_r:
            pos_r = {i: req_pts[i] for i in range(len(req_pts))}
            for u, v, d in mst_r.edges(data=True):
                ax.plot([pos_r[u][0], pos_r[v][0]], [pos_r[u][1], pos_r[v][1]],
                        color="#2563eb", lw=2.5)
                mx = (pos_r[u][0]+pos_r[v][0])/2
                my = (pos_r[u][1]+pos_r[v][1])/2
                ax.text(mx, my, f"{d['weight']:.0f}", fontsize=8, color="#1e40af",
                        ha='center', va='center',
                        bbox=dict(facecolor='#dbeafe', edgecolor='#93c5fd',
                                  alpha=0.95, boxstyle='round,pad=0.2'))

    # Plot points
    for i, p in enumerate(req_pts):
        ax.plot(p[0], p[1], 'o', ms=12, color='#2563eb', zorder=10)
        ax.text(p[0], p[1], str(i+1), color='white', ha='center', va='center',
                fontsize=8, fontweight='bold', zorder=11)
    for i, p in enumerate(stein_pts):
        used = st_graph and (n_r + i) in st_graph.nodes()
        col = '#dc2626' if used else '#f87171'
        sz = 10 if used else 8
        ax.plot(p[0], p[1], '^', ms=sz, color=col, zorder=10)
        label = f"S{i+1}" if used else "s"
        ax.text(p[0], p[1]-12, label, color=col, ha='center', fontsize=7,
                fontweight='bold', zorder=11)

    ax.axis('off')
    with col_plot:
        st.subheader("Visualization")
        st.pyplot(fig)

# --- Results & Theorems ---
st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    if len(req_pts) > 1:
        st.metric("MST on R (Algorithm)", f"{mst_r_cost:.0f} px",
                  help="2-Approximation output")
    else:
        st.metric("MST on R", "—")

with c2:
    if stein_pts and st_cost > 0:
        st.metric("Steiner Tree (≈ OPT)", f"{st_cost:.0f} px",
                  help="MST on R∪S, pruned S-leaves")
    else:
        st.metric("Steiner Tree (≈ OPT)", "— (add Steiner pts)")

with c3:
    if st_cost > 0 and mst_r_cost > 0:
        ratio = mst_r_cost / st_cost
        st.metric("Ratio MST_R / OPT", f"{ratio:.2f}",
                  delta=f"≤ 2.00 {'✓' if ratio <= 2.001 else '!'}")
    else:
        st.metric("Ratio", "—")

# --- Comparison ---
if st_cost > 0 and mst_r_cost > 0:
    saving = mst_r_cost - st_cost
    if saving > 0:
        pct = saving / mst_r_cost * 100
        st.success(f"✅ Steiner hubs save **{saving:.0f} px ({pct:.1f}%)** "
                   f"— OPT = {st_cost:.0f} vs MST_R = {mst_r_cost:.0f}")
    else:
        st.info("Steiner points don't help here. Try repositioning them as central hubs.")

    if show_shortcut:
        st.info(f"**Shortcut HC cost**: {shortcut_cost:.0f} px — "
                f"Check: {shortcut_cost:.0f} ≤ 2·OPT = {2*st_cost:.0f}? "
                f"{'✓' if shortcut_cost <= 2*st_cost + 0.1 else '✗'}")

# --- Theorems sidebar ---
st.sidebar.markdown("---")
st.sidebar.subheader("📖 Theorems")
st.sidebar.markdown("""
**Theorem 3.2** (Metric Closure)
Steiner tree in metric closure G' ≤ Steiner tree in G.

**Theorem 3.3** (2-Approximation)
MST on R ≤ 2 · OPT.

**Proof chain:**
OPT → double (2·OPT) → Euler tour
→ shortcut to R (tri. ineq ≤ 2·OPT)
→ remove edge → spanning tree on R
→ MST_R ≤ spanning tree ≤ 2·OPT  ✓
""")

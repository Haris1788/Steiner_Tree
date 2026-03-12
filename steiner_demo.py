import tkinter as tk
import math


class SteinerDemo:
    """
    Interactive demo of the 2-Approximation for Metric Steiner Tree.
    Follows Vazirani Chapter 3, Theorems 3.2 and 3.3.

    Correct proof chain (Theorem 3.3):
        OPT (Steiner tree on R using S)
        → double all edges (cost = 2·OPT)
        → Euler tour on R ∪ S
        → shortcut: skip S vertices & repeats → HC on R
        → triangle ineq: cost(HC) ≤ 2·OPT
        → remove one edge → spanning tree on R ≤ 2·OPT
        → MST_R ≤ spanning tree ≤ 2·OPT  ✓
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Steiner Tree 2-Approximation — Vazirani Ch 3")
        self.root.geometry("1250x780")
        self.root.minsize(1050, 650)

        # --- State ---
        self.points = []          # {'x','y','type','id'}
        self.mode = 'R'           # placement mode

        # Toggle variables  (ordered to match the proof flow)
        self.show_distances   = tk.BooleanVar(value=True)
        self.show_complete    = tk.BooleanVar(value=False)
        # Theorem 3.2
        self.show_closure     = tk.BooleanVar(value=False)
        # Steiner tree (≈ OPT)
        self.show_steiner_tree = tk.BooleanVar(value=False)
        # Proof of Theorem 3.3 (operates on the Steiner tree!)
        self.show_doubled     = tk.BooleanVar(value=False)
        self.show_euler       = tk.BooleanVar(value=False)
        self.show_shortcut    = tk.BooleanVar(value=False)
        # Algorithm output
        self.show_mst_req     = tk.BooleanVar(value=False)

        # --- Layout ---
        self.sidebar = tk.Frame(root, width=340, bg="#f3f4f6")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Scrollable sidebar
        self.sb_canvas = tk.Canvas(self.sidebar, bg="#f3f4f6", highlightthickness=0)
        self.sb_scroll = tk.Scrollbar(self.sidebar, orient="vertical",
                                      command=self.sb_canvas.yview)
        self.sb_inner  = tk.Frame(self.sb_canvas, bg="#f3f4f6", padx=12, pady=10)
        self.sb_inner.bind("<Configure>",
            lambda e: self.sb_canvas.configure(scrollregion=self.sb_canvas.bbox("all")))
        self.sb_canvas.create_window((0, 0), window=self.sb_inner,
                                     anchor="nw", width=325)
        self.sb_canvas.configure(yscrollcommand=self.sb_scroll.set)
        self.sb_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sb_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mouse wheel scrolling on sidebar
        self.sb_canvas.bind("<Enter>",
            lambda e: self.sb_canvas.bind_all("<MouseWheel>",
                lambda ev: self.sb_canvas.yview_scroll(-1*(ev.delta//120), "units")))
        self.sb_canvas.bind("<Leave>",
            lambda e: self.sb_canvas.unbind_all("<MouseWheel>"))

        # Canvas area
        cf = tk.Frame(root, bg="white")
        cf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(cf, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_click)

        self._build_sidebar()

    # ================================================================== UI
    def _build_sidebar(self):
        sb = self.sb_inner

        tk.Label(sb, text="Metric Steiner Tree",
                 font=("Arial", 15, "bold"), bg="#f3f4f6").pack(anchor="w")
        tk.Label(sb, text="2-Approximation  (Vazirani Ch 3)",
                 font=("Arial", 9), bg="#f3f4f6", fg="#6b7280").pack(anchor="w", pady=(0,10))

        # ---- Point placement ----
        fm = tk.Frame(sb, bg="#f3f4f6"); fm.pack(fill=tk.X, pady=(0,4))
        self.btn_r = tk.Button(fm, text="+ Required (Blue)",
                               command=lambda: self._set_mode('R'),
                               bg="#dbeafe", fg="#1d4ed8", relief="flat",
                               padx=6, pady=3, font=("Arial", 9, "bold"))
        self.btn_r.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,4))
        self.btn_s = tk.Button(fm, text="+ Steiner (Red)",
                               command=lambda: self._set_mode('S'),
                               bg="white", fg="#374151", relief="flat",
                               padx=6, pady=3, font=("Arial", 9, "bold"))
        self.btn_s.pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(sb, text="Clear Canvas", command=self._clear,
                  bg="#fee2e2", fg="#dc2626", relief="flat", pady=3,
                  font=("Arial", 9)).pack(fill=tk.X, pady=(4,10))

        self._sep(sb)

        # ============================================================ STEP 1
        self._heading(sb, "Step 1 — Problem Setup")
        self._explain(sb, (
            "Click canvas to place points.\n"
            "Blue = Required R (must connect)\n"
            "Red  = Steiner S (optional hubs)\n"
            "Graph G has metric (triangle inequality)."))
        self._chk(sb, "Show distances",            self.show_distances)
        self._chk(sb, "Complete graph (all edges)", self.show_complete)
        self._sep(sb)

        # ============================================================ STEP 2
        self._heading(sb, "Step 2 — Thm 3.2: Metric Closure G'")
        self._explain(sb, (
            "Complete graph G' on R vertices.\n"
            "Edge cost(u,v) = shortest path dist\n"
            "between u,v through any S vertices.\n"
            "(In Euclidean: direct = shortest.)"))
        self._chk(sb, "Metric Closure on R (purple)", self.show_closure,
                  fg="#7c3aed")
        self._sep(sb)

        # ============================================================ STEP 3
        self._heading(sb, "Step 3 — Steiner Tree (OPT)")
        self._explain(sb, (
            "Optimal Steiner tree connects R\n"
            "using S as hubs. Cost = OPT.\n"
            "We approximate OPT with MST on R∪S,\n"
            "then prune S-only leaves."))
        self._chk(sb, "Steiner tree R∪S (red, thick)",
                  self.show_steiner_tree, fg="#dc2626")
        self._sep(sb)

        # ============================================================ STEP 4
        self._heading(sb, "Step 4 — Proof of Thm 3.3")
        self._explain(sb, (
            "Proof that MST_R ≤ 2·OPT:\n"
            "a) Double Steiner tree edges (2·OPT)\n"
            "b) Euler tour on doubled graph\n"
            "c) Shortcut: skip S & repeats → HC on R\n"
            "   Tri. ineq: cost(HC) ≤ 2·OPT\n"
            "d) Remove edge → span. tree ≤ 2·OPT\n"
            "e) MST_R ≤ span. tree ≤ 2·OPT  ✓"))
        self._chk(sb, "4a. Doubled edges (indigo)",  self.show_doubled,
                  fg="#4f46e5")
        self._chk(sb, "4b. Euler tour (orange)",     self.show_euler,
                  fg="#d97706")
        self._chk(sb, "4c. Shortcut to R only (green)",
                  self.show_shortcut, fg="#059669")
        self._sep(sb)

        # ============================================================ STEP 5
        self._heading(sb, "Step 5 — Algorithm Output: MST on R")
        self._explain(sb, (
            "2-Approx algorithm simply computes\n"
            "MST on R (ignoring S). Guaranteed\n"
            "cost ≤ 2·OPT by Theorem 3.3.\n"
            "Compare blue MST vs red Steiner tree!"))
        self._chk(sb, "MST on R only (blue, bold)", self.show_mst_req,
                  fg="#2563eb")
        self._sep(sb)

        # ---- Results ----
        self._heading(sb, "Results")
        self.info_box = tk.Label(sb, text="", justify=tk.LEFT, bg="#e5e7eb",
                                 fg="#374151", font=("Consolas", 9),
                                 padx=10, pady=8, relief="groove",
                                 borderwidth=1, wraplength=300, anchor="nw")
        self.info_box.pack(fill=tk.X, pady=(2,8))
        self._info_welcome()

    # ---- sidebar helpers ----
    def _sep(self, p):
        tk.Frame(p, height=1, bg="#d1d5db").pack(fill=tk.X, pady=6)

    def _heading(self, p, txt):
        tk.Label(p, text=txt, font=("Arial", 10, "bold"),
                 bg="#f3f4f6", fg="#1f2937").pack(anchor="w", pady=(4,2))

    def _explain(self, p, txt):
        tk.Label(p, text=txt, font=("Arial", 8), bg="#f3f4f6",
                 fg="#6b7280", justify=tk.LEFT).pack(anchor="w", padx=(12,0))

    def _chk(self, p, txt, var, fg="#374151"):
        tk.Checkbutton(p, text=txt, variable=var, command=self.redraw,
                       bg="#f3f4f6", font=("Arial", 9, "bold"), fg=fg,
                       activebackground="#f3f4f6",
                       anchor="w").pack(fill=tk.X, pady=(1,0))

    # ================================================================= MODE
    def _set_mode(self, m):
        self.mode = m
        if m == 'R':
            self.btn_r.config(bg="#dbeafe", fg="#1d4ed8")
            self.btn_s.config(bg="white",   fg="#374151")
        else:
            self.btn_r.config(bg="white",   fg="#374151")
            self.btn_s.config(bg="#fee2e2", fg="#dc2626")

    # ================================================================= CANVAS
    def _on_click(self, e):
        self.points.append({'x': e.x, 'y': e.y,
                            'type': self.mode, 'id': len(self.points)})
        self.redraw()

    def _clear(self):
        self.points.clear()
        self.redraw()
        self._info_welcome()

    # ================================================================= HELPERS
    def _rp(self):
        return [p for p in self.points if p['type'] == 'R']

    def _sp(self):
        return [p for p in self.points if p['type'] == 'S']

    @staticmethod
    def dist(a, b):
        return math.hypot(a['x'] - b['x'], a['y'] - b['y'])

    # ---- Prim's MST ----
    def _mst(self, pts):
        """Return (edges_list, total_cost)."""
        n = len(pts)
        if n < 2:
            return [], 0.0
        INF = float('inf')
        vis   = [False] * n
        min_d = [INF]   * n
        par   = [-1]    * n
        min_d[0] = 0
        edges, cost = [], 0.0
        for _ in range(n):
            u = min((i for i in range(n) if not vis[i]),
                    key=lambda i: min_d[i], default=-1)
            if u < 0 or min_d[u] == INF:
                break
            vis[u] = True
            if par[u] >= 0:
                w = self.dist(pts[par[u]], pts[u])
                edges.append((pts[par[u]], pts[u], w))
                cost += w
            for v in range(n):
                if not vis[v]:
                    d = self.dist(pts[u], pts[v])
                    if d < min_d[v]:
                        min_d[v] = d
                        par[v] = u
        return edges, cost

    # ---- Steiner tree: MST on R∪S, prune S-only leaves ----
    def _steiner_tree(self, rp, sp):
        """Approximate OPT: MST on R∪S then prune S-leaves."""
        all_pts = rp + sp
        if len(all_pts) < 2 or not rp:
            return [], 0.0
        edges, _ = self._mst(all_pts)
        r_ids = {p['id'] for p in rp}
        # Build adjacency for pruning
        changed = True
        while changed:
            changed = False
            deg = {}
            for a, b, w in edges:
                deg[a['id']] = deg.get(a['id'], 0) + 1
                deg[b['id']] = deg.get(b['id'], 0) + 1
            new_edges = []
            for a, b, w in edges:
                # Remove edge if one endpoint is an S-leaf (degree 1 and type S)
                a_leaf = (a['id'] not in r_ids and deg.get(a['id'], 0) == 1)
                b_leaf = (b['id'] not in r_ids and deg.get(b['id'], 0) == 1)
                if a_leaf or b_leaf:
                    changed = True
                else:
                    new_edges.append((a, b, w))
            edges = new_edges
        cost = sum(w for _, _, w in edges)
        return edges, cost

    # ---- DFS-based walk on a tree (visits every edge twice = Euler walk on doubled tree) ----
    def _dfs_walk(self, pts_in_tree, tree_edges, start_id=None):
        """DFS walk on the tree: returns list of points visited (each edge traversed twice)."""
        if not tree_edges:
            return []
        adj = {}
        for a, b, _ in tree_edges:
            adj.setdefault(a['id'], []).append(b)
            adj.setdefault(b['id'], []).append(a)
        id_to_pt = {p['id']: p for p in pts_in_tree}
        # Pick start: prefer an R vertex
        if start_id is None:
            start_id = tree_edges[0][0]['id']
        path = []
        def dfs(uid, par_id):
            path.append(id_to_pt[uid])
            for nb in adj.get(uid, []):
                if nb['id'] != par_id:
                    dfs(nb['id'], uid)
                    path.append(id_to_pt[uid])
        dfs(start_id, -1)
        return path

    # ---- Drawing primitives ----
    def _edge(self, a, b, color, w, dash=None):
        self.canvas.create_line(a['x'], a['y'], b['x'], b['y'],
                                fill=color, width=w, dash=dash)

    def _label(self, a, b, color="#374151", bg="white", bd="#d1d5db", oy=0):
        if not self.show_distances.get():
            return
        mx = (a['x']+b['x'])/2
        my = (a['y']+b['y'])/2 + oy
        d = int(round(self.dist(a, b)))
        tid = self.canvas.create_text(mx, my, text=str(d),
                                      font=("Arial", 8, "bold"), fill=color)
        bb = self.canvas.bbox(tid)
        if bb:
            rid = self.canvas.create_rectangle(bb[0]-3, bb[1]-2,
                                               bb[2]+3, bb[3]+2,
                                               fill=bg, outline=bd, width=1)
            self.canvas.tag_raise(tid, rid)

    def _dot(self, p, txt, fill, r=8):
        x, y = p['x'], p['y']
        self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                fill=fill, outline="white", width=2)
        self.canvas.create_text(x, y, text=txt, fill="white",
                                font=("Arial", 9 if r >= 8 else 7, "bold"))

    # ================================================================= REDRAW
    def redraw(self):
        self.canvas.delete("all")
        rp  = self._rp()
        sp  = self._sp()
        all_pts = rp + sp
        r_ids = {p['id'] for p in rp}

        # ---- Layer 1: Complete graph (all R∪S edges) ----
        if self.show_complete.get() and len(all_pts) > 1:
            for i in range(len(all_pts)):
                for j in range(i+1, len(all_pts)):
                    a, b = all_pts[i], all_pts[j]
                    has_s = (a['type']=='S' or b['type']=='S')
                    c = "#f9a8d4" if has_s else "#e5e7eb"
                    self._edge(a, b, c, 1)
                    self._label(a, b, "#9ca3af", "#f9fafb", "#e5e7eb")

        # ---- Layer 2: Metric Closure G' on R (purple) ----
        if self.show_closure.get() and len(rp) > 1:
            for i in range(len(rp)):
                for j in range(i+1, len(rp)):
                    self._edge(rp[i], rp[j], "#a78bfa", 1.5)
                    self._label(rp[i], rp[j], "#7c3aed", "#ede9fe", "#a78bfa")

        # ---- Step 3: Steiner tree (≈ OPT) ----
        st_edges, st_cost = self._steiner_tree(rp, sp) if sp else ([], 0.0)

        if self.show_steiner_tree.get() and st_edges:
            for a, b, w in st_edges:
                self._edge(a, b, "#dc2626", 3.5)
                self._label(a, b, "#991b1b", "#fee2e2", "#fca5a5")

        # ---- Step 4a: Doubled edges of Steiner tree (indigo) ----
        if self.show_doubled.get() and st_edges:
            for a, b, w in st_edges:
                dx = b['x'] - a['x']
                dy = b['y'] - a['y']
                ln = math.hypot(dx, dy)
                if ln > 0:
                    px, py = -dy/ln*4, dx/ln*4
                    self.canvas.create_line(
                        a['x']+px, a['y']+py, b['x']+px, b['y']+py,
                        fill="#6366f1", width=2.5, dash=(6, 3))
                    self.canvas.create_line(
                        a['x']-px, a['y']-py, b['x']-px, b['y']-py,
                        fill="#818cf8", width=2.5, dash=(6, 3))

        # ---- Step 4b: Euler tour on doubled Steiner tree (orange) ----
        # Collect all points that appear in the Steiner tree
        st_pt_ids = set()
        for a, b, _ in st_edges:
            st_pt_ids.add(a['id'])
            st_pt_ids.add(b['id'])
        st_pts = [p for p in all_pts if p['id'] in st_pt_ids]

        # Find an R vertex as start for DFS
        start_id = None
        for p in rp:
            if p['id'] in st_pt_ids:
                start_id = p['id']
                break
        if start_id is None and st_pts:
            start_id = st_pts[0]['id']

        euler_walk = self._dfs_walk(st_pts, st_edges, start_id) if st_edges else []

        if self.show_euler.get() and len(euler_walk) > 1:
            for i in range(len(euler_walk)-1):
                a, b = euler_walk[i], euler_walk[i+1]
                self._edge(a, b, "#f59e0b", 2.5, dash=(5, 3))
            # Number the walk order
            for idx, p in enumerate(euler_walk):
                self.canvas.create_text(
                    p['x']+12, p['y']-12, text=str(idx),
                    font=("Arial", 7), fill="#b45309")

        # ---- Step 4c: Shortcut — skip S vertices → HC on R (green) ----
        shortcut_cost = 0.0
        shortcut_path = []
        if self.show_shortcut.get() and euler_walk:
            seen = set()
            for p in euler_walk:
                # Only keep Required vertices, skip Steiner and repeats
                if p['id'] in r_ids and p['id'] not in seen:
                    seen.add(p['id'])
                    shortcut_path.append(p)
            if len(shortcut_path) > 1:
                shortcut_path.append(shortcut_path[0])  # close the cycle
            for i in range(len(shortcut_path)-1):
                a, b = shortcut_path[i], shortcut_path[i+1]
                self._edge(a, b, "#10b981", 3.5)
                self._label(a, b, "#065f46", "#d1fae5", "#6ee7b7")
                shortcut_cost += self.dist(a, b)

        # ---- Step 5: MST on R only (blue) — the algorithm output ----
        mst_r_edges, mst_r_cost = self._mst(rp)

        if self.show_mst_req.get() and mst_r_edges:
            for a, b, w in mst_r_edges:
                self._edge(a, b, "#2563eb", 3)
                self._label(a, b, "#1e40af", "#dbeafe", "#93c5fd")

        # ---- Draw points on top ----
        for p in sp:
            # Highlight S vertices used in Steiner tree
            used = p['id'] in st_pt_ids and st_edges
            r = 8 if used else 6
            col = "#dc2626" if used else "#f87171"
            label = f"S{sp.index(p)+1}" if used else "s"
            self._dot(p, label, col, r)
        for i, p in enumerate(rp):
            self._dot(p, str(i+1), "#2563eb", 9)

        # ---- Update results box ----
        self._update_info(rp, sp, st_cost, mst_r_cost, shortcut_cost,
                          st_edges, euler_walk)

    # ================================================================= INFO
    def _info_welcome(self):
        self.info_box.config(text=(
            "Welcome!\n"
            "1. Click to place Required (blue)\n"
            "   or Steiner (red) points\n"
            "2. Follow Steps 1→5 in order\n"
            "3. See how Steiner points reduce cost\n"
            "   but MST_R is still within 2·OPT\n\n"
            "Key: c(u,v) ≤ c(u,w)+c(w,v)  [tri.ineq]\n"
            "     MST_R ≤ 2·OPT  [Thm 3.3]"))

    def _update_info(self, rp, sp, st_cost, mst_r_cost,
                     shortcut_cost, st_edges, euler_walk):
        L = []
        L.append(f"Required: {len(rp)}   Steiner: {len(sp)}")
        L.append("")

        if st_edges and st_cost > 0:
            L.append(f"Steiner tree (OPT):  {st_cost:.1f} px")
        if self.show_doubled.get() and st_cost > 0:
            L.append(f"  Doubled (2·OPT):   {2*st_cost:.1f} px")
        if self.show_euler.get() and euler_walk:
            L.append(f"  Euler walk steps:  {len(euler_walk)-1}")
        if self.show_shortcut.get() and shortcut_cost > 0:
            L.append(f"  Shortcut HC on R:  {shortcut_cost:.1f} px")
            if st_cost > 0:
                L.append(f"  Check: {shortcut_cost:.1f} ≤ {2*st_cost:.1f}?  "
                         + ("✓" if shortcut_cost <= 2*st_cost + 0.01 else "✗"))

        if self.show_mst_req.get() and len(rp) > 1:
            L.append(f"MST on R:            {mst_r_cost:.1f} px")

        if st_cost > 0 and mst_r_cost > 0:
            L.append("")
            L.append("─── Comparison ───")
            ratio = mst_r_cost / st_cost
            saving = mst_r_cost - st_cost
            L.append(f"Ratio MST_R/OPT: {ratio:.2f}")
            L.append(f"  Bound: {ratio:.2f} ≤ 2.00  "
                     + ("✓" if ratio <= 2.001 else "?"))
            if saving > 0:
                pct = saving/mst_r_cost*100
                L.append(f"  OPT saves {saving:.1f} ({pct:.0f}%)")
                L.append(f"  → Steiner hubs help!")
            else:
                L.append(f"  Steiner ≥ MST_R here")

        L.append("")
        L.append("─── Proof Chain (Thm 3.3) ───")
        L.append("OPT → ×2 → Euler → shortcut")
        L.append("→ HC on R → -edge → tree ≤ 2·OPT")
        L.append("MST_R ≤ tree ≤ 2·OPT  ✓")

        self.info_box.config(text="\n".join(L))


if __name__ == "__main__":
    root = tk.Tk()
    SteinerDemo(root)
    root.mainloop()

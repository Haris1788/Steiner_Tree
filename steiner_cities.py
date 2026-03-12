import tkinter as tk
from tkinter import font
import math

class CitySteinerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Seminar Demo: Steiner Tree Approximation")
        self.root.geometry("1200x800")

        # --- Data: Cities ---
        # Coordinates scaled for 800x600 canvas approx
        # Origin roughly Lower Saxony
        self.cities = [
            # Required (Blue)
            {'name': 'Berlin', 'x': 750, 'y': 100, 'type': 'R'},
            {'name': 'Hannover', 'x': 250, 'y': 200, 'type': 'R'},
            {'name': 'Braunschweig', 'x': 400, 'y': 220, 'type': 'R'},
            {'name': 'Wolfsburg', 'x': 450, 'y': 150, 'type': 'R'},
            {'name': 'Hildesheim', 'x': 280, 'y': 280, 'type': 'R'},
            {'name': 'Göttingen', 'x': 280, 'y': 500, 'type': 'R'},
            {'name': 'Goslar', 'x': 420, 'y': 350, 'type': 'R'},
            {'name': 'Clausthal', 'x': 400, 'y': 420, 'type': 'R'},
            
            # Steiner (Red)
            {'name': 'Wolfenbüttel', 'x': 400, 'y': 260, 'type': 'S'},
            {'name': 'Bad Harzburg', 'x': 450, 'y': 370, 'type': 'S'},
        ]
        
        # --- State ---
        self.show_closure = tk.BooleanVar(value=False)
        self.show_mst = tk.BooleanVar(value=False)
        self.show_euler = tk.BooleanVar(value=False)
        self.show_shortcuts = tk.BooleanVar(value=False)

        # --- Layout ---
        self.sidebar = tk.Frame(root, width=350, bg="#f8fafc", padx=20, pady=20)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.canvas_frame = tk.Frame(root, bg="white")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar()
        self.redraw()

    def _build_sidebar(self):
        # Title
        tk.Label(self.sidebar, text="Seminar Demo", font=("Helvetica", 12, "bold"), bg="#f8fafc", fg="#64748b").pack(anchor="w")
        tk.Label(self.sidebar, text="Steiner Tree & TSP", font=("Helvetica", 20, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w", pady=(0, 20))

        # Legend
        legend_frame = tk.Frame(self.sidebar, bg="#e2e8f0", padx=10, pady=10)
        legend_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(legend_frame, text="Legend", font=("Helvetica", 10, "bold"), bg="#e2e8f0").pack(anchor="w")
        
        r_row = tk.Frame(legend_frame, bg="#e2e8f0")
        r_row.pack(fill=tk.X, pady=2)
        tk.Frame(r_row, width=12, height=12, bg="#2563eb").pack(side=tk.LEFT)
        tk.Label(r_row, text="  Required (8 Cities)", bg="#e2e8f0").pack(side=tk.LEFT)

        s_row = tk.Frame(legend_frame, bg="#e2e8f0")
        s_row.pack(fill=tk.X, pady=2)
        tk.Frame(s_row, width=12, height=12, bg="#ef4444").pack(side=tk.LEFT)
        tk.Label(s_row, text="  Steiner points (2 Cities)", bg="#e2e8f0").pack(side=tk.LEFT)
        tk.Label(s_row, text="  (Ignored by Approx Algo)", font=("Helvetica", 8, "italic"), bg="#e2e8f0").pack(side=tk.LEFT)


        # Controls
        tk.Label(self.sidebar, text="Demonstration Steps", font=("Helvetica", 14, "bold"), bg="#f8fafc", fg="#334155").pack(anchor="w", pady=(10, 10))

        self._add_step("1. Metric Closure on R", self.show_closure, 
                       "Connect all Required cities.\nCalculates pairwise Euclidean distances.\n(Theorem 3.2)")

        self._add_step("2. MST on Required", self.show_mst, 
                       "Find Minimum Spanning Tree of R.\nThis is our 2-Approximation.\nNotice: It bypasses Steiner nodes.")

        self._add_step("3. Euler Tour", self.show_euler, 
                       "Duplicate edges to make graph Eulerian.\nPerform DFS traversal.")

        self._add_step("4. Shortcut Tour", self.show_shortcuts, 
                       "Shortcut duplicates to get Hamiltonian Cycle.\nCost <= 2 * OPT.")

        # Stats
        self.stats_label = tk.Label(self.sidebar, text="", font=("Consolas", 10), bg="#f1f5f9", justify=tk.LEFT, padx=10, pady=10, relief="solid", borderwidth=0)
        self.stats_label.pack(fill=tk.X, side=tk.BOTTOM, pady=20)


    def _add_step(self, text, var, desc):
        f = tk.Frame(self.sidebar, bg="#f8fafc", pady=5)
        f.pack(fill=tk.X)
        
        chk = tk.Checkbutton(f, text=text, variable=var, command=self.redraw, 
                             font=("Helvetica", 11, "bold"), bg="#f8fafc", activebackground="#f8fafc", anchor="w")
        chk.pack(fill=tk.X, anchor="w")
        
        lbl = tk.Label(f, text=desc, font=("Helvetica", 9), bg="#f8fafc", fg="#64748b", justify=tk.LEFT)
        lbl.pack(fill=tk.X, anchor="w", padx=(25, 0))

    def dist(self, p1, p2):
        return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

    def draw_edge_label(self, p1, p2, text, color="#64748b"):
        mx, my = (p1['x'] + p2['x']) / 2, (p1['y'] + p2['y']) / 2
        
        # Simple background
        t_id = self.canvas.create_text(mx, my, text=text, font=("Arial", 8, "bold"), fill=color)
        bbox = self.canvas.bbox(t_id)
        if bbox:
            self.canvas.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2, fill="white", outline="", tags="bg")
            self.canvas.tag_lower("bg", t_id)

    def redraw(self):
        self.canvas.delete("all")
        
        req = [c for c in self.cities if c['type'] == 'R']
        steiner = [c for c in self.cities if c['type'] == 'S']

        # 1. Closure
        if self.show_closure.get():
            for i in range(len(req)):
                for j in range(i+1, len(req)):
                    d = self.dist(req[i], req[j])
                    self.canvas.create_line(req[i]['x'], req[i]['y'], req[j]['x'], req[j]['y'], fill="#e2e8f0", width=1)
                    # Show limited labels to avoid clutter? Or all? 
                    # For demo, maybe only show nearby ones or just faint text
                    self.draw_edge_label(req[i], req[j], f"{int(d)}", "#cbd5e1")

        # MST Logic
        mst_cost = 0
        mst_edges = []
        if self.show_mst.get() or self.show_euler.get() or self.show_shortcuts.get():
            # Prim's
            n = len(req)
            visited = [False]*n
            min_dist = [float('inf')]*n
            parent = [-1]*n
            min_dist[0] = 0
            
            for _ in range(n):
                u = -1
                for i in range(n):
                    if not visited[i] and (u == -1 or min_dist[i] < min_dist[u]):
                        u = i
                if min_dist[u] == float('inf'): break
                visited[u] = True
                
                if parent[u] != -1:
                    u_node = req[parent[u]]
                    v_node = req[u]
                    d = self.dist(u_node, v_node)
                    mst_edges.append((u_node, v_node))
                    mst_cost += d
                
                for v in range(n):
                    if not visited[v]:
                        d = self.dist(req[u], req[v])
                        if d < min_dist[v]:
                            min_dist[v] = d
                            parent[v] = u

        # 2. Draw MST
        if self.show_mst.get():
            for u, v in mst_edges:
                self.canvas.create_line(u['x'], u['y'], v['x'], v['y'], fill="#2563eb", width=3)
                self.draw_edge_label(u, v, f"{int(self.dist(u,v))}", "#1e40af")

        # 3. Euler
        euler_tour = []
        if self.show_euler.get() or self.show_shortcuts.get():
             # DFS
             adj = {c['name']: [] for c in req}
             for u, v in mst_edges:
                 adj[u['name']].append(v)
                 adj[v['name']].append(u)
             
             path = []
             def dfs(u, p_name):
                 path.append(u)
                 for v in adj[u['name']]:
                     if v['name'] != p_name:
                         dfs(v, u['name'])
                         path.append(u)
             
             if req: dfs(req[0], None)
             euler_tour = path

        if self.show_euler.get():
            for i in range(len(euler_tour)-1):
                u, v = euler_tour[i], euler_tour[i+1]
                # Offset dash
                self.canvas.create_line(u['x'], u['y'], v['x'], v['y'], fill="#f59e0b", width=2, dash=(5,5))

        # 4. Shortcut
        shortcut_cost = 0
        if self.show_shortcuts.get() and euler_tour:
            visited = set()
            sc_path = []
            for c in euler_tour:
                if c['name'] not in visited:
                    visited.add(c['name'])
                    sc_path.append(c)
            if len(sc_path) > 1: sc_path.append(sc_path[0])
            
            for i in range(len(sc_path)-1):
                u, v = sc_path[i], sc_path[i+1]
                self.canvas.create_line(u['x'], u['y'], v['x'], v['y'], fill="#10b981", width=4)
                shortcut_cost += self.dist(u, v)

        # Draw Nodes
        for c in self.cities:
            color = "#ef4444" if c['type'] == 'S' else "#2563eb"
            r = 8 if c['type'] == 'R' else 5
            self.canvas.create_oval(c['x']-r, c['y']-r, c['x']+r, c['y']+r, fill=color, outline="white", width=2)
            
            # Labels
            offset_y = -20 if c['y'] < 400 else 20
            font_s = ("Helvetica", 10, "bold") if c['type'] == 'R' else ("Helvetica", 9, "italic")
            txt_col = "black" if c['type'] == 'R' else "#64748b"
            self.canvas.create_text(c['x'], c['y']+offset_y, text=c['name'], font=font_s, fill=txt_col)

        # Update stats
        info = f"Required Cities: {len(req)}\nSteiner Candidates: {len(steiner)}\n\n"
        if self.show_mst.get():
            info += f"MST Cost: {mst_cost:.0f} (units)\n"
        if self.show_shortcuts.get():
            info += f"Shortcut Tour: {shortcut_cost:.0f} (units)"
        self.stats_label.config(text=info)

if __name__ == "__main__":
    root = tk.Tk()
    app = CitySteinerDemo(root)
    root.mainloop()

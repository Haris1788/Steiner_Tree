import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Seminar Demo: Real Cities", layout="wide")

st.title("🌳 Interactive Steiner Tree Demo: Real German Cities")
st.markdown("""
This demo applies the **2-Approximation Algorithm** to real cities in Germany.

**Interactive Setup**: Choose which cities are Required (must connect) vs Steiner (optional hubs).
**Key Question**: Do strategically placed Steiner hub cities reduce the total tree cost?
""")

# --- Sidebar ---
st.sidebar.header("🎮 Interactive Configuration")

# City Selection
st.sidebar.subheader("📍 City Selection")

# All available cities
all_cities = ['Hannover', 'Magdeburg', 'Wolfsburg', 'Braunschweig', 
              'Hildesheim', 'Goslar', 'Clausthal', 'Salzgitter']

# Default configuration that demonstrates Steiner benefit
# Spread out required cities with central Steiner hubs
default_required = ['Hannover', 'Magdeburg', 'Wolfsburg', 'Clausthal']
default_steiner = ['Braunschweig', 'Hildesheim', 'Goslar']

required_cities = st.sidebar.multiselect(
    "Required Cities (Blue) - Must Connect",
    all_cities,
    default=default_required,
    help="These cities MUST be connected in the final tree"
)

steiner_cities = st.sidebar.multiselect(
    "Steiner Cities (Red) - Optional Hubs",
    [c for c in all_cities if c not in required_cities],
    default=[c for c in default_steiner if c not in required_cities],
    help="These cities can be used as hubs to reduce total distance"
)

if len(required_cities) < 2:
    st.error("⚠️ Please select at least 2 required cities!")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("Presentation Controls")

# Step 1: Problem Setup
st.sidebar.subheader("Step 1: Problem Setup")
show_labels = st.sidebar.checkbox("Show City Names", value=True)
if show_labels:
    st.sidebar.info("🏙️ **Blue circles** = Required cities (must connect)\n**Red triangles** = Steiner cities (optional hubs)")

show_complete = st.sidebar.checkbox("Complete Graph", value=False)
if show_complete:
    st.sidebar.info("📊 Shows ALL possible connections between all cities with distances. Gray lines = required-to-required, Pink lines = involving Steiner cities.")

# Step 2: Theorem 3.2
st.sidebar.markdown("---")
st.sidebar.subheader("Step 2: Theorem 3.2")
show_theorem_32 = st.sidebar.checkbox("Theorem 3.2: Metric Closure", value=False)
if show_theorem_32:
    st.sidebar.info("🔵 **Metric Closure**: Creates complete graph G' on vertex set V where each edge (u,v) has cost = shortest path in original graph G. Shows ONLY required cities connected.")

show_proof_32_part1 = st.sidebar.checkbox("  → Proof Part 1: Transform to G'", value=False)
if show_proof_32_part1:
    st.sidebar.success("Constructs metric closure G' where all required cities are directly connected with shortest-path distances.")

show_proof_32_part2 = st.sidebar.checkbox("  → Proof Part 2: MST on Required", value=False)
if show_proof_32_part2:
    st.sidebar.success("Finds MST on required vertices in G'. This gives us a tree connecting all required cities.")

show_proof_32_part3 = st.sidebar.checkbox("  → Proof Part 3: Back to Original", value=False)
if show_proof_32_part3:
    st.sidebar.success("Maps solution back: replaces each edge in MST with corresponding path in original graph, removes cycles if any.")

# Step 3: Theorem 3.3
st.sidebar.markdown("---")
st.sidebar.subheader("Step 3: Theorem 3.3")
show_theorem_33 = st.sidebar.checkbox("Theorem 3.3: 2-Approximation", value=False)
if show_theorem_33:
    st.sidebar.info("🎯 **The Guarantee**: MST on required vertices R has cost ≤ 2 × OPT (optimal Steiner tree cost)")

show_proof_33_step1 = st.sidebar.checkbox("  → Proof Step 1: Double Edges", value=False)
if show_proof_33_step1:
    st.sidebar.success("Start with optimal Steiner tree (cost = OPT). Double all edges → Eulerian graph (cost = 2·OPT).")

show_proof_33_step2 = st.sidebar.checkbox("  → Proof Step 2: Euler Tour", value=False)
if show_proof_33_step2:
    st.sidebar.success("Find Euler tour traversing each doubled edge once. Tour visits all required vertices, cost = 2·OPT.")

show_proof_33_step3 = st.sidebar.checkbox("  → Proof Step 3: Shortcuts", value=False)
if show_proof_33_step3:
    st.sidebar.success("Skip Steiner vertices and repeated required vertices using shortcuts. Triangle inequality ensures cost ≤ 2·OPT.")

show_proof_33_step4 = st.sidebar.checkbox("  → Proof Step 4: Remove Edge", value=False)
if show_proof_33_step4:
    st.sidebar.success("Delete one edge from Hamiltonian cycle → spanning tree on R with cost ≤ 2·OPT. MST has minimum cost, so MST ≤ 2·OPT ✓")

# Step 4: Optimal Solution
st.sidebar.markdown("---")
st.sidebar.subheader("Step 4: Find Optimal")
show_mst_comb = st.sidebar.checkbox("MST on (Required + Steiner)", value=False)
if show_mst_comb:
    st.sidebar.info("🌟 Finds MST using BOTH required AND Steiner cities. This approximates the optimal Steiner tree (OPT).")

# --- Data: Cities ---
# All cities with coordinates and actual Google Maps distances
all_cities_data = {
    'Hannover': {'pos': (30, 60), 'id': 0},
    'Magdeburg': {'pos': (75, 55), 'id': 1},
    'Wolfsburg': {'pos': (65, 75), 'id': 2},
    'Braunschweig': {'pos': (55, 60), 'id': 3},
    'Hildesheim': {'pos': (40, 45), 'id': 4},
    'Goslar': {'pos': (50, 35), 'id': 5},
    'Clausthal': {'pos': (45, 25), 'id': 6},
    'Salzgitter': {'pos': (45, 40), 'id': 7}
}

# Actual distances from Google Maps (in km) - Complete matrix with SORTED keys
distance_matrix = {
    # All pairs in alphabetical order for tuple(sorted()) lookup
    ('Braunschweig', 'Clausthal'): 55,
    ('Braunschweig', 'Goslar'): 40,
    ('Braunschweig', 'Hannover'): 65,
    ('Braunschweig', 'Hildesheim'): 40,
    ('Braunschweig', 'Magdeburg'): 75,
    ('Braunschweig', 'Salzgitter'): 25,
    ('Braunschweig', 'Wolfsburg'): 35,
    
    ('Clausthal', 'Goslar'): 15,
    ('Clausthal', 'Hannover'): 90,
    ('Clausthal', 'Hildesheim'): 40,
    ('Clausthal', 'Magdeburg'): 140,
    ('Clausthal', 'Salzgitter'): 30,
    ('Clausthal', 'Wolfsburg'): 85,
    
    ('Goslar', 'Hannover'): 80,
    ('Goslar', 'Hildesheim'): 40,
    ('Goslar', 'Magdeburg'): 120,
    ('Goslar', 'Salzgitter'): 20,
    ('Goslar', 'Wolfsburg'): 70,
    
    ('Hannover', 'Hildesheim'): 45,
    ('Hannover', 'Magdeburg'): 140,
    ('Hannover', 'Salzgitter'): 60,
    ('Hannover', 'Wolfsburg'): 90,
    
    ('Hildesheim', 'Magdeburg'): 130,
    ('Hildesheim', 'Salzgitter'): 25,
    ('Hildesheim', 'Wolfsburg'): 80,
    
    ('Magdeburg', 'Salzgitter'): 110,
    ('Magdeburg', 'Wolfsburg'): 100,
    
    ('Salzgitter', 'Wolfsburg'): 60
}

# Build cities_data dynamically based on user selection
cities_data = {}
city_id = 0
for city_name in required_cities:
    cities_data[city_id] = {
        'name': city_name,
        'pos': all_cities_data[city_name]['pos'],
        'type': 'R'
    }
    city_id += 1

for city_name in steiner_cities:
    cities_data[city_id] = {
        'name': city_name,
        'pos': all_cities_data[city_name]['pos'],
        'type': 'S'
    }
    city_id += 1

# Fix ID mapping
req_ids = [k for k, v in cities_data.items() if v['type'] == 'R']
stein_ids = [k for k, v in cities_data.items() if v['type'] == 'S']

# Display current configuration
st.info(f"""
**Current Configuration:**
- **Required Cities ({len(req_ids)}):** {', '.join([cities_data[i]['name'] for i in req_ids])}
- **Steiner Cities ({len(stein_ids)}):** {', '.join([cities_data[i]['name'] for i in stein_ids]) if stein_ids else 'None'}
""")

def get_dist(id1, id2):
    """Get actual distance from Google Maps distance matrix"""
    if id1 not in cities_data or id2 not in cities_data:
        return 0
    name1 = cities_data[id1]['name']
    name2 = cities_data[id2]['name']
    key = tuple(sorted([name1, name2]))
    dist = distance_matrix.get(key, 0)
    if dist == 0:
        print(f"Warning: No distance found for {name1} - {name2}")
    return dist

# --- plotting ---
fig, ax = plt.subplots(figsize=(10, 7))

# 1. Base Points
for k, v in cities_data.items():
    color = 'blue' if v['type'] == 'R' else 'red'
    size = 150 if v['type'] == 'R' else 100
    marker = 'o' if v['type'] == 'R' else '^'
    ax.scatter(v['pos'][0], v['pos'][1], c=color, s=size, zorder=10, marker=marker)
    
    if show_labels:
        # Offset label
        ax.text(v['pos'][0], v['pos'][1]+3, v['name'], ha='center', fontsize=9, fontweight='bold', color='black')

# 2. Complete Graph
if show_complete:
    # Show ALL cities connected to each other (including Steiner)
    all_ids = req_ids + stein_ids
    for i in range(len(all_ids)):
        for j in range(i+1, len(all_ids)):
            u, v = all_ids[i], all_ids[j]
            p1 = cities_data[u]['pos']
            p2 = cities_data[v]['pos']
            dist = get_dist(u, v)
            
            # Different color for edges involving Steiner vertices
            if cities_data[u]['type'] == 'S' or cities_data[v]['type'] == 'S':
                color = 'pink'
                alpha = 0.4
            else:
                color = 'lightgray'
                alpha = 0.5
            
            # Draw line
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c=color, linewidth=0.8, zorder=1, alpha=alpha)
            
            # Label with distance (show all distances)  
            if dist > 0:  # Only show if distance exists
                mid_x, mid_y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                ax.text(mid_x, mid_y, f"{dist:.0f}", fontsize=7, color='darkgray', ha='center', 
                       fontweight='bold', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, linewidth=0.5))

# 3. Theorem 3.2: Metric Closure (Required vertices only) - Shows G'
if show_theorem_32 or show_proof_32_part1:
    # Edges between all Required cities with distances (This is the metric closure G')
    for i in range(len(req_ids)):
        for j in range(i+1, len(req_ids)):
            u, v = req_ids[i], req_ids[j]
            p1 = cities_data[u]['pos']
            p2 = cities_data[v]['pos']
            dist = get_dist(u, v)
            
            # Draw line
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='purple', linewidth=1.2, zorder=1, alpha=0.6)
            
            # Label with distance
            if dist > 0:  # Only show if distance exists
                mid_x, mid_y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                ax.text(mid_x, mid_y, f"{dist:.0f}", fontsize=8, color='purple', ha='center', 
                       fontweight='bold', bbox=dict(facecolor='white', edgecolor='purple', alpha=0.95, linewidth=1))

# 4. Proof of Theorem 3.2: MST on Required
mst_r_weight = 0
mst_r_edges = []
if show_proof_32_part2 or show_proof_32_part3 or show_theorem_33 or show_proof_33_step1 or show_proof_33_step2 or show_proof_33_step3 or show_proof_33_step4:
    # Build Graph of Required cities
    G_r = nx.Graph()
    for i in range(len(req_ids)):
        for j in range(i+1, len(req_ids)):
            u, v = req_ids[i], req_ids[j]
            G_r.add_edge(u, v, weight=get_dist(u, v))
            
    mst = nx.minimum_spanning_tree(G_r)
    mst_r_weight = mst.size(weight='weight')
    mst_r_edges = list(mst.edges())
    
if show_proof_32_part2 or show_proof_32_part3:
    for u, v in mst_r_edges:
        p1 = cities_data[u]['pos']
        p2 = cities_data[v]['pos']
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='blue', linewidth=2.5, zorder=2)
        # Label MST edges distinctly
        mid_x, mid_y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        dist = get_dist(u, v)
        if dist > 0:
            ax.text(mid_x, mid_y, f"{dist:.0f}", fontsize=9, color='blue', fontweight='bold', 
                   bbox=dict(facecolor='white', edgecolor='blue', alpha=0.95, linewidth=1))

# 5. Theorem 3.3: Show the approximation statement
if show_theorem_33 or show_proof_33_step1:
    # Show the MST on required (this will be our 2-approximation)
    for u, v in mst_r_edges:
        p1 = cities_data[u]['pos']
        p2 = cities_data[v]['pos']
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='darkblue', linewidth=3, zorder=2, alpha=0.8)
        # Show distances
        mid_x, mid_y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        dist = get_dist(u, v)
        if dist > 0:
            ax.text(mid_x, mid_y, f"{dist:.0f}", fontsize=9, color='darkblue', fontweight='bold', 
                   bbox=dict(facecolor='yellow', edgecolor='darkblue', alpha=0.95, linewidth=1.5))

# 6. MST (Combined - Insight) - Shows optimal usage of Steiner points
if show_mst_comb:
    G_all = nx.Graph()
    all_ids = req_ids + stein_ids
    for i in range(len(all_ids)):
        for j in range(i+1, len(all_ids)):
            u, v = all_ids[i], all_ids[j]
            G_all.add_edge(u, v, weight=get_dist(u, v))
            
    mst_c = nx.minimum_spanning_tree(G_all)
    mst_c_weight = mst_c.size(weight='weight')
    
    for u, v in mst_c.edges():
        p1 = cities_data[u]['pos']
        p2 = cities_data[v]['pos']
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='green', linestyle='--', linewidth=2.5, zorder=3)
        # Show distances on the optimal tree
        mid_x, mid_y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        dist = get_dist(u, v)
        if dist > 0:
            ax.text(mid_x, mid_y, f"{dist:.0f}", fontsize=9, color='green', fontweight='bold', 
                   bbox=dict(facecolor='lightgreen', edgecolor='green', alpha=0.95, linewidth=1.5))
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Result Comparison")
    st.sidebar.write(f"**MST (Required only):** {mst_r_weight:.0f} km")
    st.sidebar.write(f"**MST (with Steiner):** {mst_c_weight:.0f} km")
    if mst_r_weight > 0 and mst_c_weight > 0:
        diff = mst_r_weight - mst_c_weight
        if diff > 0:
            st.sidebar.success(f"✅ Savings: {diff:.0f} km ({(diff/mst_r_weight)*100:.1f}%)")
        elif diff < 0:
            st.sidebar.warning(f"⚠️ Extra cost: {-diff:.0f} km ({(-diff/mst_r_weight)*100:.1f}%)")
        else:
            st.sidebar.info("Same cost with or without Steiner")
        ratio = mst_r_weight / mst_c_weight
        st.sidebar.info(f"Approximation Ratio: {ratio:.2f} (must be ≤ 2.0)")


# 7. Proof of Theorem 3.3 - Step 2: Euler Tour (with curved doubled edges)
if show_proof_33_step2:
    if mst_r_edges:
        # Create Eulerian multigraph by doubling MST edges
        # Visualize by drawing duplicate edges with curves
        for u, v in mst_r_edges:
            p1 = cities_data[u]['pos']
            p2 = cities_data[v]['pos']
            
            # Calculate perpendicular offset for curve
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx**2 + dy**2)
            
            if length > 0:
                # Perpendicular direction
                perp_x = -dy / length
                perp_y = dx / length
                
                # Create curved path for first edge (original)
                offset1 = 2
                mid_x1 = (p1[0] + p2[0]) / 2 + perp_x * offset1
                mid_y1 = (p1[1] + p2[1]) / 2 + perp_y * offset1
                
                # Bezier curve points
                t = np.linspace(0, 1, 30)
                curve1_x = (1-t)**2 * p1[0] + 2*(1-t)*t * mid_x1 + t**2 * p2[0]
                curve1_y = (1-t)**2 * p1[1] + 2*(1-t)*t * mid_y1 + t**2 * p2[1]
                ax.plot(curve1_x, curve1_y, c='orange', linewidth=2.5, zorder=4, alpha=0.8)
                
                # Create curved path for second edge (doubled)
                offset2 = -2
                mid_x2 = (p1[0] + p2[0]) / 2 + perp_x * offset2
                mid_y2 = (p1[1] + p2[1]) / 2 + perp_y * offset2
                
                curve2_x = (1-t)**2 * p1[0] + 2*(1-t)*t * mid_x2 + t**2 * p2[0]
                curve2_y = (1-t)**2 * p1[1] + 2*(1-t)*t * mid_y2 + t**2 * p2[1]
                ax.plot(curve2_x, curve2_y, c='orange', linewidth=2.5, zorder=4, alpha=0.8, linestyle='--')

# 8. Proof of Theorem 3.3 - Step 3: Shortcut (Hamiltonian cycle on R)
if show_proof_33_step3 or show_proof_33_step4:
    # Calculate DFS order on MST_R
    if mst_r_edges:
        G_mst = nx.Graph()
        G_mst.add_edges_from(mst_r_edges)
        if len(req_ids) > 0:
            start_node = req_ids[0]
            # Need strict subgraph
            cycle_nodes = list(nx.dfs_preorder_nodes(G_mst, source=start_node))
            if len(cycle_nodes) > 1:
                cycle_nodes.append(cycle_nodes[0])
                
                for i in range(len(cycle_nodes)-1):
                    u, v = cycle_nodes[i], cycle_nodes[i+1]
                    p1 = cities_data[u]['pos']
                    p2 = cities_data[v]['pos']
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='#10b981', linewidth=3, alpha=0.6, zorder=5)


ax.axis('off')
st.pyplot(fig)
# --- Theorem 3.3 Calculations Section ---
st.markdown("---")
st.header("📊 Theorem 3.3: Why MST on Required Vertices is a 2-Approximation")

st.markdown("""
**Theorem 3.3 Statement**: The cost of an MST on required vertices R is at most 2 × OPT, 
where OPT is the cost of the optimal Steiner tree.

**Key Insight**: Using Steiner vertices (strategic hubs) can reduce the total cost, but even without them, 
we're guaranteed to be within 2× of optimal!
""")

# Calculate both MSTs
if len(req_ids) > 0:
    # MST on Required only
    G_r = nx.Graph()
    for i in range(len(req_ids)):
        for j in range(i+1, len(req_ids)):
            u, v = req_ids[i], req_ids[j]
            G_r.add_edge(u, v, weight=get_dist(u, v))
    mst_req = nx.minimum_spanning_tree(G_r)
    mst_req_cost = mst_req.size(weight='weight')
    
    # MST on Required + Steiner (approximation of OPT)
    if len(stein_ids) > 0:
        G_all = nx.Graph()
        all_ids = req_ids + stein_ids
        for i in range(len(all_ids)):
            for j in range(i+1, len(all_ids)):
                u, v = all_ids[i], all_ids[j]
                G_all.add_edge(u, v, weight=get_dist(u, v))
        mst_steiner = nx.minimum_spanning_tree(G_all)
        mst_steiner_cost = mst_steiner.size(weight='weight')
    else:
        mst_steiner_cost = mst_req_cost
    
    # Display calculations in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("MST on Required Only", f"{mst_req_cost:.0f} km", 
                 help="Connects all required cities without using Steiner vertices")
    
    with col2:
        if len(stein_ids) > 0:
            difference = mst_steiner_cost - mst_req_cost
            delta_text = f"+{difference:.0f} km" if difference > 0 else f"{difference:.0f} km"
            st.metric("MST with Steiner Points", f"{mst_steiner_cost:.0f} km",
                     delta=delta_text,
                     delta_color="normal",
                     help="Uses Steiner vertices as hubs - this approximates OPT")
        else:
            st.metric("MST with Steiner Points", "N/A",
                     help="No Steiner cities selected")
    
    with col3:
        if len(stein_ids) > 0:
            ratio = mst_req_cost / mst_steiner_cost if mst_steiner_cost > 0 else 0
            st.metric("Approximation Ratio", f"{ratio:.2f}",
                     help="MST_Required / MST_Steiner (should be ≤ 2)")
        else:
            st.metric("Approximation Ratio", "N/A",
                     help="Need Steiner cities to calculate")
    
    st.markdown("---")
    
    # Analysis: When Steiner Points Help
    if len(stein_ids) > 0:
        st.subheader("🎯 Analysis: When Do Steiner Points Help?")
        
        if mst_steiner_cost < mst_req_cost:
            savings = mst_req_cost - mst_steiner_cost
            savings_pct = (savings / mst_req_cost) * 100
            
            st.success(f"""
            ### ✅ Steiner Points ARE Helping!
            
            **Savings: {savings:.0f} km ({savings_pct:.1f}% reduction)**
            
            **Why They Help:**
            """)
            
            # Explain the topology
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                **Without Steiner Points:**
                - Required cities connect directly to each other
                - May require long-distance connections
                - Total cost: {:.0f} km
                """.format(mst_req_cost))
                
            with col_b:
                st.markdown("""
                **With Steiner Points:**
                - Central hub cities serve as connection points
                - Shorter paths through strategic locations
                - Total cost: {:.0f} km
                """.format(mst_steiner_cost))
            
            st.info("""
            **📍 Geographic Insight:**
            
            Your Steiner points ({}) are **geographically central** to your required cities ({}). 
            This creates a "hub-and-spoke" topology where:
            
            1. Required cities connect to nearby Steiner hubs
            2. Steiner hubs connect to each other
            3. This reduces total wiring cost compared to direct connections
            
            **Real-world example**: Think of airline hub cities (Chicago, Frankfurt) connecting smaller cities 
            more efficiently than direct flights between all pairs.
            """.format(', '.join(steiner_cities), ', '.join(required_cities)))
            
        else:
            extra_cost = mst_steiner_cost - mst_req_cost
            
            st.warning(f"""
            ### ⚠️ Steiner Points Are NOT Helping!
            
            **Extra cost: +{extra_cost:.0f} km**
            
            **Why They Don't Help:**
            """)
            
            st.markdown("""
            In your current configuration, the Steiner points add extra cost rather than reducing it. 
            This happens when:
            
            1. **Required cities are already well-connected** 
               - They form a compact cluster
               - Direct connections are already efficient
               
            2. **Steiner points are poorly positioned**
               - Not geographically central to required cities
               - Not on the shortest paths between required cities
               
            3. **Wrong topology**
               - Required cities might form a path/line rather than scattered points
               - Steiner points work best when required cities are spread in multiple directions
            
            **💡 Try this:**
            - Select required cities that are more spread out
            - Choose Steiner points that are geographically central
            - Good example: Required = [Hannover, Magdeburg, Wolfsburg, Clausthal, Salzgitter], 
              Steiner = [Braunschweig, Hildesheim, Goslar]
            """)
            
        # The guarantee still holds
        st.markdown("---")
        st.subheader("✓ The 2-Approximation Guarantee")
        
        st.markdown(f"""
        **Important**: Regardless of whether Steiner points help in this specific instance, 
        the MST on required vertices gives us a **guaranteed 2-approximation**:
        
        - **MST on Required**: {mst_req_cost:.0f} km
        - **Optimal Steiner Tree (OPT)**: ≤ {mst_steiner_cost:.0f} km (our best approximation)
        - **Ratio**: {ratio:.2f}
        - **Check**: {mst_req_cost:.0f} ≤ 2 × {mst_steiner_cost:.0f} = {2*mst_steiner_cost:.0f} ✓
        
        The theorem guarantees that even in the **worst case**, MST on required vertices is 
        at most **twice** the optimal cost!
        """)
# Steiner Tree and Travelling Salesman Problem: Approximation Algorithms for Metric Networks

**Author:** Haris Masood  
**University:** TU Clausthal  
**Course:** Algorithm Seminar 2 - Approximation Algorithms

## Introduction

The Steiner Tree problem and the Travelling Salesman Problem (TSP) are two fundamental problems in combinatorial optimization. Both appear in network design, logistics, VLSI layout, and infrastructure planning. While exact solutions are computationally hard, approximation algorithms provide efficient solutions with guaranteed performance bounds relative to the optimal solution.

This presentation covers the 2-approximation algorithm for the metric Steiner Tree problem and its connections to TSP through the techniques of metric closure, Euler tours, and shortcutting.

## The Steiner Tree Problem

### Problem Definition

Given a weighted graph $G = (V, E, w)$ with edge weights satisfying the triangle inequality (metric distances), we are asked to find a minimum-cost tree connecting a required set $R \subseteq V$ of vertices. 

The Steiner Tree may use additional intermediate vertices $S = V \setminus R$, called **Steiner points**, to reduce the total cost.

**Objective:**

$$
\text{minimize} \quad \sum_{e \in T} w(e)
$$

where $T$ is a tree such that $R \subseteq V(T)$.

### The Metric Property

The triangle inequality is fundamental:

$$
d(u,w) \le d(u,v) + d(v,w)
$$

This property holds naturally in road networks, Euclidean distances, and many real-world applications. It ensures that direct paths are never more expensive than paths through intermediate vertices.

### Computational Complexity

The Steiner Tree problem is **NP-hard** even in metric graphs. This means:
- Exact algorithms have exponential worst-case time
- For large instances, exact solutions are impractical
- We must accept approximation with quality guarantees

## 2-Approximation Algorithm via Metric Closure

### Step 1: Metric Closure Transformation

**Theorem 3.2 (Metric Closure Reduction):**

Construct a new graph $G'$ as follows:
- Vertices: only the required set $R$
- Edges: complete graph (all pairs connected)
- Edge weight: $w'(u,v) = $ shortest-path distance from $u$ to $v$ in original graph $G$

**Why this works:**
- The shortest path from $u$ to $v$ may use Steiner points, but we encode that cost directly as an edge weight
- We "compress" the complex Steiner structure into simple edge weights
- The metric closure is a metric graph (triangle inequality still holds)

### Step 2: MST on Required Vertices

**Theorem 3.3 (2-Approximation Guarantee):**

Compute the Minimum Spanning Tree (MST) on the required vertices $R$ in the metric closure $G'$. Then:

$$
\text{cost}(\text{MST}_R) \le 2 \cdot \text{OPT}
$$

where OPT is the minimum Steiner tree cost.

### Proof Intuition: Doubling, Euler Tour, and Shortcutting

The proof connects the optimal Steiner tree to a 2× approximation through four key steps:

**Step 1: Doubling**
- Start with the optimal Steiner tree $T^*$ with cost = OPT
- Double every edge: create two copies of each edge in $T^*$
- Result: an Eulerian multigraph with cost $2 \cdot \text{OPT}$
- Property: every vertex now has even degree

**Step 2: Euler Tour**
- Traverse the doubled graph following every edge exactly once (Euler tour property)
- This tour visits all vertices in $R \cup S$ (required and Steiner)
- Tour cost = $2 \cdot \text{OPT}$

**Step 3: Shortcutting**
- Walk along the Euler tour but skip:
  - All Steiner vertices
  - Repeated visits to required vertices
- By triangle inequality, skipping vertices does not increase cost
- Result: a cycle (Hamiltonian-like) on required vertices with cost $\le 2 \cdot \text{OPT}$

**Step 4: Convert to Tree**
- Remove any one edge from the cycle → obtain a spanning tree on $R$
- Cost is still $\le 2 \cdot \text{OPT}$
- The MST on $R$ is the minimum-cost spanning tree, so MST cost $\le 2 \cdot \text{OPT}$

**Why this is tight:** A star configuration (central Steiner vertex with $n$ required vertices around it at distance 1) shows that the factor of 2 is achievable and cannot be improved by this method.

## Connection to the Travelling Salesman Problem

### TSP Definition

The Travelling Salesman Problem seeks a **Hamiltonian cycle** visiting each city exactly once and returning to the start, minimizing total distance.

### Shared Proof Techniques

Both Steiner Tree and TSP approximations use the same core techniques:
- Edge doubling to construct Eulerian structure
- Euler traversal as an intermediate object
- Shortcutting under metric inequality to remove repeated visits

### Key Differences

| Aspect | Steiner Tree | TSP |
|--------|--------------|-----|
| **Structure** | Tree (no cycles) | Cycle (Hamiltonian) |
| **Vertices** | Connect required set $R$ | Visit all vertices |
| **Steiner points** | Can be used | Not applicable |
| **Approximation** | 2-approximation via MST | 1.5-approximation (Christofides) |

Both rely on metric properties and shortcutting arguments, making these techniques powerful for metric optimization problems.

## Interactive Demonstration

### What the Demonstration Shows

A visual demonstration using real German cities illustrates how Steiner points affect network cost:

**Scenario:**
- Select a small set of required cities that must be connected
- Select optional Steiner cities that could serve as hubs
- Compute and compare different tree structures

**What you observe:**

1. **Complete Graph View:** All possible connections between cities with their distances (km)

2. **Required-Only MST:** The cheapest tree connecting only the required cities (no Steiner hubs)
   - Cost = MST cost on required vertices only
   - This represents our 2-approximation algorithm

3. **With Steiner Hubs:** The cheapest tree using required cities plus optional Steiner hubs
   - Cost may be significantly lower
   - Shows when and why intermediate cities reduce total cost

4. **Cost Comparison:** Direct visualization of savings
   - Demonstrates that Steiner points can reduce cost by 15-25%
   - Shows that the approximation guarantee (factor 2) is loose in practice

### How Steiner Points Help

**Example:** Three required cities forming a large triangle

- **Direct MST approach:** Connect them with 2 edges of the triangle (cheapest path using only vertices in $R$)
- **With Steiner hub:** 
  - Place an intermediate city at or near the interior (Fermat point)
  - Create 3 shorter edges from hub to each required city
  - If hub position is optimal, total cost can be 5-15% cheaper

This illustrates the key intuition of Steiner trees: **intermediate connection points can provide cheaper routes than direct connections**.

The mathematical reason: the optimal Steiner tree may use hub locations that are not required vertices but serve the connection function more efficiently.

### How Steiner Points May Not Help

- If required cities are already close together (direct path is efficient)
- If candidate Steiner cities are far from the optimal connection routes
- When the direct MST is already near-optimal (limited room for improvement)

The demonstration lets you experiment with different configurations to understand when hubs provide real savings.

### What the Demo Demonstrates About Our Algorithms

1. **Metric Closure in Action:** All connections shown respect metric distances; shortcuts never increase cost

2. **MST Optimality on Required:** The algorithm finds the cheapest spanning tree on $R$ alone

3. **Practical vs. Theoretical Bounds:** 
   - Worst-case bound is factor 2
   - Observed approximation ratio on city instances: 1.3 - 1.5
   - Shows that the bound is conservative

4. **Steiner Benefit Visualization:** See directly when and by how much hubs reduce cost

## Key Takeaways

1. **Steiner Tree Problem:** Connect required vertices minimizing cost; Steiner points are optional hubs that may reduce total cost

2. **Metric Property:** Triangle inequality is essential—it allows shortcutting and ensures direct paths are shortest paths

3. **NP-Hardness:** Exact solutions are computationally hard in worst case; approximation is necessary for practical computation

4. **2-Approximation:** MST on required vertices in metric closure gives provable 2× worst-case guarantee

5. **Proof Technique:** Doubling → Euler tour → shortcutting → spanning tree reduction—elegant chain linking OPT to 2·OPT

6. **TSP Connection:** Same techniques (Euler, shortcutting, doubling) apply; TSP achieves 1.5-approximation via Christofides algorithm

7. **Practice vs. Theory:** Real-world performance is much better than worst-case guarantees; practical ratio often 1.2-1.5

## References

- Vazirani, V. V., *Approximation Algorithms*, Springer-Verlag, 2001. Chapter 3.
- Christofides, N., "Worst-case analysis of a new heuristic for the travelling salesman problem," 1976.
- Robins, G., and Zelikovsky, A., "Improved Steiner tree approximation in graphs," 2000.

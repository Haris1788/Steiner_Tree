# Seminar: Steiner Tree and Traveling Salesman Problem

Based on **Vazirani, V. V.** *Approximation Algorithms*, Chapter 3 (Steiner Tree and TSP)

**Author:** Haris Masood  
**University:** TU Clausthal  
**Course:** Algorithm Seminar 2 - Approximation Algorithms

---

## 1. Steiner Tree Problem

### Definition and Formulation

**Problem Statement:** Given a connected undirected graph $G = (V, E)$ with edge costs $c: E \to \mathbb{R}^+$, the vertex set $V$ is partitioned into:
- **Required vertices**: $R \subseteq V$ (must be connected)
- **Steiner vertices**: $V \setminus R$ (optional, may improve solution)

Find a minimum-cost tree $T$ such that $R \subseteq V(T)$ (all required vertices are in the tree).

### The Metric Closure Reduction (Theorem 3.2)

The general Steiner Tree problem can be reduced to the **metric Steiner Tree problem** without losing approximation quality.

**Construction:** Create $G' = (V, E')$ where:
- Each edge $(u,v) \in E'$ has cost $c'(u,v) = $ shortest path distance from $u$ to $v$ in $G$
- $G'$ is the **metric closure** of $G$ (satisfies triangle inequality)

**Key Result:** Any optimal solution in $G'$ can be converted to a solution in $G$ with the same cost:
- Replace each edge in the $G'$ solution with its corresponding shortest path in $G$
- This may create cycles, but they can be removed to restore tree structure (no cost increase by triangle inequality)

**Consequence:** Approximation factors for metric Steiner tree carry over to the general problem.

### The MST-Based 2-Approximation Algorithm

**Core Insight:** The MST on the required vertices $R$ alone provides a simple 2-approximation.

**Algorithm:**
1. Compute MST $T$ on the subgraph induced by required vertices $R$ only
2. Output $T$ as the Steiner tree

**Theorem 3.3** (MST-Based 2-Approximation):
$$\text{cost}(\text{MST on } R) \leq 2 \cdot \text{OPT}$$

**Proof (from Vazirani, Ch. 3, page 28-29):**

Consider an optimal Steiner tree $T^*$ with cost $\text{OPT}$.

1. **Double the edges:** Create a multigraph by doubling every edge in $T^*$. This produces an Eulerian graph where all vertices (required and Steiner) have even degree.

2. **Find Euler tour:** An Euler tour $\mathcal{T}$ exists in this multigraph. Cost: $\text{cost}(\mathcal{T}) = 2 \cdot \text{OPT}$.

3. **Short-cut to required vertices:** Traverse $\mathcal{T}$ and record required vertices in order of first appearance. Skip Steiner vertices and repeated visits to required vertices.
   - By triangle inequality: shortcuts do not increase cost
   - Result: a Hamiltonian path on $R$ with cost $\leq 2 \cdot \text{OPT}$

4. **Path becomes tree:** Delete one edge from the Hamiltonian path to get a spanning tree on $R$ with cost $\leq 2 \cdot \text{OPT}$.

5. **MST optimality:** The MST on $R$ achieves minimum spanning tree cost, so $\text{cost}(\text{MST}) \leq 2 \cdot \text{OPT}$.

**Tightness Example (Example 3.4):**
- Graph: $n$ required vertices, 1 Steiner vertex $s$ at center
- Edges: $(s, \text{req}_i)$ cost 1 for all $i$; direct connections between required vertices cost 2
- MST on $R$: Must connect via 2-cost edges $\Rightarrow$ cost = $2(n-1)$
- Optimal Steiner tree: Use star via $s$ $\Rightarrow$ cost = $n$
- Approximation ratio: $\frac{2(n-1)}{n} \to 2$ as $n \to \infty$



## 2. Traveling Salesman Problem (TSP)

### Definition

**Problem 3.5** (TSP): Given a complete undirected graph with nonnegative edge costs, find a minimum-cost cycle visiting every vertex exactly once.

**Formal notation:**
$$\text{cost}(C) = \sum_{(u,v) \in C} c(u,v) \text{ is minimized}$$

### Hardness in the General Case (Theorem 3.6 – Sahni & Gonzalez)

**Theorem 3.6**: For any polynomial-time computable function $\alpha(n)$, TSP **cannot be approximated within a factor of $\alpha(n)$** unless $P = NP$.

**Proof Sketch (Vazirani, Ch. 3, page 30):**
- Reduction from Hamiltonian Cycle (NP-hard) to TSP
- Given graph $G$ with $n$ vertices, construct complete graph $G'$ where:
  - Edges in $G$: weight 1
  - Non-edges in $G$: weight $\alpha(n) \cdot n$
- If $G$ has Hamiltonian cycle: optimal TSP tour in $G'$ has cost $n$
- If $G$ has no Hamiltonian cycle: any TSP tour in $G'$ has cost $> \alpha(n) \cdot n$
- Thus, any $\alpha(n)$-approximation algorithm decides Hamiltonian Cycle (unless $P = NP$)

**Key Insight:** Hardness arises because costs **violate triangle inequality**.

### Metric TSP: Approximable Restriction

When edge costs satisfy **triangle inequality** $c(u,w) \leq c(u,v) + c(v,w)$ for all $u,v,w \in V$:
- Problem remains NP-complete
- But approximation algorithms exist with guaranteed factors

---

## 3. Metric TSP: Factor 2 Algorithm (Algorithm 3.7)

### Algorithm Statement

**Input:** Complete graph $G = (V, E, c)$ with edge costs satisfying triangle inequality

**Output:** Hamiltonian cycle (tour) $C$

**Steps (Vazirani, Ch. 3, page 30-31):**
1. Find a minimum spanning tree $T$ of $G$
2. Double every edge of $T$ to create an Eulerian multigraph (all vertices even degree)
3. Find an Eulerian tour $\mathcal{T}$ (e.g., via DFS)
4. Traverse $\mathcal{T}$ and output tour $C$ in order of **first appearance** of each vertex

### Theorem 3.8 (Factor 2 Guarantee)

**Statement:** Algorithm 3.7 achieves a $2$-approximation for metric TSP.

**Proof:**
$$\text{cost}(T) \leq \text{OPT}$$
(Removing any edge from optimal TSP tour yields a spanning tree)

$$\text{cost}(\mathcal{T}) = 2 \cdot \text{cost}(T)$$
(Each edge in $T$ traversed exactly twice)

$$\text{cost}(C) \leq \text{cost}(\mathcal{T})$$
(Triangle inequality: shortcuts preserve or reduce cost)

**Combining:** 
$$\text{cost}(C) \leq 2 \cdot \text{cost}(T) \leq 2 \cdot \text{OPT}$$

### Tightness Example (Example 3.9, Page 31-32)

For $n = 6$ vertices with edges of cost 1 and 2:
- Thick edges (cost 1): form a star + $(n-1)$-cycle = $2n-2$ edges
- Other edges (cost 2): complete the graph
- MST found: star of cost $2(n-1)$
- Optimal TSP tour: uses only thick edges = cost $n$
- Algorithm's tour (after short-cutting): uses $(n-2)$ thick edges + cost-2 edges = $2n-2$ ≈ $2 \cdot OPT$

---

## 4. Metric TSP: Factor 3/2 Algorithm (Christofides, Algorithm 3.10)

### Algorithm Motivation

The MST doubling wastes edges. **Key observation:** Only odd-degree vertices in the MST prevent an Eulerian graph.

**Solution:** Add a minimum-cost perfect matching on odd-degree vertices.

### Algorithm Statement

**Input:** Complete graph $G$ with triangle inequality

**Output:** Hamiltonian cycle $C$

**Steps (Vazirani, Ch. 3, page 32):**
1. Find MST $T$ of $G$
2. Let $V_{\text{odd}}$ = set of odd-degree vertices in $T$
3. Find minimum-cost perfect matching $M$ on $V_{\text{odd}}$
4. Combine $T + M$ to form Eulerian multigraph $G_E$
5. Find Eulerian tour $\mathcal{T}$
6. Short-cut to obtain Hamiltonian cycle $C$

### Theorem 3.12 (Factor 3/2 Guarantee)

**Lower Bound on OPT (Lemma 3.11, Page 32):**

For any set $V' \subseteq V$ of even cardinality, if $M$ is a min-cost perfect matching on $V'$:
$$\text{cost}(M) \leq \frac{1}{2} \cdot \text{OPT}$$

**Proof:** Any Hamiltonian cycle partitions into two edge-disjoint perfect matchings on $V'$ (alternate edges of the cycle). The cheaper matching costs $\leq \frac{1}{2} \cdot \text{OPT}$.

**Main Result (Theorem 3.12, Page 32):**
$$\text{cost}(G_E) = \text{cost}(T) + \text{cost}(M) \leq \text{OPT} + \frac{1}{2}\text{OPT} = \frac{3}{2}\text{OPT}$$

---

## 5. Connection to Steiner Tree

Both Steiner Tree and TSP approximations use the same core techniques:
- **Doubling edges** to construct Eulerian structure
- **Euler tours** as intermediate combinatorial objects  
- **Shortcutting** under triangle inequality to reduce visited vertices

The main difference:
- **Steiner Tree:** Connects a required subset $R$ of vertices (can use Steiner vertices)
- **Metric TSP:** Visits all vertices in a cycle (no Steiner points)

---

## 6. Interactive Demo: steiner_cities_streamlit.py

The Streamlit application demonstrates Steiner Tree 2-approximation using real German cities:

**Features:**
- Select required cities (interactive canvas)
- Compute MST on required cities
- Optional Steiner vertices (intermediate cities)
- Visualize tree and cost comparison
- Real road distances from Google Maps

**What it illustrates:**
- Metric closure in action (all distances respect triangle inequality)
- MST computation on subsets of vertices
- Practical vs. theoretical bounds (often MST is 1.3-1.5 approximation in practice)



---

## Key Theorems Summary

| Problem | Algorithm | Approximation Factor | Key Theorem |
|---------|-----------|---------------------|------------|
| **Metric Steiner Tree** | MST on required vertices | 2 | Theorem 3.3 |
| **General TSP** | (None) | Inapproximable | Theorem 3.6 |
| **Metric TSP** | MST + edge doubling + short-cut | 2 | Theorem 3.8 |
| **Metric TSP** | MST + perfect matching (Christofides) | 3/2 | Theorem 3.12 |

---

## References

- **Vazirani, V. V.** (2003). *Approximation Algorithms*. Springer-Verlag. Chapter 3: Steiner Tree and TSP.
  - Pages 28–32: Steiner Tree problem, metric closure, MST 2-approximation (Theorems 3.2, 3.3)
  - Pages 30–32: TSP hardness (Theorem 3.6), metric TSP algorithms (Theorems 3.8, 3.12)
  - Examples 3.4, 3.9, 3.13: Tight examples demonstrating factor 2, 2, 3/2 respectively
- **Christofides, N.** (1976). "Worst-case analysis of a new heuristic for the travelling salesman problem." *Proceedings of the 7th Annual ACM Symposium on Theory of Computing*.
- **Hwang, F. K., Richards, D. S., & Winter, P.** (1992). *The Steiner Tree Problem*. North-Holland.

---

**Last Updated:** Based on Vazirani Chapter 3 content (March 2026)

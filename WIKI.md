# Steiner Tree and Travelling Salesman Problem: Approximation Algorithms for Metric Networks

**Author:** Haris Masood  
**University:** TU Clausthal  
**Course:** Algorithm Seminar 2 - Approximation Algorithms

## Introduction

The Steiner Tree problem and the Travelling Salesman Problem (TSP) are two fundamental problems in combinatorial optimization. Both appear in network design, logistics, VLSI layout, and infrastructure planning. While exact solutions are computationally hard, approximation algorithms provide efficient solutions with guaranteed performance bounds relative to the optimal solution.

This presentation covers the 2-approximation algorithm for the metric Steiner Tree problem and its connections to TSP through the techniques of metric closure, Euler tours, and shortcutting.

## The Steiner Tree Problem

Imagine you need to connect a set of required cities with minimum total road length. A natural approach is to directly connect only these required cities using the shortest paths between them. However, what if you could reduce the total cost by adding intermediate cities as **Steiner points**—hubs that aren't required but serve as connection points?

This is the core idea of the **Steiner Tree problem**: given a graph with some required vertices, find a tree that connects all required vertices (and possibly uses additional Steiner vertices) with minimum total edge cost.

### What is a Steiner Point?

A Steiner point is an optional intermediate vertex we can include in the tree to reduce the total cost. It's not a required destination, but it acts as a junction point. For instance, a logistics company might designate a warehouse (Steiner point) to reduce the total delivery distance between customer locations (required vertices).

### The Problem We Solve

Suppose we have a connected graph $G = (V, E)$ with nonnegative edge costs and a set of **required vertices** $R \subseteq V$. We seek a tree $T$ that:
- Connects all required vertices in $R$
- May include additional Steiner vertices from $V \setminus R$
- Has minimum total edge cost

The challenge is that finding the optimal subset of Steiner vertices to include is **NP-hard**—there's no known polynomial-time algorithm to guarantee an optimal solution.

### Why Triangle Inequality Matters

For most real-world scenarios, edge costs satisfy the **triangle inequality**: the direct path between two points is never more expensive than going through an intermediate point. This property is crucial because it enables approximation algorithms that use shortcuts to reduce cost.

## The 2-Approximation Algorithm

Rather than solving the problem exactly (which is hard), we use an elegant approximation approach based on **Theorem 3.2** and **Theorem 3.3** from Vazirani's textbook.

### Step 1: Metric Closure

The key insight is to reduce the problem to a **metric version**. Construct a new graph $G'$:
- Keep only the required vertices $R$
- Add edges between all pairs of required vertices
- Set each edge's cost to the shortest path distance in the original graph $G$

This graph $G'$ is called the **metric closure**. Any optimal Steiner tree in the original graph can be converted to an equally-cost solution in $G'$ by simply expanding the metric edges back into their shortest paths. Therefore, any approximation algorithm for the metric version automatically works for the general problem.

### Step 2: MST-Based 2-Approximation

Now we exploit a simple but powerful fact: **Theorem 3.3** states that the cost of an MST on $R$ in the metric closure is within twice the optimal cost.

**Algorithm:** Compute the Minimum Spanning Tree on the required vertices in $G'$.

**Why it works:** The proof uses a clever sequence of steps:

1. **Double the edges** of the optimal Steiner tree—create a multigraph where every edge appears twice. This costs exactly $2 \times \text{OPT}$ and makes every vertex have even degree.

2. **Find an Euler tour**—traverse every edge exactly once. This tour visits all required and Steiner vertices and has cost $2 \times \text{OPT}$.

3. **Shortcut to required vertices**—as you walk the Euler tour, skip any Steiner vertices or repeated visits to required vertices. By triangle inequality, these shortcuts never increase cost.

4. **Convert to spanning tree**—the resulting path on required vertices has cost $\leq 2 \times \text{OPT}$. Removing one edge gives a spanning tree on $R$, which the MST minimizes.

Therefore: $\text{cost}(\text{MST on } R) \leq 2 \times \text{OPT}$

### When is the Approximation Tight?

Consider a star graph: one central Steiner vertex connected to $n$ required vertices, each edge costing 1, but direct connections between required vertices cost 2. The MST must use only the 2-cost edges ($2(n-1)$ total cost), while the optimal tree uses the star ($n$ total cost). The ratio approaches 2 as $n$ grows, showing this bound is tight.



## The Travelling Salesman Problem

Now consider a related but different problem: a salesman must visit every city exactly once and return home, minimizing total travel distance. This is the **Travelling Salesman Problem (TSP)**.

Unlike Steiner Tree, where we only need to connect required vertices, TSP demands visiting **all** vertices in a cycle. But the similar structure—both are hard combinatorial optimizations on graphs—means we can use similar approximation techniques.

### Why General TSP is Inapproximable

A striking result (Theorem 3.6 in Vazirani) shows that TSP in its most general form cannot be approximated by any polynomial-time algorithm unless P=NP. The reason: without the triangle inequality constraint, you can construct instances where any approximation fails. 

For example, if graph edges have arbitrary costs (violating triangle inequality), you could make the direct path between two cities expensive while indirect paths are cheap—defeating shortcutting strategies used in approximation algorithms.

### Metric TSP: Where Approximation Works

When we restrict to **metric TSP**—where costs satisfy triangle inequality—the problem becomes approximable. We can then use the same proof techniques as Steiner Tree: edge doubling, Euler tours, and intelligent shortcuts.

The key insight: **triangle inequality guarantees that shortcuts never increase cost**. When you skip a vertex on your tour and jump directly to the next required vertex, the direct edge is never more expensive than the path through the skipped vertex.

Using MST doubling and shortcutting (like in Steiner Tree), we achieve a factor 2 approximation. The Christofides algorithm, which adds a minimum perfect matching on odd-degree vertices, improves this to factor 3/2.

### Connection to Steiner Tree

Both problems use the same core techniques:
- **Doubling edges** to create an Eulerian structure (all vertices have even degree)
- **Euler tours** to traverse the graph visiting all required vertices
- **Shortcutting** under triangle inequality to collapse paths and reduce cost

The main difference: Steiner Tree connects only required vertices (and may use Steiner points to optimize), while TSP must visit every vertex in a cycle.

| Aspect | Steiner Tree | TSP |
|--------|--------------|-----|
| **Goal** | Connect required vertices with minimum cost | Visit all vertices in a cycle with minimum cost |
| **Steiner vertices** | Allowed (can use intermediate points) | Not applicable (must visit all) |
| **Structure** | Tree (acyclic) | Cycle (Hamiltonian) |
| **Approximation** | Factor 2 via MST | Factor 2 via MST doubling; Factor 3/2 via Christofides |


## Seeing It in Action: The Demo

Our interactive Streamlit application lets you experiment with the Steiner Tree algorithm using real German cities and their road distances. The demo illustrates:

**How it works:**
1. Select a set of required cities that must be connected
2. Optionally choose Steiner cities (intermediate hubs)
3. Watch the algorithm compute the MST and visualize the tree
4. Compare the cost with and without Steiner hubs

**What you'll observe:**
- The shortest direct connections between required cities alone
- How intermediate cities can reduce total cost (when optimally placed)
- That the factor 2 worst-case bound is conservative—real instances often achieve 1.3–1.5 approximation
- When Steiner points help (cities forming large triangles) vs. when they don't (already-clustered cities)

This hands-on exploration shows why approximation algorithms matter: while we can't always find the optimal solution quickly, we can find solutions that are guaranteed to be at most twice the optimal—and usually much better.



## References

- Vazirani, V. V., *Approximation Algorithms*, Springer-Verlag, 2001. Chapter 3.
- Christofides, N., "Worst-case analysis of a new heuristic for the travelling salesman problem," 1976.
- Robins, G., and Zelikovsky, A., "Improved Steiner tree approximation in graphs," 2000.

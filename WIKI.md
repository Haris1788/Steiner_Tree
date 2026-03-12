# Wiki: Steiner Tree and Travelling Sales Problem

**Author:** Haris Masood  
**University:** TU Clausthal  
**Course:** Algorithm Seminar 2 - Approximation Algorithms

## Overview

This wiki summarizes the seminar topic area around the Metric Steiner Tree problem and its connection to the Travelling Sales Problem (TSP). The focus is on approximation techniques, especially the classical 2-approximation framework based on metric closure and minimum spanning trees.

The practical part is implemented in [steiner_cities_streamlit.py](steiner_cities_streamlit.py), where the theory is visualized on a small real-city instance.

## Topics Covered

1. Metric Steiner Tree: formulation and objective
2. Metric closure construction (Theorem 3.2 idea)
3. 2-approximation guarantee using MST on required vertices (Theorem 3.3 idea)
4. Connection to TSP via doubling, Euler tour, and shortcutting
5. Practical interpretation using real distance data

## Problem Setting

Given a weighted graph with metric distances:
- Let $R$ be the required vertices that must be connected.
- Let $S$ be optional Steiner vertices that may be used as intermediate hubs.
- Goal: compute a minimum-cost tree that spans all vertices in $R$ (using vertices from $S$ if helpful).

The metric assumption is essential:

$$
d(u,w) \le d(u,v) + d(v,w)
$$

This triangle inequality is what makes shortcut-based approximation arguments valid.

## Why Steiner Tree Is Hard

The exact Steiner Tree problem is NP-hard. For realistic inputs, exact optimization can be expensive, so approximation algorithms are used to provide provable quality bounds with efficient runtime.

In this topic, the objective is not exact optimality for every instance, but a guaranteed bound relative to OPT (the unknown true optimum).

## Metric Closure (Theorem 3.2 Perspective)

Metric closure transforms the problem to a complete graph on required vertices only:

1. Build a complete graph on vertex set $R$.
2. For each pair $(u,v)$ in $R$, assign edge weight equal to the shortest-path distance between $u$ and $v$ in the original graph.
3. Work on this complete metric graph for approximation.

Interpretation:
- Optional Steiner structure is not discarded conceptually; it is absorbed into shortest-path distances.
- This allows the algorithm to reason over required nodes while still accounting for potentially beneficial intermediate routes.

## 2-Approximation Guarantee (Theorem 3.3 Perspective)

Main bound:

$$
	ext{cost(MST on } R\text{ in metric closure)} \le 2 \cdot \text{OPT}
$$

Proof idea in compact form:

1. Start with an optimal Steiner tree $T^*$, cost = OPT.
2. Double every edge of $T^*$, producing an Eulerian multigraph of cost $2\cdot \text{OPT}$.
3. Take an Euler tour.
4. Shortcut repeated/Steiner visits using triangle inequality.
5. Obtain a cycle/tour over required vertices of cost at most $2\cdot \text{OPT}$.
6. Remove one edge to get a spanning tree on required vertices.
7. MST is no more expensive than any spanning tree on the same vertex set.

The result is a worst-case guarantee. In many practical instances, the observed ratio is better than 2.

## Connection to Travelling Sales Problem

The Steiner and TSP analyses share core techniques:
- Edge doubling to construct Eulerian structure.
- Euler traversal as an intermediate object.
- Shortcutting under metric inequality to remove repeated visits.

Difference in objective:
- Steiner Tree seeks a low-cost tree connecting required nodes (no need to return to start, no cycle requirement).
- TSP seeks a Hamiltonian cycle visiting each city exactly once.

The shortcut argument links both topics and motivates why metric assumptions are central in approximation theory.

## Practical Demo in This Repository

Primary implementation: [steiner_cities_streamlit.py](steiner_cities_streamlit.py)

### What the demo models

- Required cities (must-connect terminals)
- Optional Steiner cities (candidate hubs)
- Weighted metric instance using fixed inter-city distances (km)
- Visual comparison of different connection structures

### What can be analyzed interactively

1. Required vs Steiner selection
2. Complete graph visibility
3. Metric-closure-like connectivity view on required nodes
4. MST on required nodes only
5. MST on required + Steiner nodes (used as practical proxy to show hub benefit)
6. Cost comparison and relative savings

### Educational value of the demo

- Makes approximation bounds concrete with visible edges and costs
- Shows when and why optional hubs reduce total network cost
- Demonstrates that theoretical worst-case bounds and practical behavior can differ

## Notes on Interpretation

- The implemented visualization is for intuition and topic communication.
- In code, MST on required+Steiner is used as a practical comparative object; this helps show the effect of optional hubs, though it is not a full exact Steiner solver.
- For seminar-level discussion, this is appropriate to explain both guarantees and empirical behavior.

## Run Instructions

From the project root:

```bash
pip install -r Docs/requirements.txt
streamlit run steiner_cities_streamlit.py --server.port 8503
```

Open in browser: http://localhost:8503

## Relevant Files

- [steiner_cities_streamlit.py](steiner_cities_streamlit.py)
- [Docs/requirements.txt](Docs/requirements.txt)
- [WIKI.md](WIKI.md)

## References

- Vazirani, V. V., Approximation Algorithms, Chapter 3.
- Standard results on metric MST/TSP shortcut arguments and Euler-tour constructions.

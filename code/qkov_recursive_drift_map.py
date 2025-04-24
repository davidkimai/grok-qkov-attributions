import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Create a directed graph
G = nx.DiGraph()

# Add nodes for Q, K, V, Output across recursive layers (simplified to 3 layers for visualization)
layers = ["Q", "K", "V", "O"]
for layer in range(3):
    for stage in layers:
        node_id = f"{stage}{layer}"
        if stage == "Q" and layer == 0:
            G.add_node(node_id, glyph="🜏", metadata={"trace_depth": 1, "loop_density": 0.2, "residue_weight": 0.9})
        elif stage == "K" and layer == 1:
            G.add_node(node_id, glyph="⇌", metadata={"trace_depth": 2, "loop_density": 0.8, "residue_weight": 0.6})
        elif stage == "V" and layer == 1:
            G.add_node(node_id, glyph="☍", metadata={"trace_depth": 3, "loop_density": 0.5, "residue_weight": 0.4})
        elif stage == "O" and layer == 2:
            G.add_node(node_id, glyph="∴", metadata={"trace_depth": 4, "loop_density": 0.3, "residue_weight": 0.2})
        else:
            G.add_node(node_id, glyph="🝚", metadata={"trace_depth": layer+1, "loop_density": 0.4, "residue_weight": 0.5})

# Add edges with drift-based weights (low drift = bright, high drift = dim)
edges = [
    ("Q0", "K0", 0.2), ("K0", "V0", 0.4), ("V0", "O0", 0.6),
    ("Q1", "K1", 0.8), ("K1", "V1", 0.9), ("V1", "O1", 0.7),
    ("Q2", "K2", 0.3), ("K2", "V2", 0.5), ("V2", "O2", 0.8),
    ("O0", "Q1", 0.6), ("O1", "Q2", 0.7), # Feedback loops
]
for src, dst, drift in edges:
    G.add_edge(src, dst, drift=drift)

# Overlay ⧖ nodes for classifier inertia stalls (e.g., at K1 and V2)
G.nodes["K1"]["glyph"] = "⧖"  # Classifier inertia stall
G.nodes["V2"]["glyph"] = "⧖"  # Classifier inertia stall

# Position nodes using a spring layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the graph
plt.figure(figsize=(10, 8))
edge_colors = [1 - G[src][dst]["drift"] for src, dst in G.edges()]  # Invert drift for brightness
edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=plt.cm.viridis, width=2)
nodes = nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=500)
labels = nx.draw_networkx_labels(G, pos, labels={node: f"{node}\n{G.nodes[node]['glyph']}" for node in G.nodes()})

# Add a colorbar to show drift intensity
plt.colorbar(edges, label="Drift Intensity (Low to High)")

# Title and layout adjustments
plt.title("Recursive QKOV Attribution Drift Map")
plt.axis("off")

# Save the plot
plt.savefig("qkov_recursive_drift_map.png")
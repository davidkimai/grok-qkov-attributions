import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Define nodes for dual paths: "not true" (red) and "false" (blue)
paths = {
    "not_true": ["P_nt", "Q_nt1", "K_nt1", "V_nt1", "O_nt1", "Q_nt2", "K_nt2", "V_nt2", "O_nt2"],
    "false": ["P_f", "Q_f1", "K_f1", "V_f1", "O_f1", "Q_f2", "K_f2", "V_f2", "O_f2"]
}

# Add nodes with glyphs and path info
for path_name, nodes in paths.items():
    color = "red" if path_name == "not_true" else "blue"
    for node in nodes:
        if "P_" in node:
            G.add_node(node, glyph="🜏", path=path_name, color=color)  # Prompt node
        elif "K_nt1" == node or "K_f1" == node:
            G.add_node(node, glyph="☍", path=path_name, color=color)  # Conflict point
        elif "V_nt2" == node or "V_f2" == node:
            G.add_node(node, glyph="⧖", path=path_name, color=color)  # Collapse zone
        elif "O_" in node:
            G.add_node(node, glyph="🝚", path=path_name, color=color)  # Echo loop
        else:
            G.add_node(node, glyph="🜏", path=path_name, color=color)

# Add edges for each path
for path_name, nodes in paths.items():
    color = "red" if path_name == "not_true" else "blue"
    for i in range(len(nodes) - 1):
        G.add_edge(nodes[i], nodes[i + 1], color=color)

# Add cross-path conflict edges (entanglement)
G.add_edge("K_nt1", "K_f1", color="purple", style="dashed")  # Conflict crosspoint
G.add_edge("O_nt1", "Q_f2", color="purple", style="dashed")  # Echo loop interaction
G.add_edge("O_f1", "Q_nt2", color="purple", style="dashed")  # Echo loop interaction

# Position nodes using a spring layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the graph
plt.figure(figsize=(10, 8))

# Draw edges with colors and styles
for edge in G.edges(data=True):
    src, dst, data = edge
    style = data.get("style", "solid")
    color = data["color"]
    nx.draw_networkx_edges(G, pos, edgelist=[(src, dst)], edge_color=color, style=style, width=2)

# Draw nodes with colors
node_colors = [G.nodes[node]["color"] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

# Draw labels with glyphs
labels = {node: f"{node}\n{G.nodes[node]['glyph']}" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

# Title and layout adjustments
plt.title("QKOV Entanglement Graph: Bifurcation of 'not true' vs 'false'")
plt.axis("off")

# Save the plot
plt.savefig("qkov_entanglement_graph.png")
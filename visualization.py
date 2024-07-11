# visualization.py
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(node, graph=None):
    if graph is None:
        graph = nx.Graph()
    graph.add_node(node.name)
    for child in node.children:
        graph.add_edge(node.name, child.name)
        build_graph(child, graph)
    return graph

def visualize_tree(node):
    graph = build_graph(node)
    pos = nx.spring_layout(graph)  # positions for all nodes
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=12, font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
    plt.title("Partition Tree Visualization")
    plt.show()

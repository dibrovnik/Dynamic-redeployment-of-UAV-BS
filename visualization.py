import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch
import numpy as np

def visualize_tree_with_euler_circles(node, center=(0, 0), radius=10, level=0, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')

    # Рисуем круг для текущего узла
    circle = Circle(center, radius, color='skyblue', ec='black', zorder=2)
    ax.add_patch(circle)
    ax.annotate(node.name, center, color='black', weight='bold', fontsize=12, ha='center', va='center', zorder=3)

    # Рисуем круги для дочерних узлов
    num_children = len(node.children)
    if num_children > 0:
        child_radius = radius / (2 * num_children)
        for i, child in enumerate(node.children):
            angle = (i / num_children) * 2 * 3.14159  # угол для равномерного распределения дочерних узлов по окружности
            x_child = center[0] + radius * 0.8 * np.cos(angle)
            y_child = center[1] + radius * 0.8 * np.sin(angle)
            child_center = (x_child, y_child)
            visualize_tree_with_euler_circles(child, center=child_center, radius=child_radius, level=level + 1, ax=ax)

            # Соединяем круги родителя и дочерние круги
            con = ConnectionPatch(xyA=center, xyB=child_center, coordsA="data", coordsB="data",
                                  arrowstyle="-|>", shrinkA=5, shrinkB=5, mutation_scale=20, color="gray", zorder=1)
            ax.add_patch(con)

    ax.set_title("Partition Tree Visualization with Euler Circles")
    ax.autoscale_view()
    ax.axis('off')

    if level == 0:
        plt.show()



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

def build_graph_extended(node, graph=None):
    if graph is None:
        graph = nx.Graph()
    
    graph.add_node(node.name)
    
    # Добавляем ребра для дочерних узлов
    for child in node.children:
        graph.add_edge(node.name, child.name)
        build_graph_extended(child, graph)
    
    # Добавляем ребра для кластеров внутри каждого ребенка
    for child in node.children:
        for cluster in child.clusters:
            graph.add_edge(child.name, cluster.name)
            build_graph_extended(cluster, graph)
    
    return graph

import matplotlib.pyplot as plt
import networkx as nx
from partition import partition
from assign import assign_uav_bss

def create_graph(node, graph=None, pos=None, level=0, pos_x=0.5, width=1.0):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}
    
    graph.add_node(node.name, level=level, uav_bss=node.N_assigned)
    pos[node.name] = (pos_x, -level)
    
    num_children = len(node.children)
    if num_children > 0:
        dx = width / num_children
        next_x = pos_x - width / 2 - dx / 2
        for i, child in enumerate(node.children):
            next_x += dx
            graph.add_edge(node.name, child.name)
            create_graph(child, graph, pos, level + 1, next_x, dx)
    
    return graph, pos

def draw_graph(graph, pos):
    plt.figure(figsize=(10, 8))
    labels = {node: f"{node}\nUAV-BSs: {graph.nodes[node]['uav_bss']}" for node in graph.nodes}
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
    plt.show()

# Параметры
area_name = "A"  # Название корневой области
num_clusters = 3  # Количество кластеров на каждом уровне
max_depth = 2  # Максимальная глубина дерева
total_uav_bss = 21  # Общее количество БПЛА для назначения

# Создание структуры дерева
root = partition(area_name, num_clusters, max_depth)

# Назначение UAV-BS, начиная с корня
assign_uav_bss(root, total_uav_bss, 0)

# Создание графа
graph, pos = create_graph(root)

# Визуализация графа
draw_graph(graph, pos)

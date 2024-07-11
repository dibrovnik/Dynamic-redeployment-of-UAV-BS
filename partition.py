# Класс TreeNode:
# Класс для представления узла дерева, где каждый узел имеет имя и список детей.

# Функция partition:
# Создает корневой узел дерева и вызывает функцию create_partition_tree для создания дерева разделения.

# Функция create_partition_tree:
# Рекурсивно делит текущий узел на k подблоков, создавая для каждого нового подблока новый узел.
# Процесс продолжается до достижения максимальной глубины дерева max_depth.


# Параметры:
# area: имя корневого узла (вся площадь).
# k: количество подблоков, на которые делится каждый узел.
# max_depth: максимальная глубина дерева.

# Функция print_tree:
# Рекурсивно печатает дерево разделения, отображая имена узлов и их иерархию.

# Этот код показывает как разбивается вся площадь на кластеры
# Для визуализации строится граф

import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

def partition(area, k, max_depth):
    root = TreeNode(area)
    create_partition_tree(root, k, max_depth)
    return root

def create_partition_tree(node, k, max_depth, depth=0):
    if depth == max_depth:
        return
    
    for i in range(k):
        child_name = f"{node.name}.{i+1}"
        child_node = TreeNode(child_name)
        node.children.append(child_node)
        
        create_partition_tree(child_node, k, max_depth, depth + 1)

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

area = "A"

# k: количество подблоков, на которые делится каждый узел.
k = 4

# max_depth: максимальная глубина дерева.
max_depth = 2

partition_tree = partition(area, k, max_depth)
visualize_tree(partition_tree)


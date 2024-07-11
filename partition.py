class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.clusters = []  # Добавляем список для хранения кластеров

# area - название области (например, 'A'), k - количество кластеров max_depth - максимальная глубина дерева
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
        
        # Создаем кластеры внутри каждой области
        for j in range(2):  # Пример: в каждой области создаются 2 кластера
            cluster_name = f"{child_node.name}.cluster{j+1}"
            cluster_node = TreeNode(cluster_name)
            child_node.clusters.append(cluster_node)
    
        create_partition_tree(child_node, k, max_depth, depth + 1)

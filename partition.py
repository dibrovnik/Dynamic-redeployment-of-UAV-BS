# partition.py

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.N_upper = 0
        self.N_lower = 0
        self.N_assigned = 0

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

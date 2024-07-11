# deploy.py
from partition import partition
from assign import assign_uav_bss

# Пример структуры дерева
root = partition("A", 3, 2)

# Назначение UAV-BS, начиная с корня
assign_uav_bss(root, 10, 0)

# Функция для вывода дерева и назначений
def print_tree(node, level=0):
    print(" " * level * 2, f"{node.name}: Assigned {node.N_assigned} UAV-BSs")
    for child in node.children:
        print_tree(child, level + 1)

# Вывод назначений
print_tree(root)

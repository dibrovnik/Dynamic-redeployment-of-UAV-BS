from partition import *
from visualization import visualize_tree, visualize_tree_with_euler_circles

tree = partition('A', 3, 2)  # Увеличиваем глубину дерева до 2

visualize_tree(tree)
visualize_tree_with_euler_circles(tree)
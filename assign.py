# assign.py
from partition import TreeNode

def calculate_user_distribution(node):
    # Ваша логика для расчета распределения пользователей в подблоке
    return 1

def calculate_upper_bound(node):
    # Ваша логика для расчета верхней границы
    return 3

def calculate_lower_bound(node):
    # Ваша логика для расчета нижней границы
    return 1

def assign_uav_bss(node, uav_bss, node_depth):
    # Рассчитать верхнюю и нижнюю границы для UAV-BS для этого узла
    N_plus_A = calculate_upper_bound(node)
    N_minus_A = calculate_lower_bound(node)

    # Убедиться, что количество UAV-BS находится в пределах границ
    uav_bss = min(max(uav_bss, N_minus_A), N_plus_A)
    node.N_assigned = uav_bss

    # Если у узла нет дочерних элементов, вернуться
    if not node.children:
        return

    # Рассчитать количество пользователей в подблоках
    users_in_sub_blocks = [calculate_user_distribution(child) for child in node.children]
    total_users = sum(users_in_sub_blocks)

    # Пропорционально распределить UAV-BS между дочерними узлами
    remaining_uav_bss = uav_bss
    for i, child in enumerate(node.children):
        if i == len(node.children) - 1:  # Последний дочерний узел получает оставшиеся UAV-BS
            child_uav_bss = remaining_uav_bss
        else:
            child_uav_bss = round((users_in_sub_blocks[i] / total_users) * uav_bss)
            remaining_uav_bss -= child_uav_bss
        
        # Убедиться, что количество UAV-BS у дочернего узла находится в пределах границ
        child_uav_bss = min(max(child_uav_bss, calculate_lower_bound(child)), calculate_upper_bound(child))
        assign_uav_bss(child, child_uav_bss, node_depth + 1)

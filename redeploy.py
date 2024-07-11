# redeploy.py
from partition import partition
from assign import assign_uav_bss

def redeploy_uav_bss(root, new_uav_bss):
    # Функция для перераспределения UAV-BS с новыми параметрами
    assign_uav_bss(root, new_uav_bss, 0)

# Пример использования
root = partition("A", 3, 2)

# Первоначальное назначение
assign_uav_bss(root, 10, 0)

# Перераспределение с новыми параметрами
redeploy_uav_bss(root, 12)

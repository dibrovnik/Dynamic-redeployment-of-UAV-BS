import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise  # библиотека для шума Перлина

class Territory:
    def __init__(self, area_size):
        self.area_size = area_size  # площадь территории в квадратных километрах

class User:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def simulate_user_distribution(territory, num_users, cluster_probability, perlin_scale=0.1, perlin_octaves=6, perlin_seed=None):
    area_side_length = np.sqrt(territory.area_size)  # длина стороны квадрата, представляющего территорию

    users = []

    # Генерируем шум Перлина
    noise = PerlinNoise(octaves=perlin_octaves, seed=perlin_seed)

    # Генерируем пользователей
    for _ in range(num_users):
        if np.random.rand() < cluster_probability:
            # Генерируем кластер в случайной точке территории
            cluster_center_x = np.random.uniform(0, area_side_length)
            cluster_center_y = np.random.uniform(0, area_side_length)

            # Генерируем случайное количество пользователей в кластере (от 1 до 10)
            cluster_size = np.random.randint(1, 11)

            for _ in range(cluster_size):
                # Генерируем смещение по x и y с использованием шума Перлина
                offset_x = noise([perlin_scale * cluster_center_x, perlin_scale * cluster_center_y])
                offset_y = noise([perlin_scale * cluster_center_x + 1000, perlin_scale * cluster_center_y + 1000])
                
                user_x = cluster_center_x + offset_x * perlin_scale
                user_y = cluster_center_y + offset_y * perlin_scale
                
                if 0 <= user_x <= area_side_length and 0 <= user_y <= area_side_length:
                    users.append(User(user_x, user_y))
        else:
            # Генерируем случайного пользователя в случайной точке территории
            user_x = np.random.uniform(0, area_side_length)
            user_y = np.random.uniform(0, area_side_length)
            users.append(User(user_x, user_y))

    return users

# Пример использования модуля для симуляции и визуализации распределения пользователей
if __name__ == "__main__":
    territory = Territory(area_size=50)  # территория размером 50 км²
    num_users = 1000  # общее количество пользователей
    cluster_probability = 0.8  # вероятность того, что пользователи образуют кластеры
    perlin_scale = 0.1  # масштаб шума Перлина
    perlin_octaves = 6  # количество октав шума Перлина
    perlin_seed = None  # семя для воспроизводимости

    users = simulate_user_distribution(territory, num_users, cluster_probability, perlin_scale, perlin_octaves, perlin_seed)
   
    # plot_user_distribution(users, territory)

import numpy as np
import matplotlib.pyplot as plt

class Territory:
    def __init__(self, area_size):
        self.area_size = area_size  # площадь территории в квадратных километрах

class User:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def simulate_user_distribution(territory, num_users, cluster_probability):
    area_side_length = np.sqrt(territory.area_size)  # длина стороны квадрата, представляющего территорию

    users = []

    # Генерируем случайные кластеры пользователей
    for _ in range(num_users):
        if np.random.rand() < cluster_probability:
            # Генерируем кластер в случайной точке территории
            cluster_center_x = np.random.uniform(0, area_side_length)
            cluster_center_y = np.random.uniform(0, area_side_length)

            # Генерируем случайное количество пользователей в кластере (от 1 до 10)
            cluster_size = np.random.randint(1, 11)

            for _ in range(cluster_size):
                user_x = np.random.normal(cluster_center_x, 0.5)
                user_y = np.random.normal(cluster_center_y, 0.5)
                if 0 <= user_x <= area_side_length and 0 <= user_y <= area_side_length:
                    users.append(User(user_x, user_y))
        else:
            # Генерируем случайного пользователя в случайной точке территории
            user_x = np.random.uniform(0, area_side_length)
            user_y = np.random.uniform(0, area_side_length)
            users.append(User(user_x, user_y))

    return users

def plot_user_distribution(users, territory):
    area_side_length = np.sqrt(territory.area_size)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    for user in users:
        ax.plot(user.x, user.y, 'bo', markersize=3)

    ax.set_xlim(0, area_side_length)
    ax.set_ylim(0, area_side_length)
    ax.set_title('User Distribution Simulation')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.grid(True)

    plt.show()

# Пример использования модуля для симуляции и визуализации распределения пользователей
if __name__ == "__main__":
    territory = Territory(area_size=50)  # территория размером 50 км²
    num_users = 1000  # общее количество пользователей
    cluster_probability = 0.3  # вероятность того, что пользователи образуют кластеры

    users = simulate_user_distribution(territory, num_users, cluster_probability)
    plot_user_distribution(users, territory)

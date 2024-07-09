import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Параметры симуляции
area_size = 50  # Размер области (км)
num_uav = 10  # Количество UAV-BS
num_users = 1000  # Количество пользователей
simulation_steps = 100  # Количество временных слотов
uav_range = 5  # Радиус обслуживания UAV-BS (км)

# Инициализация позиций UAV-BS и пользователей
uav_positions = np.random.rand(num_uav, 2) * area_size
user_positions = np.random.rand(num_users, 2) * area_size

# Сохранение всех позиций UAV-BS на каждом шаге
uav_positions_over_time = np.zeros((simulation_steps, num_uav, 2))

def plot_positions(uav_positions, user_positions, step):
    plt.figure(figsize=(10, 10))
    plt.scatter(user_positions[:, 0], user_positions[:, 1], c='blue', label='Users')
    plt.scatter(uav_positions[:, 0], uav_positions[:, 1], c='red', label='UAV-BS')
    plt.xlim(0, area_size)
    plt.ylim(0, area_size)
    plt.title(f'UAV-BS and User Positions at Step {step}')
    plt.legend()
    plt.show()

def redistribute_uavs(uav_positions, user_positions, uav_range):
    new_positions = uav_positions.copy()
    for i in range(len(uav_positions)):
        users_in_range = np.linalg.norm(user_positions - uav_positions[i], axis=1) < uav_range
        if np.sum(users_in_range) < 10:  # Пороговое значение количества пользователей
            closest_uav = np.argmin(np.linalg.norm(uav_positions - uav_positions[i], axis=1) + np.eye(num_uav) * 1e6)
            direction = uav_positions[closest_uav] - uav_positions[i]
            new_positions[i] += direction / np.linalg.norm(direction) * 0.1  # Перемещение на 10%
    return new_positions

# Метод PADR
def padr_redistribute(uav_positions, user_positions, uav_range):
    new_positions = uav_positions.copy()
    for i in range(len(uav_positions)):
        # Считаем количество пользователей в радиусе действия
        users_in_range = np.linalg.norm(user_positions - uav_positions[i], axis=1) < uav_range
        if np.sum(users_in_range) < 10:  # Пороговое значение количества пользователей
            closest_uav = np.argmin(np.linalg.norm(uav_positions - uav_positions[i], axis=1) + np.eye(num_uav) * 1e6)
            direction = uav_positions[closest_uav] - uav_positions[i]
            new_positions[i] += direction / np.linalg.norm(direction) * 0.1  # Перемещение на 10%
    return new_positions

# Основной цикл симуляции
for step in range(simulation_steps):
    uav_positions = padr_redistribute(uav_positions, user_positions, uav_range)
    uav_positions_over_time[step] = uav_positions
    user_positions += np.random.randn(num_users, 2) * 0.1  # Динамическое изменение позиций пользователей

# Рассчет средних позиций UAV-BS
mean_uav_positions = np.mean(uav_positions_over_time, axis=0)

# Визуализация зон покрытия с использованием диаграмм Вороного
def plot_voronoi(uav_positions, user_positions, area_size):
    vor = Voronoi(uav_positions)
    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)
    ax.scatter(user_positions[:, 0], user_positions[:, 1], c='blue', label='Users')
    ax.scatter(uav_positions[:, 0], uav_positions[:, 1], c='red', label='UAV-BS')
    ax.set_xlim(0, area_size)
    ax.set_ylim(0, area_size)
    ax.set_title('Average UAV-BS Coverage Zones')
    ax.legend()
    plt.show()

# Визуализация распределения базовых станций с использованием метода PADR
def plot_padr_redistribution(uav_positions_over_time, user_positions, area_size):
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = plt.cm.viridis(np.linspace(0, 1, simulation_steps // 10))
    for t in range(0, simulation_steps, 10):
        ax.scatter(uav_positions_over_time[t][:, 0], uav_positions_over_time[t][:, 1], label=f'Step {t}', color=colors[t // 10])
        if t > 0:
            for i in range(num_uav):
                ax.plot([uav_positions_over_time[t-10][i, 0], uav_positions_over_time[t][i, 0]],
                        [uav_positions_over_time[t-10][i, 1], uav_positions_over_time[t][i, 1]], color=colors[t // 10])
    ax.scatter(user_positions[:, 0], user_positions[:, 1], c='blue', label='Users', alpha=0.3)
    ax.set_xlim(0, area_size)
    ax.set_ylim(0, area_size)
    ax.set_title('PADR UAV-BS Redistribution Over Time')
    ax.legend()
    plt.show()

plot_voronoi(mean_uav_positions, user_positions, area_size)
plot_padr_redistribution(uav_positions_over_time, user_positions, area_size)
print("Simulation completed.")

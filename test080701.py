import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.animation import FuncAnimation

# Параметры симуляции
area_size = 50  # Размер области (км)
num_uav = 10  # Количество UAV-BS
num_users = 1000  # Количество пользователей
simulation_steps = 100  # Количество временных слотов
uav_range = 5  # Радиус обслуживания UAV-BS (км)
movement_speed = 0.1  # Скорость движения UAV-BS (единицы расстояния за шаг)

# Инициализация позиций UAV-BS и пользователей
uav_positions = np.random.rand(num_uav, 2) * area_size
user_positions = np.random.rand(num_users, 2) * area_size

# Сохранение всех позиций UAV-BS на каждом шаге для обычного метода
uav_positions_over_time_basic = np.zeros((simulation_steps, num_uav, 2))

# Сохранение всех позиций UAV-BS на каждом шаге для метода PADR
uav_positions_over_time_padr = np.zeros((simulation_steps, num_uav, 2))

# Обычный метод перераспределения (простое движение к ближайшей базовой станции)
# Пример простого случайного движения для базового метода
def basic_redistribute(uav_positions, user_positions, movement_speed):
    new_positions = uav_positions.copy()
    for i in range(len(uav_positions)):
        # Движение в случайном направлении
        new_positions[i] += np.random.randn(2) * movement_speed
    return new_positions


# Метод PADR (Proximity-Aware Dynamic Redistribution)
def padr_redistribute(uav_positions, user_positions, uav_range, movement_speed):
    new_positions = uav_positions.copy()
    for i in range(len(uav_positions)):
        users_in_range = np.linalg.norm(user_positions - uav_positions[i], axis=1) < uav_range
        if np.sum(users_in_range) < 10:  # Пороговое значение количества пользователей
            closest_uav = np.argmin(np.linalg.norm(uav_positions - uav_positions[i], axis=1) + np.eye(num_uav) * 1e6)
            direction = uav_positions[closest_uav] - uav_positions[i]
            norm = np.linalg.norm(direction)
            if norm > 0:  # Проверка на нулевую норму
                new_positions[i] += direction / norm * movement_speed  # Перемещение на заданную скорость
    return new_positions

# Основной цикл симуляции
for step in range(simulation_steps):
    # Обычный метод
    uav_positions_basic = basic_redistribute(uav_positions, user_positions, movement_speed)
    uav_positions_over_time_basic[step] = uav_positions_basic.copy()
    
    # Метод PADR
    uav_positions_padr = padr_redistribute(uav_positions, user_positions, uav_range, movement_speed)
    uav_positions_over_time_padr[step] = uav_positions_padr.copy()
    
    # Обновление позиций пользователей каждые 10 шагов
    if step % 10 == 0:
        user_positions += np.random.randn(num_users, 2) * 0.1  # Моделирование движения пользователей

    # Обновление позиций UAV-BS
    uav_positions = uav_positions_basic  # Для базового метода

# Рассчет средних позиций UAV-BS для визуализации
mean_uav_positions_basic = np.mean(uav_positions_over_time_basic, axis=0)
mean_uav_positions_padr = np.mean(uav_positions_over_time_padr, axis=0)

# Визуализация зон покрытия с использованием диаграммы Вороного
def plot_voronoi(uav_positions, user_positions, area_size):
    valid_indices = ~np.isnan(uav_positions).any(axis=1)
    uav_positions = uav_positions[valid_indices]
    
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

# Анимация перераспределения UAV-BS с использованием обоих методов
def animate_redistribution(uav_positions_over_time_basic, uav_positions_over_time_padr, user_positions, area_size):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, area_size)
    ax.set_ylim(0, area_size)
    ax.set_title('Comparison of UAV-BS Redistribution Methods')
    ax.scatter(user_positions[:, 0], user_positions[:, 1], c='blue', label='Users', alpha=0.3)
    
    scatter_basic = ax.scatter([], [], c='green', label='Basic Method')
    scatter_padr = ax.scatter([], [], c='red', label='PADR Method')

    def update(frame):
        scatter_basic.set_offsets(uav_positions_over_time_basic[frame])
        scatter_padr.set_offsets(uav_positions_over_time_padr[frame])
        return scatter_basic, scatter_padr,

    anim = FuncAnimation(fig, update, frames=simulation_steps, interval=200, blit=True)
    plt.legend()
    plt.show()

# Визуализация
plot_voronoi(mean_uav_positions_basic, user_positions, area_size)
animate_redistribution(uav_positions_over_time_basic, uav_positions_over_time_padr, user_positions, area_size)
print("Simulation completed.")

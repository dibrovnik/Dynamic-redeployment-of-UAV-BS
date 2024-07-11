import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise  # библиотека для шума Перлина
def plot_territory_with_users_and_drones(users, drones, territory):
    area_side_length = np.sqrt(territory.area_size)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    # Рисуем пользователей
    for user in users:
        ax.plot(user.x, user.y, 'bo', markersize=3)

    # Рисуем дронов
    for drone in drones:
        ax.plot(drone.x, drone.y, 'rs', markersize=5)

    ax.set_xlim(0, area_side_length)
    ax.set_ylim(0, area_side_length)
    ax.set_title('Territory with Users and Drones')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.grid(True)

    plt.show()
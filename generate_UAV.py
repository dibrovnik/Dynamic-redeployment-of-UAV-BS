import numpy as np
import matplotlib.pyplot as plt

class Territory:
    def __init__(self, area_size):
        self.area_size = area_size  # площадь территории в квадратных километрах

class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def generate_random_drones(territory, num_drones):
    area_side_length = np.sqrt(territory.area_size)  # длина стороны квадрата, представляющего территорию

    drones = []

    for _ in range(num_drones):
        drone_x = np.random.uniform(0, area_side_length)
        drone_y = np.random.uniform(0, area_side_length)
        drones.append(Drone(drone_x, drone_y))

    return drones

def plot_drones(drones, territory):
    area_side_length = np.sqrt(territory.area_size)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')

    for drone in drones:
        ax.plot(drone.x, drone.y, 'rs', markersize=5)

    ax.set_xlim(0, area_side_length)
    ax.set_ylim(0, area_side_length)
    ax.set_title('Randomly Located Drones')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.grid(True)

    plt.show()

# Пример использования модуля для генерации и визуализации расположения дронов
if __name__ == "__main__":
    territory = Territory(area_size=50)  # территория размером 50 км²
    num_drones = 20  # количество дронов

    drones = generate_random_drones(territory, num_drones)
    plot_drones(drones, territory)

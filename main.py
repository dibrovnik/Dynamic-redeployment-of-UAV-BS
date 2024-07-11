from user_distribution_simulation_perlin import *
from generate_UAV import *
from visualizate import *

territory = Territory(area_size=50)  # территория размером 50 км²
num_users = 1000  # общее количество пользователей
cluster_probability = 0.8  # вероятность того, что пользователи образуют кластеры
perlin_scale = 0.1  # масштаб шума Перлина
perlin_octaves = 6  # количество октав шума Перлина
perlin_seed = None  # семя для воспроизводимости
num_drones = 20  # количество дронов

users = simulate_user_distribution(territory, num_users, cluster_probability, perlin_scale, perlin_octaves, perlin_seed)
drones = generate_random_drones(territory, num_drones)
plot_territory_with_users_and_drones(users,drones, territory)
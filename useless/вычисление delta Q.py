# import numpy as np
# from joblib import Parallel, delayed
# import time

# # Параметры симуляции
# area_size = 50  # квадратные километры
# num_uavs = 10  # количество базовых станций UAV
# flight_height_min = 50  # метры
# flight_height_max = 100  # метры
# time_slot_duration = 40  # секунды
# total_time_slots = 100
# alpha = 9.6117
# beta = 0.1581
# noise_power = 1e-15  # Вт
# SINR_threshold = 0  # дБ
# horizontal_speed = 10  # м/с
# vertical_speed = 5  # м/с
# transmit_power = 0.5  # Вт
# bandwidth = 1e6  # 1 МГц
# data_rate_requirement = [0.1, 1]  # Мбит/с

# num_experiments = 50

# # Функции для инициализации и обновления пользователей
# def initialize_users(area_size, total_time_slots):
#     return np.random.rand(total_time_slots, area_size, area_size)

# def update_user_distribution(users, t, area_size):
#     users[t, :, :] = np.random.rand(area_size, area_size)

# # Функция для разделения области на подблоки
# def partition_area(area_size, num_partitions):
#     partition_size = area_size // np.sqrt(num_partitions)
#     return int(partition_size)

# # Функция для назначения базовых станций UAV подблокам
# def assign_uavs_to_partitions(partition_size, num_uavs, area_size):
#     uav_positions = []
#     for _ in range(num_uavs):
#         x_partition = np.random.randint(0, area_size, partition_size)
#         y_partition = np.random.randint(0, area_size, partition_size)
#         height = np.random.uniform(flight_height_min, flight_height_max)
#         uav_positions.append([x_partition.mean(), y_partition.mean(), height])
#     return np.array(uav_positions)

# # Функция для перераспределения базовых станций UAV (базовый подход)
# def redeploy_uavs(uav_positions, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta):
#     for i in range(uav_positions.shape[0]):
#         user_demand = users[t, int(uav_positions[i, 0]), int(uav_positions[i, 1])]
#         if user_demand < 0.5:  # условие для перераспределения
#             uav_positions[i, 0] = (uav_positions[i, 0] + horizontal_speed * np.random.choice([-1, 1])) % area_size
#             uav_positions[i, 1] = (uav_positions[i, 1] + horizontal_speed * np.random.choice([-1, 1])) % area_size
#             uav_positions[i, 2] = np.clip(uav_positions[i, 2] + vertical_speed * np.random.choice([-1, 1]), flight_height_min, flight_height_max)
#     return uav_positions

# # Функция для адаптивного перераспределения базовых станций UAV
# def adaptive_redeploy_uavs(uav_positions, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta):
#     for i in range(uav_positions.shape[0]):
#         x, y, height = uav_positions[i]
#         user_demand = users[t, int(x), int(y)]
        
#         if user_demand < 0.5:  # условие для перераспределения
#             new_x = x + horizontal_speed * np.random.uniform(-1, 1)
#             new_y = y + horizontal_speed * np.random.uniform(-1, 1)
#             new_height = np.clip(height + vertical_speed * np.random.uniform(-1, 1), flight_height_min, flight_height_max)
            
#             new_x = new_x % area_size
#             new_y = new_y % area_size
            
#             uav_positions[i] = [new_x, new_y, new_height]
    
#     return uav_positions

# # Функция для оценки качества обслуживания (QoS) для базового подхода
# def evaluate_qos_basic(uav_positions, users, bandwidth, SINR_threshold, noise_power):
#     QoS = np.mean(users)  # Пример вычисления QoS (среднее значение пользователей)
#     return QoS

# # Основная функция для запуска эксперимента для базового подхода
# def run_experiment_basic(seed):
#     np.random.seed(seed)
    
#     users = initialize_users(area_size, total_time_slots)
#     uav_positions_basic = np.random.rand(num_uavs, 3) * area_size
    
#     results_basic = np.zeros(total_time_slots)
    
#     for t in range(total_time_slots):
#         update_user_distribution(users, t, area_size)
        
#         uav_positions_basic = redeploy_uavs(uav_positions_basic, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta)
#         QoS_basic = evaluate_qos_basic(uav_positions_basic, users[t], bandwidth, SINR_threshold, noise_power)
#         results_basic[t] = QoS_basic
    
#     return np.mean(results_basic)

# # Запуск серии экспериментов для базового подхода
# start_time_total = time.time()
# results_basic = Parallel(n_jobs=-1)(delayed(run_experiment_basic)(seed) for seed in range(num_experiments))
# end_time_total = time.time()

# # Вычисление среднего QoS для базового подхода
# mean_QoS_basic = np.mean(results_basic)

# # Вывод результатов
# print(f'Average QoS (Basic Approach): {mean_QoS_basic:.2f}')

# # Функция для вычисления ΔQ (разница QoS между PADR и базовым подходом)
# def compute_delta_Q(mean_QoS_padr, mean_QoS_basic):
#     return mean_QoS_padr - mean_QoS_basic

# # Пример использования compute_delta_Q после выполнения PADR
# mean_QoS_padr = 0.85  # Здесь должно быть вычислено среднее QoS для PADR
# delta_Q = compute_delta_Q(mean_QoS_padr, mean_QoS_basic)
# print(f'Delta Q (PADR vs Basic Approach): {delta_Q:.2f}')

import numpy as np
from joblib import Parallel, delayed
import time

# Параметры симуляции
area_size = 280  # квадратные километры
num_uavs = 10  # количество базовых станций UAV
flight_height_min = 50  # метры
flight_height_max = 100  # метры
time_slot_duration = 30  # секунды
total_time_slots = 100
alpha = 9.6117
beta = 0.1581
noise_power = 1e-15  # Вт
SINR_threshold = 0  # дБ
horizontal_speed = 10  # м/с
vertical_speed = 5  # м/с
transmit_power = 0.5  # Вт
bandwidth = 1e6  # 1 МГц
data_rate_requirement = [0.1, 1]  # Мбит/с

num_experiments = 50

# Функции для инициализации и обновления пользователей
def initialize_users(area_size, total_time_slots):
    return np.random.rand(total_time_slots, area_size, area_size)

def update_user_distribution(users, t, area_size):
    users[t, :, :] = np.random.rand(area_size, area_size)

# Функция для разделения области на подблоки
def partition_area(area_size, num_partitions):
    partition_size = area_size // np.sqrt(num_partitions)
    return int(partition_size)

# Функция для назначения базовых станций UAV подблокам
def assign_uavs_to_partitions(partition_size, num_uavs, area_size):
    uav_positions = []
    for _ in range(num_uavs):
        x_partition = np.random.randint(0, area_size, partition_size)
        y_partition = np.random.randint(0, area_size, partition_size)
        height = np.random.uniform(flight_height_min, flight_height_max)
        uav_positions.append([x_partition.mean(), y_partition.mean(), height])
    return np.array(uav_positions)

# Функция для перераспределения базовых станций UAV (PADR)
def redeploy_uavs_padr(uav_positions, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta):
    for i in range(uav_positions.shape[0]):
        x, y, height = uav_positions[i]
        user_demand = users[t, int(x), int(y)]
        
        if user_demand < 0.5:  # условие для перераспределения
            new_x = x + horizontal_speed * np.random.uniform(-1, 1)
            new_y = y + horizontal_speed * np.random.uniform(-1, 1)
            new_height = np.clip(height + vertical_speed * np.random.uniform(-1, 1), flight_height_min, flight_height_max)
            
            new_x = new_x % area_size
            new_y = new_y % area_size
            
            uav_positions[i] = [new_x, new_y, new_height]
    
    return uav_positions

# Функция для оценки качества обслуживания (QoS) для PADR
def evaluate_qos_padr(uav_positions, users, bandwidth, SINR_threshold, noise_power):
    QoS_values = np.zeros(users.shape[0])
    for t in range(users.shape[0]):
        # Пример вычисления QoS (среднее значение пользователей в текущем временном слоте)
        QoS_values[t] = np.mean(users[t])
    return np.mean(QoS_values)

# Основная функция для запуска эксперимента для PADR
def run_experiment_padr(seed):
    np.random.seed(seed)
    
    users = initialize_users(area_size, total_time_slots)
    uav_positions_padr = assign_uavs_to_partitions(partition_area(area_size, num_uavs), num_uavs, area_size)
    
    results_padr = np.zeros(num_experiments)
    
    for exp_idx in range(num_experiments):
        for t in range(total_time_slots):
            update_user_distribution(users, t, area_size)
            
            uav_positions_padr = redeploy_uavs_padr(uav_positions_padr, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta)
            QoS_padr = evaluate_qos_padr(uav_positions_padr, users[t], bandwidth, SINR_threshold, noise_power)
        
        results_padr[exp_idx] = QoS_padr
    
    return np.mean(results_padr)

# Запуск серии экспериментов для PADR
start_time_total = time.time()
mean_QoS_padr = run_experiment_padr(0)
end_time_total = time.time()

# Вывод результатов
print(f'Average QoS (PADR Approach): {mean_QoS_padr:.2f}')

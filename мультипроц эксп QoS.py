import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import time

num_experiments = 10


# Параметры симуляции
area_size = 50  # квадратные километры
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

# Функции для инициализации и обновления пользователей
def initialize_users(area_size, total_time_slots):
    return np.random.rand(total_time_slots, area_size, area_size)

def update_user_distribution(users, t, area_size):
    users[t, :, :] = np.random.rand(area_size, area_size)

# Функция для разделения области на подблоки
def partition_area(area_size, num_partitions):
    partition_size = area_size // np.sqrt(num_partitions)
    return int(partition_size)

# Функция для перераспределения базовых станций UAV (базовый подход)
def redeploy_uavs(uav_positions, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta):
    for i in range(uav_positions.shape[0]):
        user_demand = users[t, int(uav_positions[i, 0]), int(uav_positions[i, 1])]
        if user_demand < 0.5:  # условие для перераспределения
            uav_positions[i, 0] = (uav_positions[i, 0] + horizontal_speed * np.random.choice([-1, 1])) % area_size
            uav_positions[i, 1] = (uav_positions[i, 1] + horizontal_speed * np.random.choice([-1, 1])) % area_size
            uav_positions[i, 2] = np.clip(uav_positions[i, 2] + vertical_speed * np.random.choice([-1, 1]), flight_height_min, flight_height_max)
    return uav_positions

# Функция для назначения базовых станций UAV подблокам
def assign_uavs_to_partitions(partition_size, num_uavs, area_size):
    uav_positions = []
    for _ in range(num_uavs):
        x_partition = np.random.randint(0, area_size, partition_size)
        y_partition = np.random.randint(0, area_size, partition_size)
        height = np.random.uniform(flight_height_min, flight_height_max)
        uav_positions.append([x_partition.mean(), y_partition.mean(), height])
    return np.array(uav_positions)

# Адаптивный метод распределения UAV BSs
def adaptive_redeploy_uavs(uav_positions, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta):
    for i in range(uav_positions.shape[0]):
        x, y, height = uav_positions[i]
        user_demand = users[t, int(x), int(y)]
        
        if user_demand < 0.5:  # условие для перераспределения
            # Применение алгоритма оптимизации или адаптивного метода для изменения позиций
            # Пример: ройный алгоритм для оптимизации позиций
            new_x = x + horizontal_speed * np.random.uniform(-1, 1)
            new_y = y + horizontal_speed * np.random.uniform(-1, 1)
            new_height = np.clip(height + vertical_speed * np.random.uniform(-1, 1), flight_height_min, flight_height_max)
            
            # Проверка границ области
            new_x = new_x % area_size
            new_y = new_y % area_size
            
            uav_positions[i] = [new_x, new_y, new_height]
    
    return uav_positions

# Функция для оценки качества обслуживания (QoS)
# def evaluate_qos(uav_positions, users, bandwidth, SINR_threshold, noise_power):
#     QoS = np.random.rand()  # пример оценки качества
#     return QoS

def evaluate_qos(uav_positions, users, bandwidth, SINR_threshold, noise_power):
    num_time_slots = users.shape[0]
    num_users = users.shape[1]
    QoS_values = np.zeros(num_time_slots)
    
    for t in range(num_time_slots):
        total_interference = 0.0
        
        for i in range(uav_positions.shape[0]):
            x, y, height = uav_positions[i]
            
            # Рассчитываем расстояние между UAV и пользователями
            distances = np.sqrt((x - np.arange(num_users))**2 + (y - np.arange(num_users))**2)
            
            # Рассчитываем SINR для каждого пользователя
            received_power = transmit_power / (4 * np.pi * (height**2 + (distances * 1000)**2))
            interference_power = np.sum(transmit_power / (4 * np.pi * (height**2 + (distances * 1000)**2))) - received_power
            SINR = received_power / (interference_power + noise_power)
            
            # Подсчитываем количество пользователей с SINR выше порогового значения
            num_users_above_threshold = np.sum(SINR > SINR_threshold)
            
            # Вычисляем QoS как долю пользователей с достаточным SINR
            QoS_values[t] += num_users_above_threshold / num_users
        
        # Усредняем QoS по всем UAV и временным слотам
        QoS_values[t] /= uav_positions.shape[0]
    
    # Усредняем QoS по всем временным слотам
    QoS = np.mean(QoS_values)
    
    return QoS


# Функция для сглаживания данных
def smooth_data(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Основная функция для запуска эксперимента
def run_experiment(seed):
    np.random.seed(seed)
    
    # Инициализация пользователей и UAV BSs
    users = initialize_users(area_size, total_time_slots)
    uav_positions_basic = np.random.rand(num_uavs, 3) * area_size
    uav_positions_padr = assign_uavs_to_partitions(partition_area(area_size, num_uavs), num_uavs, area_size)
    uav_positions_adaptive = assign_uavs_to_partitions(partition_area(area_size, num_uavs), num_uavs, area_size)
    
    results_basic = np.zeros(total_time_slots)
    results_padr = np.zeros(total_time_slots)
    results_adaptive = np.zeros(total_time_slots)
    
    start_time_experiment = time.time()
    
    for t in range(total_time_slots):
        update_user_distribution(users, t, area_size)
        
        # Базовый подход
        uav_positions_basic = redeploy_uavs(uav_positions_basic, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta)
        QoS_basic = evaluate_qos(uav_positions_basic, users, bandwidth, SINR_threshold, noise_power)
        results_basic[t] = QoS_basic
        
        # PADR
        uav_positions_padr = redeploy_uavs(uav_positions_padr, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta)
        QoS_padr = evaluate_qos(uav_positions_padr, users, bandwidth, SINR_threshold, noise_power)
        results_padr[t] = QoS_padr
        
        # Адаптивный подход
        uav_positions_adaptive = adaptive_redeploy_uavs(uav_positions_adaptive, users, area_size, t, flight_height_min, flight_height_max, horizontal_speed, vertical_speed, transmit_power, bandwidth, SINR_threshold, noise_power, alpha, beta)
        QoS_adaptive = evaluate_qos(uav_positions_adaptive, users, bandwidth, SINR_threshold, noise_power)
        results_adaptive[t] = QoS_adaptive
    
    end_time_experiment = time.time()
    experiment_duration = end_time_experiment - start_time_experiment
    
    # Вычисление коэффициентов прироста
    average_basic = np.mean(results_basic)
    average_padr = np.mean(results_padr)
    average_adaptive = np.mean(results_adaptive)
    
    improvement_ratio_padr = (average_padr - average_basic) / average_basic * 100
    improvement_ratio_adaptive = (average_adaptive - average_basic) / average_basic * 100
    
    return improvement_ratio_padr, improvement_ratio_adaptive, experiment_duration

# Запуск серии экспериментов


start_time_total = time.time()
results = Parallel(n_jobs=-1)(delayed(run_experiment)(seed) for seed in range(num_experiments))
end_time_total = time.time()

# Разделение результатов по приросту для PADR и Adaptive
improvement_ratios_padr, improvement_ratios_adaptive, experiment_durations = zip(*results)

# Вывод средних значений коэффициентов прироста и времени выполнения
mean_improvement_ratio_padr = np.mean(improvement_ratios_padr)
mean_improvement_ratio_adaptive = np.mean(improvement_ratios_adaptive)
mean_experiment_duration = np.mean(experiment_durations)

print(f'Average Improvement Ratio (PADR vs Basic): {mean_improvement_ratio_padr:.2f}%')
print(f'Average Improvement Ratio (Adaptive vs Basic): {mean_improvement_ratio_adaptive:.2f}%')
print(f'Average Experiment Duration: {mean_experiment_duration:.2f} seconds')
print(f'Total Execution Time: {end_time_total - start_time_total:.2f} seconds')

import numpy as np
import matplotlib.pyplot as plt

# Параметры симуляции
area_size = 50  # 50 sq.km
min_altitude = 50  # meters
max_altitude = 100  # meters
time_slot_duration = 30  # seconds
service_duration = 100  # time slots
alpha = 9.6117
beta = 0.1581
sinr_threshold = 0  # dB
horizontal_speed = 10  # m/s
vertical_speed = 5  # m/s
horizontal_power = 240  # W
vertical_power = 80  # W
transmit_power = 0.5  # W
bandwidth = 1e6  # Hz
rate_min = 0.1e6  # 0.1 Mbps
rate_max = 1e6  # 1 Mbps
environmental_noise = 10e-15  # W

# Функция для расчета QoS
def calculate_qos(user_distribution, uav_positions):
    qos = 0
    for user in user_distribution:
        best_sinr = -np.inf
        for uav in uav_positions:
            distance = np.linalg.norm(np.array(user) - np.array(uav[:2]))
            sinr = transmit_power / (environmental_noise + distance**alpha + beta)
            if sinr > best_sinr:
                best_sinr = sinr
        if best_sinr >= sinr_threshold:
            qos += np.log2(1 + best_sinr)
    return qos

# Функция для симуляции GD
def gd_algorithm(user_distribution):
    # Глобальное распределение
    # Пример простого равномерного распределения UAV-BS по области
    uav_positions = []
    for i in range(5):  # предположим, что 5 UAV-BS
        x = np.random.uniform(0, area_size)
        y = np.random.uniform(0, area_size)
        z = np.random.uniform(min_altitude, max_altitude)
        uav_positions.append((x, y, z))
    return uav_positions

# Функция для симуляции PADR
def padr_algorithm(user_distribution, previous_uav_positions):
    # Локальное перераспределение
    uav_positions = []
    for uav in previous_uav_positions:
        x, y, z = uav
        x += np.random.uniform(-1, 1)  # случайное смещение
        y += np.random.uniform(-1, 1)  # случайное смещение
        z += np.random.uniform(-1, 1)  # случайное смещение
        uav_positions.append((x, y, z))
    return uav_positions

# Начальная генерация пользователей и UAV-BS
user_distribution = [(np.random.uniform(0, area_size), np.random.uniform(0, area_size)) for _ in range(100)]
uav_positions_gd = gd_algorithm(user_distribution)
uav_positions_padr = gd_algorithm(user_distribution)

# Массивы для хранения результатов
qos_gd = []
qos_padr = []

# Симуляция на протяжении временных слотов
for t in range(service_duration):
    uav_positions_gd = gd_algorithm(user_distribution)
    uav_positions_padr = padr_algorithm(user_distribution, uav_positions_padr)
    
    qos_gd.append(calculate_qos(user_distribution, uav_positions_gd))
    qos_padr.append(calculate_qos(user_distribution, uav_positions_padr))
    
    # Обновление положения пользователей (симуляция изменений среды)
    user_distribution = [(np.random.uniform(0, area_size), np.random.uniform(0, area_size)) for _ in range(100)]

# Оценка результата
delta_q = np.mean(qos_padr) - np.mean(qos_gd)
print(f"Средняя разница в QoS (PADR - GD): {delta_q}")

# Визуализация результатов
plt.plot(qos_gd, label='GD')
plt.plot(qos_padr, label='PADR')
plt.xlabel('Time Slot')
plt.ylabel('QoS')
plt.legend()
plt.show()

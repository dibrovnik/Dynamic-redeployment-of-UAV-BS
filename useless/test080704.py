import numpy as np
import matplotlib.pyplot as plt

# Параметры симуляции
area_size = 50  # Размер области в км^2
altitude_min = 50  # Минимальная высота UAV в метрах
altitude_max = 100  # Максимальная высота UAV в метрах
time_slot = 30  # Продолжительность одного временного слота в секундах
service_duration = 100  # Общее количество временных слотов
alpha = 9.6117
beta = 0.1581
delta_min = np.pi / 3  # Нижняя граница угла возвышения UAV в радианах
sigma_u = 10**-15  # Шумовая мощность в Вт
SINR_threshold = 0  # Пороговое значение SINR в дБ
uav_horizontal_speed = 10  # Горизонтальная скорость UAV в м/с
uav_vertical_speed = 5  # Вертикальная скорость UAV в м/с
uav_horizontal_power = 240  # Потребляемая мощность в горизонтальном полете в Вт
uav_vertical_power = 180  # Потребляемая мощность в вертикальном полете в Вт
uav_transmit_power = 0.5  # Передающая мощность UAV в Вт
bandwidth = 1e6  # Ширина полосы пропускания в Гц
rate_min = 0.1e6  # Минимальная требуемая скорость в бит/с
rate_max = 1e6  # Максимальная требуемая скорость в бит/с
epsilon_values = [0.25, 0.5, 0.75]  # Интенсивность изменений окружения

# Количество UAV и пользователей
initial_uav_count = 10
initial_user_count = 100

# Функция для генерации случайных изменений в окружении
def generate_environment_changes(area, user_count, uav_count, epsilon):
    area_1d = area.reshape(-1, 2)  # Преобразование в одномерный массив
    change_areas = area_1d[np.random.choice(len(area_1d), int(epsilon * len(area_1d)), replace=False)]
    for sub_area in change_areas:
        sub_area_tuple = tuple(sub_area)
        user_count[sub_area_tuple] = np.random.randint(0, initial_user_count)
        uav_count[sub_area_tuple] = max(0, uav_count[sub_area_tuple] + np.random.randint(-2, 3))  # Изменение количества UAV

# Функция для вычисления SINR
def calculate_sinr(uav_position, user_position):
    distance = np.linalg.norm(uav_position - user_position)
    path_loss = alpha * np.log10(distance) + beta
    received_power = uav_transmit_power / (10**(path_loss / 10))
    sinr = received_power / sigma_u
    return sinr

# Функция для вычисления QoS
def compute_qos(uav_positions, user_positions):
    qos_values = []
    for user_position in user_positions:
        sinr_values = [calculate_sinr(uav_position, user_position) for uav_position in uav_positions]
        max_sinr = max(sinr_values)
        qos = np.log2(1 + max_sinr)  # Пример вычисления QoS
        qos_values.append(qos)
    return np.mean(qos_values)

# Функция для перемещения UAV (PADR)
def padr(uav_positions, user_positions):
    new_uav_positions = []
    for uav_position in uav_positions:
        closest_user = user_positions[np.argmin(np.linalg.norm(user_positions - uav_position, axis=1))]
        direction = (closest_user - uav_position) / np.linalg.norm(closest_user - uav_position)
        new_position = uav_position + direction * uav_horizontal_speed
        new_uav_positions.append(new_position)
    return np.array(new_uav_positions)

# Основная симуляция
def run_simulation(epsilon, strategy):
    area = np.array([[x, y] for x in range(int(np.sqrt(area_size))) for y in range(int(np.sqrt(area_size)))])
    user_positions = np.random.rand(initial_user_count, 2) * np.sqrt(area_size)
    uav_positions = np.random.rand(initial_uav_count, 2) * np.sqrt(area_size)
    user_count = {tuple(pos): initial_user_count // len(area) for pos in area}
    uav_count = {tuple(pos): initial_uav_count // len(area) for pos in area}
    
    qos_values = []
    avg_flight_times = []
    avg_energy_efficiencies = []

    for t in range(service_duration):
        generate_environment_changes(area, user_count, uav_count, epsilon)
        
        if strategy == 'PADR':
            new_uav_positions = padr(uav_positions, user_positions)
        elif strategy == 'GD':
            new_uav_positions = user_positions[np.random.choice(range(len(user_positions)), len(uav_positions))]

        flight_times = np.linalg.norm(new_uav_positions - uav_positions, axis=1) / uav_horizontal_speed
        energy_efficiencies = uav_transmit_power / (uav_transmit_power + uav_horizontal_power + uav_vertical_power)
        
        qos = compute_qos(new_uav_positions, user_positions)
        
        qos_values.append(qos)
        avg_flight_times.append(np.mean(flight_times))
        avg_energy_efficiencies.append(np.mean(energy_efficiencies))

        uav_positions = new_uav_positions

    return qos_values, avg_flight_times, avg_energy_efficiencies

# Запуск симуляций для разных значений epsilon и стратегий
results = {}
for epsilon in epsilon_values:
    for strategy in ['PADR', 'GD']:
        qos, flight_times, energy_efficiencies = run_simulation(epsilon, strategy)
        results[(epsilon, strategy)] = {
            'qos': qos,
            'flight_times': flight_times,
            'energy_efficiencies': energy_efficiencies
        }

# Построение графиков
fig, axs = plt.subplots(3, 1, figsize=(10, 15))
for epsilon in epsilon_values:
    axs[0].plot(results[(epsilon, 'PADR')]['qos'], label=f'PADR, ε={epsilon}')
    axs[0].plot(results[(epsilon, 'GD')]['qos'], label=f'GD, ε={epsilon}')
    axs[1].plot(results[(epsilon, 'PADR')]['flight_times'], label=f'PADR, ε={epsilon}')
    axs[1].plot(results[(epsilon, 'GD')]['flight_times'], label=f'GD, ε={epsilon}')
    axs[2].plot(results[(epsilon, 'PADR')]['energy_efficiencies'], label=f'PADR, ε={epsilon}')
    axs[2].plot(results[(epsilon, 'GD')]['energy_efficiencies'], label=f'GD, ε={epsilon}')

axs[0].set_title('QoS Over Time')
axs[0].set_xlabel('Time Slot')
axs[0].set_ylabel('QoS')
axs[0].legend()

axs[1].set_title('Average Flight Time Over Time')
axs[1].set_xlabel('Time Slot')
axs[1].set_ylabel('Flight Time (s)')
axs[1].legend()

axs[2].set_title('Average Energy Efficiency Over Time')
axs[2].set_xlabel('Time Slot')
axs[2].set_ylabel('Energy Efficiency')
axs[2].legend()

plt.tight_layout()
plt.show()

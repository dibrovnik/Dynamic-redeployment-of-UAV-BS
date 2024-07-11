import numpy as np

# Параметры системы
area_size = (1000, 1000)  # Размер области (ширина, высота)
num_uavs = 10  # Количество UAV
num_users = 100  # Количество пользователей
time_slots = 10  # Количество временных слотов

# Параметры UAV
uav_height = 100  # Высота UAV
uav_power = 1  # Мощность передатчика UAV
noise_power = 0.1  # Мощность шума

# Инициализация позиций пользователей и UAV
user_positions = np.random.rand(num_users, 2) * area_size
uav_positions = np.random.rand(num_uavs, 2) * area_size

# Функция для вычисления расстояния между точками
def distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Функция для вычисления SINR
def compute_sinr(user_pos, uav_pos, uav_positions, uav_power, noise_power):
    d = distance(user_pos, uav_pos)
    if d == 0:  # Avoid division by zero
        return float('inf')
    signal_power = uav_power / (d ** 2)
    interference = sum(uav_power / (distance(user_pos, pos) ** 2) for pos in uav_positions if not np.array_equal(pos, uav_pos))
    sinr = signal_power / (interference + noise_power)
    return sinr

# Функция для оценки качества обслуживания
def evaluate_qos(user_positions, uav_positions, uav_power, noise_power):
    sinr_values = [
        compute_sinr(user_pos, uav_positions[np.argmin([distance(user_pos, uav_pos) for uav_pos in uav_positions])], uav_positions, uav_power, noise_power)
        for user_pos in user_positions
    ]
    return np.mean(sinr_values), np.min(sinr_values)

# Имитация динамических изменений и перераспределения UAV
for t in range(time_slots):
    # Динамическое изменение позиций пользователей
    user_positions += (np.random.rand(num_users, 2) - 0.5) * 10
    user_positions = np.clip(user_positions, 0, area_size[0])

    # Перераспределение UAV
    # Простой пример: перемещение UAV ближе к центру масс пользователей
    center_of_mass = np.mean(user_positions, axis=0)
    uav_positions += (center_of_mass - uav_positions) * 0.1

    # Оценка качества обслуживания
    avg_sinr, min_sinr = evaluate_qos(user_positions, uav_positions, uav_power, noise_power)
    print(f"Time slot {t+1}: Average SINR = {avg_sinr:.2f}, Minimum SINR = {min_sinr:.2f}")

    # Отладочный вывод для проверки значений
    if t == 0:  # Вывод только для первого временного слота для краткости
        for i, user_pos in enumerate(user_positions):
            uav_idx = np.argmin([distance(user_pos, uav_pos) for uav_pos in uav_positions])
            sinr = compute_sinr(user_pos, uav_positions[uav_idx], uav_positions, uav_power, noise_power)
            print(f"User {i}: SINR = {sinr:.2f}")

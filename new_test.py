import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры симуляции
AREA_SIZE = 5000  # в метрах, т.е. 50 км²
TIME_SLOT = 30  # временной слот в секундах
SERVICE_DURATION = 100  # длительность обслуживания в временных слотах
ALPHA = 9.6117
BETA = 0.1581
ELEVATION_ANGLE = np.pi / 3
NOISE_POWER = 1e-15  # в Вт
SINR_THRESHOLD = 0  # в дБ
HORIZONTAL_SPEED = 10  # горизонтальная скорость БПЛА в м/с
VERTICAL_SPEED = 5  # вертикальная скорость БПЛА в м/с
POWER_CONSUMPTION_HORIZONTAL = 240  # потребляемая мощность горизонтального полета в Вт
POWER_CONSUMPTION_VERTICAL = 180  # потребляемая мощность вертикального полета в Вт
TRANSMIT_POWER = 0.5  # передающая мощность БПЛА в Вт
BANDWIDTH = 1e6  # ширина полосы пропускания в Гц
DATA_RATE_MIN = 0.1e6  # минимальная требуемая скорость передачи данных в бит/с
DATA_RATE_MAX = 1e6  # максимальная требуемая скорость передачи данных в бит/с
ENVIRONMENT_CHANGE_INTENSITY = [0.25, 0.5, 0.75]  # интенсивность изменений окружения

class Simulation:
    def __init__(self):
        self.time_slots = SERVICE_DURATION
        self.area_size = AREA_SIZE
        self.bpla_positions = []  # список для хранения позиций БПЛА
        self.user_positions = []  # список для хранения позиций пользователей
        self.init_simulation()

    def init_simulation(self):
        # Инициализация начальных положений БПЛА и пользователей
        num_bpla = 10
        num_users = 1000
        
        # Распределение БПЛА по случайным позициям в области
        self.bpla_positions = np.random.uniform(0, self.area_size, size=(num_bpla, 2))
        
        # Распределение пользователей по случайным позициям в области
        self.user_positions = np.random.uniform(0, self.area_size, size=(num_users, 2))

    def generate_environment_changes(self):
        # Генерация изменений окружения (пользователи, БПЛА)
        for intensity in ENVIRONMENT_CHANGE_INTENSITY:
            num_changes = int(intensity * len(self.user_positions))
            user_indices = np.random.choice(len(self.user_positions), num_changes, replace=False)
            self.user_positions[user_indices] = np.random.uniform(0, self.area_size, size=(num_changes, 2))
            
            num_changes = int(intensity * len(self.bpla_positions))
            bpla_indices = np.random.choice(len(self.bpla_positions), num_changes, replace=False)
            self.bpla_positions[bpla_indices] = np.random.uniform(0, self.area_size, size=(num_changes, 2))

    def compute_sinr(self, bpla_position, user_position):
        # Вычисление SINR для данного БПЛА и пользователя
        distance = np.linalg.norm(bpla_position - user_position)
        received_power = self.compute_received_power(distance)
        interference = self.compute_interference(bpla_position, user_position)
        sinr = received_power / (interference + NOISE_POWER)
        return sinr

    def compute_received_power(self, distance):
        # Вычисление полученной мощности на основе модели распространения
        received_power = TRANSMIT_POWER / (distance**ALPHA)
        return received_power

    def compute_interference(self, bpla_position, user_position):
        # Вычисление интерференции от других БПЛА или источников
        interference = 0.0
        for other_bpla_pos in self.bpla_positions:
            if not np.array_equal(other_bpla_pos, bpla_position):
                distance = np.linalg.norm(other_bpla_pos - user_position)
                interference += TRANSMIT_POWER / (distance**ALPHA)
        return interference

    def evaluate_qos_for_bpla(self, bpla_position):
        # Вычисление QoS для данного положения БПЛА
        nearest_users = self.find_nearest_users(bpla_position)
        total_qos = 0.0
        
        for user_pos in nearest_users:
            sinr = self.compute_sinr(bpla_position, user_pos)
            if sinr > SINR_THRESHOLD:
                qos = np.log2(1 + sinr)
            else:
                qos = 0.0  # если SINR меньше порогового значения, QoS считаем нулевым
            total_qos += qos
        
        # Возвращаем среднее значение QoS для всех пользователей
        return total_qos / len(nearest_users) if len(nearest_users) > 0 else 0.0

    def find_nearest_users(self, bpla_position):
        # Нахождение ближайших пользователей к данной позиции БПЛА
        distances = np.linalg.norm(self.user_positions - bpla_position, axis=1)
        sorted_indices = np.argsort(distances)
        nearest_users = self.user_positions[sorted_indices[:10]]  # выбираем 10 ближайших пользователей
        return nearest_users

    def move_bpla_gd(self):
        # Метод глобального размещения (GD)
        for idx in range(len(self.bpla_positions)):
            dx = np.random.uniform(-HORIZONTAL_SPEED * TIME_SLOT, HORIZONTAL_SPEED * TIME_SLOT)
            dy = np.random.uniform(-VERTICAL_SPEED * TIME_SLOT, VERTICAL_SPEED * TIME_SLOT)
            self.bpla_positions[idx][0] += dx
            self.bpla_positions[idx][1] += dy
            # Проверка на границы области
            self.bpla_positions[idx][0] = max(0, min(self.bpla_positions[idx][0], self.area_size))
            self.bpla_positions[idx][1] = max(0, min(self.bpla_positions[idx][1], self.area_size))

    def move_bpla_padr(self):
        # Метод адаптивного размещения на основе потенциала (PADR)
        learning_rate = 0.1
        
        for idx in range(len(self.bpla_positions)):
            current_qos = self.evaluate_qos_for_bpla(self.bpla_positions[idx])
            direction = np.random.uniform(-1, 1, 2)
            direction /= np.linalg.norm(direction)
            
            self.bpla_positions[idx][0] += learning_rate * direction[0]
            self.bpla_positions[idx][1] += learning_rate * direction[1]
            # Проверка на границы области
            self.bpla_positions[idx][0] = max(0, min(self.bpla_positions[idx][0], self.area_size))
            self.bpla_positions[idx][1] = max(0, min(self.bpla_positions[idx][1], self.area_size))

    def run_simulation(self):
        for t in range(self.time_slots):
            self.generate_environment_changes()
            self.move_bpla_gd()  # или self.move_bpla_gd(), в зависимости от выбранного метода

    def plot_animation(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.area_size)
        ax.set_ylim(0, self.area_size)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Dynamic Redistribution of UAV-BS')

        scat = ax.scatter([], [])

        def update(frame):
            positions = self.bpla_positions
            scat.set_offsets(positions)
            return scat,

        ani = animation.FuncAnimation(fig, update, frames=self.time_slots, interval=500, blit=True)
        plt.show()

simulation = Simulation()
simulation.run_simulation()
simulation.plot_animation()

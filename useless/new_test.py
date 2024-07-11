import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.cluster import KMeans

# Параметры симуляции
AREA_SIZE = 5000  # в метрах, т.е. 50 км²
TRANSMIT_POWER = 0.5  # передающая мощность БПЛА в Вт
ALPHA = 9.6117
NOISE_POWER = 1e-15  # в Вт

class Simulation:
    def __init__(self):
        self.area_size = AREA_SIZE
        self.bpla_positions_gd = []  # список для хранения позиций БПЛА (GD)
        self.bpla_positions_padr = []  # список для хранения позиций БПЛА (PADR)
        self.user_positions = []  # список для хранения позиций пользователей
        self.init_simulation()

    def init_simulation(self):
        # Инициализация начальных положений БПЛА и пользователей
        num_bpla = 10
        num_users = 1000
        
        # Распределение БПЛА по случайным позициям в области для GD
        self.bpla_positions_gd = np.random.uniform(0, self.area_size, size=(num_bpla, 2))
        
        # Распределение БПЛА по случайным позициям в области для PADR (используем GD как базовую точку)
        self.bpla_positions_padr = np.copy(self.bpla_positions_gd)
        
        # Распределение пользователей по случайным позициям в области
        self.user_positions = np.random.uniform(0, self.area_size, size=(num_users, 2))

    def generate_environment_changes(self, intensity):
        # Генерация изменений окружения (пользователи, БПЛА)
        num_changes = int(intensity * len(self.user_positions))
        change_indices = np.random.choice(len(self.user_positions), num_changes, replace=False)

        for idx in change_indices:
            self.user_positions[idx] = np.random.uniform(0, self.area_size, size=2)

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
        for other_bpla_pos in self.bpla_positions_gd:
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
            if sinr > 0:  # Пороговое значение SINR равно 0 дБ
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
        for idx in range(len(self.bpla_positions_gd)):
            dx = np.random.uniform(-10, 10)
            dy = np.random.uniform(-5, 5)
            self.bpla_positions_gd[idx][0] += dx
            self.bpla_positions_gd[idx][1] += dy
            # Проверка на границы области
            self.bpla_positions_gd[idx][0] = max(0, min(self.bpla_positions_gd[idx][0], self.area_size))
            self.bpla_positions_gd[idx][1] = max(0, min(self.bpla_positions_gd[idx][1], self.area_size))
    def move_bpla_padr(self):
        # Метод адаптивного размещения на основе потенциала (PADR)

        # Кластеризуем текущие позиции БПЛА
        try:
            kmeans = KMeans(n_clusters=len(self.bpla_positions_padr), init=self.bpla_positions_padr, n_init=1)
            kmeans.fit(self.bpla_positions_padr)
            cluster_centers = kmeans.cluster_centers_
        except :
            # Если возникает предупреждение о сходимости, генерируем случайные начальные центры
            cluster_centers = np.random.uniform(0, self.area_size, size=(len(self.bpla_positions_padr), 2))

        for idx in range(len(self.bpla_positions_padr)):
            current_qos = self.evaluate_qos_for_bpla(self.bpla_positions_padr[idx])
            learning_rate = 0.1  # начальный learning rate
            max_iterations = 10  # максимальное количество итераций для поиска улучшения QoS
            iteration = 0

            best_position = np.copy(self.bpla_positions_padr[idx])

            while iteration < max_iterations:
                # Вычисляем направление кластера
                direction = cluster_centers[idx] - self.bpla_positions_padr[idx]
                if np.linalg.norm(direction) > 0:
                    direction /= np.linalg.norm(direction)  # нормируем вектор направления

                # Вычисляем новое положение БПЛА
                new_position = self.bpla_positions_padr[idx] + learning_rate * direction

                # Проверяем границы области
                new_position[0] = max(0, min(new_position[0], self.area_size))
                new_position[1] = max(0, min(new_position[1], self.area_size))

                # Оцениваем новое QoS
                new_qos = self.evaluate_qos_for_bpla(new_position)

                # Если новое положение улучшает QoS, то принимаем его
                if new_qos > current_qos:
                    self.bpla_positions_padr[idx] = new_position
                    break
                else:
                    # Иначе уменьшаем learning rate и повторяем попытку
                    learning_rate *= 0.9
                    iteration += 1

    # def move_bpla_padr(self):
    #     # Метод адаптивного размещения на основе потенциала (PADR)
    #     for idx in range(len(self.bpla_positions_padr)):
    #         current_qos = self.evaluate_qos_for_bpla(self.bpla_positions_padr[idx])
    #         learning_rate = 0.1  # начальный learning rate
    #         max_speed = 10.0  # максимальная скорость перемещения в метрах
    #         max_iterations = 10  # максимальное количество итераций для поиска улучшения QoS
    #         iteration = 0
            
    #         while iteration < max_iterations:
    #             direction = np.random.randn(2)  # случайное направление для изменения позиции
    #             direction /= np.linalg.norm(direction)  # нормируем вектор направления
                
    #             # Вычисляем новое положение БПЛА
    #             new_position = self.bpla_positions_padr[idx] + learning_rate * direction
                
    #             # Проверяем границы области
    #             new_position[0] = max(0, min(new_position[0], self.area_size))
    #             new_position[1] = max(0, min(new_position[1], self.area_size))
                
    #             # Оцениваем новое QoS
    #             new_qos = self.evaluate_qos_for_bpla(new_position)
                
    #             # Если новое положение улучшает QoS, то принимаем его
    #             if new_qos > current_qos:
    #                 self.bpla_positions_padr[idx] = new_position
    #                 break
    #             else:
    #                 # Иначе уменьшаем learning rate и повторяем попытку
    #                 learning_rate *= 0.9
    #                 iteration += 1
        


    def plot_coverage_zones(self, ax, bpla_positions):
        # Отображение зон покрытия БПЛА-БС
        for bpla_pos in bpla_positions:
            coverage_circle = plt.Circle((bpla_pos[0], bpla_pos[1]), ALPHA * (TRANSMIT_POWER / NOISE_POWER)**(1/ALPHA), color='gray', fill=False)
            ax.add_artist(coverage_circle)

    def update_plot(self, frame):
        # Обновление данных и визуализации для анимации
        self.generate_environment_changes(1)  # изменения окружения с интенсивностью 0.5
        
        self.move_bpla_gd()  # перемещение БПЛА по методу GD
        self.move_bpla_padr()  # перемещение БПЛА по методу PADR
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.set_xlim(0, self.area_size)
        self.ax1.set_ylim(0, self.area_size)
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_title('GD Method')
        self.plot_coverage_zones(self.ax1, self.bpla_positions_gd)
        self.ax1.scatter(self.bpla_positions_gd[:, 0], self.bpla_positions_gd[:, 1], color='blue', label='UAV-BS (GD)')
        self.ax1.scatter(self.user_positions[:, 0], self.user_positions[:, 1], color='red', label='Users')
        self.ax1.legend()

        self.ax2.set_xlim(0, self.area_size)
        self.ax2.set_ylim(0, self.area_size)
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_title('PADR Method')
        self.plot_coverage_zones(self.ax2, self.bpla_positions_padr)
        self.ax2.scatter(self.bpla_positions_padr[:, 0], self.bpla_positions_padr[:, 1], color='green', label='UAV-BS (PADR)')
        self.ax2.scatter(self.user_positions[:, 0], self.user_positions[:, 1], color='red', label='Users')
        self.ax2.legend()

        self.ax3.set_xlim(0, self.area_size)
        self.ax3.set_ylim(0, self.area_size)
        self.ax3.set_xlabel('X')
        self.ax3.set_ylabel('Y')
        self.ax3.set_title('Comparison: GD vs PADR')
        self.plot_coverage_zones(self.ax3, self.bpla_positions_gd)
        self.plot_coverage_zones(self.ax3, self.bpla_positions_padr)
        self.ax3.scatter(self.bpla_positions_gd[:, 0], self.bpla_positions_gd[:, 1], color='blue', label='UAV-BS (GD)')
        self.ax3.scatter(self.bpla_positions_padr[:, 0], self.bpla_positions_padr[:, 1], color='green', label='UAV-BS (PADR)')
        self.ax3.scatter(self.user_positions[:, 0], self.user_positions[:, 1], color='red', label='Users')
        self.ax3.legend()

    def animate_simulation(self, num_time_slots=100):
        # Создаем новое окно с графиками
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        self.ax1 = axs[0]
        self.ax2 = axs[1]
        self.ax3 = axs[2]

        # Запускаем анимацию
        animation = FuncAnimation(fig, self.update_plot, frames=num_time_slots, repeat=False)
        plt.tight_layout()
        plt.show()

# Запуск симуляции с анимацией
simulation = Simulation()
simulation.animate_simulation(num_time_slots=100)

import simpy
import random
import numpy as np

# Параметры
NUM_UAVS = 10
SIM_TIME = 100
FLIGHT_DURATION = 5  # Время, которое БПЛА проводит в полете
SERVICE_DURATION = 15  # Время, которое БПЛА проводит в состоянии обслуживания
AREA_SIZE = (100, 100)  # Размеры области обслуживания
PARTITION_SIZE = (20, 20)  # Размеры подблоков
NUM_USERS = 50  # Количество пользователей
SERVICE_RADIUS = 10  # Радиус обслуживания БПЛА

class User:
    def __init__(self, env, user_id, location):
        
        self.user_id = user_id
        self.location = location
        self.served = False

class UAV:
    def __init__(self, env, uav_id, partitions):
        
        self.uav_id = uav_id
        self.partitions = partitions
        self.current_partition = None
        self.location = None
        self.action = env.process(self.run())
    
    def run(self):
        while True:
            # Переход в состояние полета
            flight_time = random.expovariate(1.0 / FLIGHT_DURATION)
            yield self.env.timeout(flight_time)
            
            # Назначение нового подблока
            self.current_partition = random.choice(self.partitions)
            self.location = (random.uniform(self.current_partition[0] * PARTITION_SIZE[0], 
                                            (self.current_partition[0] + 1) * PARTITION_SIZE[0]),
                             random.uniform(self.current_partition[1] * PARTITION_SIZE[1], 
                                            (self.current_partition[1] + 1) * PARTITION_SIZE[1]))

            # Состояние обслуживания
            service_time = random.expovariate(1.0 / SERVICE_DURATION)
            yield self.env.timeout(service_time)

def setup(env, num_uavs, partitions, users):
    for i in range(num_uavs):
        UAV(env, i, partitions)
    
    # Мониторинг эффективности
    env.process(monitor_efficiency(env, users))

def create_partitions(area_size, partition_size):
    partitions = []
    num_partitions_x = area_size[0] // partition_size[0]
    num_partitions_y = area_size[1] // partition_size[1]
    for i in range(num_partitions_x):
        for j in range(num_partitions_y):
            partitions.append((i, j))
    return partitions

def create_users(num_users, area_size):
    users = []
    for i in range(num_users):
        location = (random.uniform(0, area_size[0]), random.uniform(0, area_size[1]))
        users.append(User(env, i, location))
    return users

def distance(loc1, loc2):
    return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def monitor_efficiency(env, users):
    while True:
        for user in users:
            user.served = False
            for uav in env.active_process:
                if uav.current_partition and distance(user.location, uav.location) <= SERVICE_RADIUS:
                    user.served = True
                    break
        # Печать результата каждые 10 единиц времени
        yield env.timeout(10)
        served_users = sum(user.served for user in users)
        print(f'Время {env.now}: обслужено {served_users} из {NUM_USERS} пользователей')

# Создание подблоков и пользователей
partitions = create_partitions(AREA_SIZE, PARTITION_SIZE)
users = create_users(NUM_USERS, AREA_SIZE)

# Настройка и запуск симуляции
env = simpy.Environment()
setup(env, NUM_UAVS, partitions, users)
env.run(until=SIM_TIME)

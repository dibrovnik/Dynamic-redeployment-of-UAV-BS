import numpy as np

class Drone:
    def __init__(self, id, position):
        self.id = id
        self.position = position

class BaseStation:
    def __init__(self, id, position):
        self.id = id
        self.position = position

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def calculate_sinr(signal_power, interference_power, noise_power):
    return signal_power / (interference_power + noise_power)

def allocate_base_stations(drones, base_stations):
    allocations = {}
    for drone in drones:
        best_station = None
        best_sinr = -np.inf
        for station in base_stations:
            distance = calculate_distance(drone.position, station.position)
            signal_power = 1 / (distance ** 2)  # Simplified signal power model
            interference_power = sum(1 / (calculate_distance(drone.position, bs.position) ** 2) for bs in base_stations if bs != station)
            noise_power = 0.01  # Example noise power level
            sinr = calculate_sinr(signal_power, interference_power, noise_power)
            if sinr > best_sinr:
                best_sinr = sinr
                best_station = station
        allocations[drone.id] = best_station.id
    return allocations

def evaluate_qos(drones, base_stations):
    qos_scores = {}
    for drone in drones:
        station = base_stations[allocate_base_stations(drones, base_stations)[drone.id]]
        distance = calculate_distance(drone.position, station.position)
        signal_power = 1 / (distance ** 2)
        interference_power = sum(1 / (calculate_distance(drone.position, bs.position) ** 2) for bs in base_stations if bs != station)
        noise_power = 0.01
        sinr = calculate_sinr(signal_power, interference_power, noise_power)
        qos_scores[drone.id] = sinr
    return qos_scores

# Example usage
drones = [Drone(id=1, position=(0, 0)), Drone(id=2, position=(10, 10))]
base_stations = [BaseStation(id=1, position=(5, 5)), BaseStation(id=2, position=(15, 15))]

allocations = allocate_base_stations(drones, base_stations)
qos_scores = evaluate_qos(drones, base_stations)

print("Base station allocations:")
for drone_id, station_id in allocations.items():
    print(f"Drone {drone_id} allocated to Base Station {station_id}")

print("\nQoS Scores (SINR):")
for drone_id, sinr in qos_scores.items():
    print(f"Drone {drone_id}: SINR = {sinr:.2f}")

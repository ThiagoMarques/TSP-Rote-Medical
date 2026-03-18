import math
import random


CITIES = [
    (512, 317),  # 0 - hospital
    (741, 72),   # 1
    (552, 50),   # 2
    (589, 131),  # 3
    (576, 216),  # 4
]

HOSPITAL = CITIES[0]
POPULATION_SIZE = 20

def distance(city1, city2):
    """Distância em linha reta entre dois pontos (x, y)."""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(path, start):
    """Distância total de um roteiro."""
    if not path:
        return 0.0
    d = distance(path[-1], start)
    for i in range(len(path) - 1):
        d += distance(path[i], path[i + 1])
    d += distance(path[-1], start)
    return d

def random_route():
    """Roteiro aleatório entre as cidades."""
    deliveries = CITIES[1:]
    return random.sample(deliveries, len(deliveries))

if __name__ == "__main__":
    print("Cidades:", len(CITIES), "pontos")
    print("Hospital:", HOSPITAL)

    population = [random_route() for _ in range(POPULATION_SIZE)]
    fitness_list = [total_distance(route, HOSPITAL) for route in population]
    # Ordenar: menor distância = melhor (índice 0 = melhor)
    sorted_pairs = sorted(zip(population, fitness_list), key=lambda p: p[1])
    best_route, best_dist = sorted_pairs[0]
    print("Melhor distância desta geração:", best_dist)
    print("Melhor rota (primeiros 3):", best_route[:3])
import math
import random


CITIES = [
    (512, 317),  # 0 - hospital
    (741, 72),   # 1
    (552, 50),   # 2
    (589, 131),  # 3
    (576, 216),  # 4
]
city_to_id = {coord: i for i, coord in enumerate(CITIES)}

def distance(city1, city2):
    """Distância em linha reta entre dois pontos (x, y)."""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def build_distance_matrix(cities):
    """Matriz de distâncias entre todas as cidades."""
    n = len(cities)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(cities[i], cities[j])
            D[i][j] = D[j][i] = d
    return D

# Matriz de distâncias entre todas as cidades
distance_matrix = build_distance_matrix(CITIES)

HOSPITAL = CITIES[0]
POPULATION_SIZE = 20

N_GENERATIONS = 50
MUTATION_PROB = 0.3
TOP_FOR_SELECTION = 10

# Prioridade por city_id (0=hospital não conta na penalidade; 1=crítico, 2=regular, 3=insumo)
PRIORITIES = {0: 0, 1: 0, 2: 1, 3: 2, 4: 1}

DEMANDS = {0: 0, 1: 3, 2: 2, 3: 1, 4: 2}
VEHICLE_CAPACITY = 10

def route_knn(cities, hospital):
    rest = [c for c in cities if c != hospital]
    route = []
    current = hospital
    while rest:
        nearest = min(rest, key=lambda c: distance(current, c))
        route.append(nearest)
        rest.remove(nearest)
        current = nearest
    return route

def total_distance_with_matrix(route, hospital, city_to_id, matrix):
    hid = city_to_id[hospital]
    ids = [city_to_id[c] for c in route]
    dist = matrix[hid][ids[0]]
    for i in range(len(ids) - 1):
        dist += matrix[ids[i]][ids[i + 1]]
    dist += matrix[ids[-1]][hid]
    return dist

def total_distance(path, start):
    """Distância total de um roteiro."""
    if not path:
        return 0.0
    d = distance(start, path[0])
    for i in range(len(path) - 1):
        d += distance(path[i], path[i + 1])
    d += distance(path[-1], start)
    return d

def random_route():
    """Roteiro aleatório entre as cidades."""
    deliveries = CITIES[1:]
    return random.sample(deliveries, len(deliveries))

def order_crossover(parent1, parent2):
    """Crossover OX: copia um trecho de parent1 e preenche o resto na ordem de parent2."""
    n = len(parent1)
    start = random.randint(0, n - 1)
    end = random.randint(start + 1, n)
    child = [None] * n
    child[start:end] = parent1[start:end]
    rest = [g for g in parent2 if g not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = rest[j]
            j += 1
    return child

def mutate(route, prob):
    """Com probabilidade prob, troca dois pontos consecutivos da rota."""
    out = list(route)
    if random.random() < prob and len(out) >= 2:
        i = random.randint(0, len(out) - 2)
        out[i], out[i + 1] = out[i + 1], out[i]
    return out

def priority_penalty(route, city_to_id, priorities, hospital):
    """Penalidade por atrasar entregas urgentes. Só consideramos as entregas (route)."""
    total = 0.0
    for i, city in enumerate(route):
        cid = city_to_id.get(city)
        if cid is None:
            continue
        prio = priorities.get(cid, 2)
        weight = (3 - prio) ** 2
        total += (i + 1) * weight
    return total

def fitness(route, city_to_id, priorities, hospital, w_dist=0.3, w_prio=0.7):
    d = total_distance_with_matrix(route, hospital, city_to_id, distance_matrix)
    p = priority_penalty(route, city_to_id, priorities, hospital)
    return w_dist * d + w_prio * p

def capacity_penalty(route, city_to_id, demands, capacity):
    total = sum(demands.get(city_to_id.get(c, -1), 0) for c in route)
    return max(0.0, total - capacity)

def fitness(route, city_to_id, priorities, demands, capacity, hospital,
            w_dist=0.3, w_prio=0.5, w_cap=0.2):
    d = total_distance_with_matrix(route, hospital, city_to_id, distance_matrix)
    p = priority_penalty(route, city_to_id, priorities, hospital)
    c = capacity_penalty(route, city_to_id, demands, capacity)
    print(f"Distância: {d:.2f}, Penalidade de prioridade: {p:.2f}, Penalidade de capacidade: {c:.2f}")
    return w_dist * d + w_prio * p + w_cap * c


if __name__ == "__main__":
    print("Cidades:", len(CITIES), "| População:", POPULATION_SIZE, "| Gerações:", N_GENERATIONS)

    population = [route_knn(CITIES, HOSPITAL)] + [random_route() for _ in range(POPULATION_SIZE - 1)]

    for gen in range(N_GENERATIONS):
        fitness_list = [fitness(r, city_to_id, PRIORITIES, DEMANDS, VEHICLE_CAPACITY, HOSPITAL) for r in population]       
        sorted_pairs = sorted(zip(population, fitness_list), key=lambda p: p[1])
        population = [p[0] for p in sorted_pairs]
        fitness_list = [p[1] for p in sorted_pairs]

        best_route, best_fit = population[0], fitness_list[0]
        if gen % 10 == 0:
            print(f"Geração {gen}: melhor distância = {best_fit:.2f}")

        new_pop = [population[0]]
        while len(new_pop) < POPULATION_SIZE:
            p1, p2 = random.choices(population[:TOP_FOR_SELECTION], k=2)
            child = order_crossover(p1, p2)
            child = mutate(child, MUTATION_PROB)
            new_pop.append(child)
        population = new_pop

    print("Final:", fitness(population[0], city_to_id, PRIORITIES, DEMANDS, VEHICLE_CAPACITY, HOSPITAL))
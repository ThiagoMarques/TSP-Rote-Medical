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

N_GENERATIONS = 50
MUTATION_PROB = 0.3
TOP_FOR_SELECTION = 10

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

if __name__ == "__main__":
    print("Cidades:", len(CITIES), "| População:", POPULATION_SIZE, "| Gerações:", N_GENERATIONS)

    population = [random_route() for _ in range(POPULATION_SIZE)]

    for gen in range(N_GENERATIONS):
        fitness_list = [total_distance(r, HOSPITAL) for r in population]
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

    print("Final:", total_distance(population[0], HOSPITAL))
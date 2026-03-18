import math


CITIES = [
    (512, 317),  # 0 - hospital
    (741, 72),   # 1
    (552, 50),   # 2
    (589, 131),  # 3
    (576, 216),  # 4
]

HOSPITAL = CITIES[0]

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

if __name__ == "__main__":
    print(f"Cidades: {CITIES}"  , end="\n\n")
    print(f"Hospital: {HOSPITAL}")

    #Teste para uma rota = ordem 1,2,3,4
    route = [CITIES[1], CITIES[2], CITIES[3], CITIES[4]]
    print(f"Roteiro: {route}")
    print(f"Distância total: {total_distance(route, HOSPITAL)}")

    #Teste para uma rota = ordem 1,3,2,4
    route = [CITIES[1], CITIES[3], CITIES[2], CITIES[4]]
    print(f"Roteiro: {route}")
    print(f"Distância total: {total_distance(route, HOSPITAL)}")

    #Teste para uma rota = ordem 1,4,2,3
    route = [CITIES[1], CITIES[4], CITIES[2], CITIES[3]]
    print(f"Roteiro: {route}")
    print(f"Distância total: {total_distance(route, HOSPITAL)}")
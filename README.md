# TSP Rote Medical

Projeto de otimização de rotas para entregas médicas usando o problema do caixeiro-viajante (TSP). O veículo parte do hospital, visita os pontos de entrega e retorna ao hospital, minimizando distância e respeitando prioridades e capacidade.

## O que faz

- **Cenário**: Um hospital (ponto 0) e vários pontos de entrega com coordenadas (x, y). Cada ponto tem prioridade (crítico, regular, insumo) e demanda; o veículo tem capacidade limitada.
- **Objetivo**: Encontrar uma ordem de visitas que minimize uma função de custo que combina:
  - Distância total (ida e volta ao hospital)
  - Penalidade por prioridade (entregas urgentes visitadas mais cedo)
  - Penalidade por capacidade (não exceder a carga do veículo)
- **Método**: Algoritmo genético com população inicial que inclui uma rota gerada por heurística KNN (vizinho mais próximo) e rotas aleatórias; crossover OX, mutação por troca de vizinhos e seleção pelos melhores.

## Requisitos

- Python 3.x (apenas biblioteca padrão: `math`, `random`).

## Como executar

```bash
cd TSP-Rote-Medical
python3 tsp.py
```

## Parâmetros (no código)

- `CITIES`: lista de coordenadas (x, y); o primeiro ponto é o hospital.
- `POPULATION_SIZE`: tamanho da população (ex.: 20).
- `N_GENERATIONS`: número de gerações (ex.: 50).
- `MUTATION_PROB`: probabilidade de mutação (ex.: 0.3).
- `TOP_FOR_SELECTION`: quantos melhores indivíduos podem ser escolhidos como pais (ex.: 10).
- `PRIORITIES`: prioridade por índice da cidade (0 = hospital; 1 = crítico, 2 = regular, 3 = insumo).
- `DEMANDS`: demanda por cidade; `VEHICLE_CAPACITY`: capacidade máxima do veículo.

## Estrutura do código

- `distance`, `build_distance_matrix`, `total_distance` / `total_distance_with_matrix`: cálculo de distâncias em linha reta e via matriz.
- `route_knn`: rota pelo vizinho mais próximo a partir do hospital.
- `random_route`: rota aleatória entre os pontos de entrega.
- `order_crossover` (OX): crossover de ordem entre duas rotas.
- `mutate`: mutação trocando dois pontos consecutivos da rota.
- `priority_penalty`, `capacity_penalty`: penalidades usadas na função de fitness.
- `fitness`: combina distância, penalidade de prioridade e de capacidade com pesos configuráveis.


from src.path import Path
from src.network import Network, PhysicalNetwork
from src.node import Node
import numpy as np


class Optimizer:
    def __init__(
        self,
        first_node_name: str,
        last_node_name: str,
        network: Network,
        population_size: int,
        crossover_probability: float,
        mutation_probability: float,
        generations: int = 100,
        random_seed: int = 0,
    ):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        self.network = network
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generations = generations
        self.random_seed = random_seed

    def nsga2(self):
        population = np.array(
            [
                Path(
                    self.first_node_name,
                    self.last_node_name,
                    self.network,
                    self.random_seed,
                )
                for _ in range(self.population_size)
            ]
        )
        for _ in range(self.generations):
            pass
            
        result = self.non_dominated_sorting_algorithm(population)
        self.crowding_algorithm(result[0])
        print(result[0][0].crowding_distance)
        print(result[0][1].crowding_distance)
        print(result[0][2].crowding_distance)
        print(result[0][3].crowding_distance)
        print(result[0][4].crowding_distance)
        print(result[0][5].crowding_distance)

    def crossover(self, path_one: Path, path_two: Path):
        nodes = [Node(name) for name in list(set(path_one.nodes) | set(path_two.nodes))]
        edges = list(set(path_one.edge_path) | set(path_two.edge_path))
        temp_network = PhysicalNetwork(nodes, edges)
        return Path(
            self.first_node_name, self.last_node_name, temp_network, self.random_seed
        )

    def mutation(self, path_one: Path):
        generated_path = Path(
            self.first_node_name, self.last_node_name, self.network, self.random_seed
        )
        return self.crossover(path_one, generated_path)

    def non_dominated_sorting_algorithm(self, population: np.ndarray) -> np.ndarray:
        domination_count = np.zeros(population.size)
        dominated_solutions = [[] for _ in range(population.size)]
        fronts = list()
        current_fronts = list()

        for i, first_individual in enumerate(population):
            for j, second_individual in enumerate(population[i + 1 :], start=i + 1):
                if first_individual > second_individual:
                    dominated_solutions[i].append(j)
                    domination_count[j] += 1
                elif second_individual > first_individual:
                    dominated_solutions[j].append(i)
                    domination_count[i] += 1
        for k, _ in enumerate(population):
            if domination_count[k] == 0:
                current_fronts.append(k)
        while len(current_fronts) > 0:
            fronts.append(current_fronts)
            next_front = list()
            for front_individual in current_fronts:
                for id in dominated_solutions[front_individual]:
                    domination_count[id] -= 1
                    if domination_count[id] == 0:
                        next_front.append(id)
            current_fronts = next_front
        result_fronts = [np.array([population[i] for i in front]) for front in fronts]
        return result_fronts

    def crowding_algorithm(self, front: list) -> None:
        for i, path in enumerate(front):
            path.front_index = i
            path.crowding_distance = 0
        for i in range(len(front[0].metrics)):
            sorted_front = sorted(front, key=lambda x: x.metrics[i])
            if i == 0:
                sorted_front = sorted_front[::-1]
            sorted_front[0].crowding_distance = float("inf")
            sorted_front[-1].crowding_distance = float("inf")
            difference = (
                abs(sorted_front[0].metrics[i] - sorted_front[-1].metrics[i]) + 1e-9
            )
            for j, path in enumerate(sorted_front[1:-1], start=1):
                distance = (
                    abs(sorted_front[j + 1].metrics[i] - sorted_front[j - 1].metrics[i])
                    / difference
                )
                path.crowding_distance += distance

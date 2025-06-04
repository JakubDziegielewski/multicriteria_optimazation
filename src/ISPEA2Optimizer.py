import numpy as np
from src.path import Path
from src.network import Network
from typing import Tuple

class ISPEA2Optimizer:
    def __init__(
        self,
        first_node_name: str,
        last_node_name: str,
        network: Network,
        population_size: int,
        crossover_probability: float,
        mutation_probability: float,
        generations: int = 100,
    ):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        self.network = network
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generations = generations

    def crossover(self, parent1: Path, parent2: Path):
        nodes = list(set(parent1.nodes + parent2.nodes))
        edges = list(set(parent1.edge_path + parent2.edge_path))
        subnetwork = Network(
            [node for node in self.network.nodes if node.name in nodes],
            [edge for edge in self.network.edges if edge in edges],
        )
        return Path(self.first_node_name, self.last_node_name, subnetwork)

    def mutation(self, path: Path):
        return Path(self.first_node_name, self.last_node_name, self.network)

    def dominates(self, a: Path, b: Path) -> bool:
        return a > b

    def calculate_fitness(self, population, archive):
        for path in population:
            strength = sum(1 for other in population if path > other)
            path.strength = strength

        for path in population:
            path.raw_fitness = sum(other.strength for other in population if other > path)

        for path in population:
            distances = [self.euclidean_distance(path.metrics, other.metrics) for other in population if other != path]
            if len(distances) >= 1:
                path.density = 1 / (np.partition(distances, 0)[0] + 2)
            else:
                path.density = 1  # lub np.inf, w zależności od logiki
            path.fitness = path.raw_fitness + path.density

    def euclidean_distance(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    def environmental_selection(self, combined, size):
        sorted_pop = sorted(combined, key=lambda x: x.fitness)
        return sorted_pop[:size]

    def tournament_selection(self, population):
        a, b = np.random.choice(population, 2, replace=False)
        return a if a.fitness < b.fitness else b

    def run(self):
        population = [Path(self.first_node_name, self.last_node_name, self.network) for _ in range(self.population_size)]
        archive = []

        for _ in range(self.generations):
            self.calculate_fitness(population, archive)
            mating_pool = [self.tournament_selection(population) for _ in range(self.population_size)]

            offspring = []
            for i in range(0, len(mating_pool), 2):
                p1, p2 = mating_pool[i], mating_pool[i+1]
                if np.random.random() < self.crossover_probability:
                    child1 = self.crossover(p1, p2)
                    child2 = self.crossover(p2, p1)
                else:
                    child1, child2 = p1, p2
                if np.random.random() < self.mutation_probability:
                    child1 = self.mutation(child1)
                if np.random.random() < self.mutation_probability:
                    child2 = self.mutation(child2)
                offspring.extend([child1, child2])

            combined = population + archive + offspring
            self.calculate_fitness(combined, archive)
            population = self.environmental_selection(combined, self.population_size)
            archive = self.environmental_selection(combined, self.population_size)

        return archive

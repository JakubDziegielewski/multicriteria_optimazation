import numpy as np
from src.path import Path
from src.network import Network
from typing import List, Optional

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

    def crossover(self, parent1: Path, parent2: Path) -> Path:
        nodes = list(set(parent1.nodes + parent2.nodes))
        edges = list(set(parent1.edge_path + parent2.edge_path))
        subnetwork = Network(
            [node for node in self.network.nodes if node.name in nodes],
            [edge for edge in self.network.edges if edge in edges],
        )
        return Path(self.first_node_name, self.last_node_name, subnetwork)

    def mutation(self, path: Path) -> Path:
        # Tu można dodać bardziej zaawansowaną mutację
        return Path(self.first_node_name, self.last_node_name, self.network)

    def dominates(self, a: Path, b: Path) -> bool:
        """a dominuje b jeśli jest lepszy we wszystkich celach i lepszy w co najmniej jednym"""
        better_or_equal = all(x <= y for x, y in zip(a.metrics, b.metrics))
        strictly_better = any(x < y for x, y in zip(a.metrics, b.metrics))
        return better_or_equal and strictly_better

    def calculate_fitness(self, population: List[Path], archive: Optional[List[Path]] = None):
        if archive is None:
            archive = []
        combined = population + archive

        # Strength obliczamy tylko dla populacji (lub combined)
        for p in combined:
            p.strength = sum(1 for q in combined if self.dominates(p, q))

        for p in combined:
            p.raw_fitness = sum(q.strength for q in combined if self.dominates(q, p))

        # Gęstość – odległość do k-tego sąsiada (k = sqrt(N))
        k = int(np.sqrt(len(combined)))
        for p in combined:
            distances = [self.euclidean_distance(p.metrics, q.metrics) for q in combined if q != p]
            distances.sort()
            sigma_k = distances[k] if k < len(distances) else distances[-1] if distances else 1e-9
            p.density = 1 / (sigma_k + 2)

        for p in combined:
            p.fitness = p.raw_fitness + p.density

    @staticmethod
    def euclidean_distance(a, b) -> float:
        return np.linalg.norm(np.array(a) - np.array(b))

    def environmental_selection(self, combined: List[Path], size: int) -> List[Path]:
        sorted_pop = sorted(combined, key=lambda x: x.fitness)
        selected = sorted_pop[:size]
        # Jeśli jest więcej niż size elementów na granicy, można dodać logikę gęstości, ale uprościmy
        return selected

    def tournament_selection(self, population: List[Path]) -> Path:
        if len(population) == 1:
            return population[0]
        a, b = np.random.choice(population, 2, replace=False)
        return a if a.fitness < b.fitness else b

    def run(self) -> List[Path]:
        population = [Path(self.first_node_name, self.last_node_name, self.network) for _ in range(self.population_size)]
        archive = []

        for _ in range(self.generations):
            self.calculate_fitness(population, archive)
            mating_pool = [self.tournament_selection(population) for _ in range(self.population_size)]

            offspring = []
            i = 0
            while i + 1 < len(mating_pool):
                p1, p2 = mating_pool[i], mating_pool[i + 1]
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
                i += 2

            if i < len(mating_pool):
                remaining = mating_pool[i]
                if np.random.random() < self.mutation_probability:
                    remaining = self.mutation(remaining)
                offspring.append(remaining)

            combined = population + archive + offspring
            self.calculate_fitness(combined, archive)
            population = self.environmental_selection(combined, self.population_size)
            archive = self.environmental_selection(combined, self.population_size)

        return archive

    def run_full_trace(self) -> List[List[Path]]:
        population = [Path(self.first_node_name, self.last_node_name, self.network) for _ in
                      range(self.population_size)]
        archive = []

        archive_history = []

        for _ in range(self.generations):
            self.calculate_fitness(population, archive)
            mating_pool = [self.tournament_selection(population) for _ in range(self.population_size)]

            offspring = []
            i = 0
            while i + 1 < len(mating_pool):
                p1, p2 = mating_pool[i], mating_pool[i + 1]
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
                i += 2

            if i < len(mating_pool):
                remaining = mating_pool[i]
                if np.random.random() < self.mutation_probability:
                    remaining = self.mutation(remaining)
                offspring.append(remaining)

            combined = population + archive + offspring
            self.calculate_fitness(combined, archive)
            population = self.environmental_selection(combined, self.population_size)
            archive = self.environmental_selection(combined, self.population_size)

            # Zapisz kopię archiwum po każdej generacji
            archive_history.append(archive.copy())

        return archive_history

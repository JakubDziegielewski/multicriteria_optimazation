import numpy as np
from src.path import Path
from src.network import Network, PhysicalNetwork
from src.node import Node
from typing import Tuple

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
    ):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        self.network = network
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generations = generations

    def crossover(self, parent1: Path, parent2: Path):
        nodes = [Node(name) for name in list(set(parent1.nodes) | set(parent2.nodes))]
        edges = list(set(parent1.edge_path) | set(parent2.edge_path))
        temp_network = PhysicalNetwork(nodes, edges)
        return Path(self.first_node_name, self.last_node_name, temp_network)

    def mutation(self, path: Path):
        return Path(self.first_node_name, self.last_node_name, self.network)

    def evolution_operations(self, ind1: Path, ind2: Path) -> Tuple[Path, Path]:
        if np.random.random() < self.crossover_probability:
            ind1 = self.crossover(ind1, ind2)
            ind2 = self.crossover(ind2, ind1)
        if np.random.random() < self.mutation_probability:
            ind1 = self.mutation(ind1)
        if np.random.random() < self.mutation_probability:
            ind2 = self.mutation(ind2)
        return ind1, ind2

    def nsga2(self):
        population = np.array([
            Path(self.first_node_name, self.last_node_name, self.network)
            for _ in range(self.population_size)
        ])

        fronts = self.non_dominated_sorting_algorithm(population)
        for front in fronts:
            self.crowding_algorithm(front)

        for _ in range(self.generations):
            mating_pool = self.tournament_selection_nsga2(population, self.population_size)
            offspring = []

            i = 0
            while i + 1 < len(mating_pool):
                ind1, ind2 = mating_pool[i], mating_pool[i + 1]
                child1, child2 = self.evolution_operations(ind1, ind2)
                offspring.extend([child1, child2])
                i += 2

            # jeśli nieparzysta liczba osobników – ostatni osobnik mutowany solo
            if i < len(mating_pool):
                offspring.append(self.mutation(mating_pool[i]))

            population = np.array(population.tolist() + offspring[:self.population_size], dtype=Path)
            fronts = self.non_dominated_sorting_algorithm(population)
            population = self.choose_next_population(fronts)

        fronts = self.non_dominated_sorting_algorithm(population)
        self.crowding_algorithm(fronts[0])
        return fronts[0]

    def non_dominated_sorting_algorithm(self, population: np.ndarray) -> list:
        fronts = []
        domination_count = np.zeros(population.size)
        dominated_solutions = [[] for _ in range(population.size)]

        for i, p in enumerate(population):
            for j, q in enumerate(population):
                if p > q:
                    dominated_solutions[i].append(j)
                elif q > p:
                    domination_count[i] += 1

        current_front = [i for i, count in enumerate(domination_count) if count == 0]
        for i in current_front:
            population[i].front_pareto = 0

        front_level = 0
        while current_front:
            next_front = []
            for i in current_front:
                for j in dominated_solutions[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)
                        population[j].front_pareto = front_level + 1
            fronts.append([population[i] for i in current_front])
            current_front = next_front
            front_level += 1

        return fronts

    def crowding_algorithm(self, front: list) -> None:
        for path in front:
            path.crowding_distance = 0

        for i in range(len(front[0].metrics)):
            front.sort(key=lambda x: x.metrics[i])
            front[0].crowding_distance = front[-1].crowding_distance = float("inf")
            min_val = front[0].metrics[i]
            max_val = front[-1].metrics[i]
            denom = max_val - min_val if max_val - min_val != 0 else 1e-9
            for j in range(1, len(front) - 1):
                front[j].crowding_distance += (
                    front[j + 1].metrics[i] - front[j - 1].metrics[i]
                ) / denom

    def choose_next_population(self, fronts: list) -> np.ndarray:
        next_population = []
        for front in fronts:
            if len(next_population) + len(front) <= self.population_size:
                self.crowding_algorithm(front)
                next_population.extend(front)
            else:
                self.crowding_algorithm(front)
                sorted_front = sorted(front, key=lambda x: x.crowding_distance, reverse=True)
                remaining = self.population_size - len(next_population)
                next_population.extend(sorted_front[:remaining])
                break
        return np.array(next_population, dtype=Path)

    def tournament_selection_nsga2(self, population: np.ndarray, population_size: int) -> np.ndarray:
        mating_pool = np.empty(population_size, dtype=Path)
        for i in range(population_size):
            a, b = np.random.choice(population, 2, replace=True)
            if a.front_pareto < b.front_pareto:
                winner = a
            elif a.front_pareto > b.front_pareto:
                winner = b
            elif a.crowding_distance > b.crowding_distance:
                winner = a
            else:
                winner = b
            mating_pool[i] = winner
        return mating_pool

    def nsga2_full_trace(self):
        population = np.array([
            Path(self.first_node_name, self.last_node_name, self.network)
            for _ in range(self.population_size)
        ])

        fronts = self.non_dominated_sorting_algorithm(population)
        for front in fronts:
            self.crowding_algorithm(front)

        fronts_history = []  # tutaj będziemy zbierać fronty po każdej generacji

        for _ in range(self.generations):
            mating_pool = self.tournament_selection_nsga2(population, self.population_size)
            offspring = []

            i = 0
            while i + 1 < len(mating_pool):
                ind1, ind2 = mating_pool[i], mating_pool[i + 1]
                child1, child2 = self.evolution_operations(ind1, ind2)
                offspring.extend([child1, child2])
                i += 2

            if i < len(mating_pool):
                offspring.append(self.mutation(mating_pool[i]))

            population = np.array(population.tolist() + offspring[:self.population_size], dtype=Path)
            fronts = self.non_dominated_sorting_algorithm(population)
            population = self.choose_next_population(fronts)

            # zapisz aktualny front najlepszych rozwiązań
            best_front = fronts[0]
            fronts_history.append(best_front)

        return fronts_history

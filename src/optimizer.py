from src.path import Path
from src.network import Network, PhysicalNetwork
from src.node import Node
import numpy as np
from typing import Tuple
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

    def crossover(self, path_one: Path, path_two: Path):
        nodes = [Node(name) for name in list(set(path_one.nodes) | set(path_two.nodes))]
        edges = list(set(path_one.edge_path) | set(path_two.edge_path))
        temp_network = PhysicalNetwork(nodes, edges)
        return Path(
            self.first_node_name, self.last_node_name, temp_network
        )

    def mutation(self, path_one: Path):
        generated_path = Path(
            self.first_node_name, self.last_node_name, self.network
        )
        return self.crossover(path_one, generated_path)

    def nsga2(self):
        population = np.array(
            [
                Path(
                    self.first_node_name,
                    self.last_node_name,
                    self.network
                )
                for _ in range(self.population_size)
            ]
        )

        fronts = self.non_dominated_sorting_algorithm(population)
        for front in fronts:
            self.crowding_algorithm(front)
        for generation in range(self.generations):
            mating_pool = self.tournament_selection(population, self.population_size)
            offspring = np.empty(self.population_size, dtype=Path)
            for i in range(0, len(mating_pool), 2):
                individual_one, individual_two = mating_pool[i], mating_pool[i + 1]
                offspring[i], offspring[i + 1] = self.evolution_operations(
                    individual_one, individual_two
                )
            resulting_population = np.concatenate((population, offspring))
            fronts = self.non_dominated_sorting_algorithm(resulting_population)
            population = self.choose_next_population(fronts)
        fronts = self.non_dominated_sorting_algorithm(population)
        self.crowding_algorithm(fronts[0])
        return fronts[0]

    def evolution_operations(
        self, individual_one: Path, individual_two: Path
    ) -> Tuple[Path, Path]:
        if np.random.random() < self.crossover_probability:
            cross_one, cross_two = self.crossover(
                individual_one, individual_two
            ), self.crossover(individual_one, individual_two)
            individual_one, individual_two = cross_one, cross_two
        if np.random.random() < self.mutation_probability:
            individual_one = self.mutation(individual_one)
        if np.random.random() < self.mutation_probability:
            individual_two = self.mutation(individual_two)
        return individual_one, individual_two

    def choose_next_population(self, fronts: list) -> np.ndarray:
        next_population = np.empty(self.population_size, dtype=Path)
        current_size = 0
        current_front = 0
        while current_size + len(fronts[current_front]) <= self.population_size:
            self.crowding_algorithm(fronts[current_front])
            next_population[
                current_size : current_size + len(fronts[current_front])
            ] = fronts[current_front]
            current_size += len(fronts[current_front])
            current_front += 1
        self.crowding_algorithm(fronts[current_front])
        sorted_front = sorted(
            fronts[current_front], key=lambda x: x.crowding_distance, reverse=True
        )
        next_population[current_size:] = sorted_front[
            : self.population_size - current_size
        ]
        return next_population
                offspring[i], offspring[i + 1] = self.evolution_operations(
                    individual_one, individual_two
                )
            resulting_population = np.concatenate((population, offspring))
            fronts = self.non_dominated_sorting_algorithm(resulting_population)
            population = self.choose_next_population(fronts)
        fronts = self.non_dominated_sorting_algorithm(population)
        self.crowding_algorithm(fronts[0])
        return fronts[0]

    def evolution_operations(
        self, individual_one: Path, individual_two: Path
    ) -> Tuple[Path, Path]:
        if np.random.random() < self.crossover_probability:
            cross_one, cross_two = self.crossover(
                individual_one, individual_two
            ), self.crossover(individual_one, individual_two)
            individual_one, individual_two = cross_one, cross_two
        if np.random.random() < self.mutation_probability:
            individual_one = self.mutation(individual_one)
        if np.random.random() < self.mutation_probability:
            individual_two = self.mutation(individual_two)
        return individual_one, individual_two

    def choose_next_population(self, fronts: list) -> np.ndarray:
        next_population = np.empty(self.population_size, dtype=Path)
        current_size = 0
        current_front = 0
        while current_size + len(fronts[current_front]) <= self.population_size:
            self.crowding_algorithm(fronts[current_front])
            next_population[
                current_size : current_size + len(fronts[current_front])
            ] = fronts[current_front]
            current_size += len(fronts[current_front])
            current_front += 1
        self.crowding_algorithm(fronts[current_front])
        sorted_front = sorted(
            fronts[current_front], key=lambda x: x.crowding_distance, reverse=True
        )
        next_population[current_size:] = sorted_front[
            : self.population_size - current_size
        ]
        return next_population

    def non_dominated_sorting_algorithm(self, population: np.ndarray) -> np.ndarray:
        fronts = list()

        domination_count, dominated_solutions = self.calculate_domination_metrics(
            population
        )

        domination_count, dominated_solutions = self.calculate_domination_metrics(
            population
        )
        current_level = 0
        current_fronts = self.find_front_zero(population, domination_count)
        current_fronts = self.find_front_zero(population, domination_count)

        while len(current_fronts) > 0:
            fronts.append(current_fronts)
            current_level += 1
            next_front = list()
            for front_individual in current_fronts:
                for id in dominated_solutions[front_individual]:
                    domination_count[id] -= 1
                    if domination_count[id] == 0:
                        next_front.append(id)
                        population[id].front_pareto = current_level
            current_fronts = next_front
        result_fronts = [np.array([population[i] for i in front]) for front in fronts]
        return result_fronts

    def find_front_zero(
        self, population: np.ndarray, domination_count: np.ndarray
    ) -> list:
        current_fronts = list()
        for k, path in enumerate(population):
            if domination_count[k] == 0:
                current_fronts.append(k)
                path.front_pareto = 0
        return current_fronts

    def calculate_domination_metrics(
        self, population: np.ndarray
    ) -> Tuple[np.ndarray, list]:
        domination_count = np.zeros(population.size)
        dominated_solutions = [[] for _ in range(population.size)]
        for i, first_individual in enumerate(population):
            for j, second_individual in enumerate(population[i + 1 :], start=i + 1):
                if first_individual > second_individual:
                    dominated_solutions[i].append(j)
                    domination_count[j] += 1
                elif second_individual > first_individual:
                    dominated_solutions[j].append(i)
                    domination_count[i] += 1
        return domination_count, dominated_solutions

    def find_front_zero(
        self, population: np.ndarray, domination_count: np.ndarray
    ) -> list:
        current_fronts = list()
        for k, path in enumerate(population):
            if domination_count[k] == 0:
                current_fronts.append(k)
                path.front_pareto = 0
        return current_fronts

    def calculate_domination_metrics(
        self, population: np.ndarray
    ) -> Tuple[np.ndarray, list]:
        domination_count = np.zeros(population.size)
        dominated_solutions = [[] for _ in range(population.size)]
        for i, first_individual in enumerate(population):
            for j, second_individual in enumerate(population[i + 1 :], start=i + 1):
                if first_individual > second_individual:
                    dominated_solutions[i].append(j)
                    domination_count[j] += 1
                elif second_individual > first_individual:
                    dominated_solutions[j].append(i)
                    domination_count[i] += 1
        return domination_count, dominated_solutions

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

    def tournament_selection(
        self, population: np.ndarray, population_size: int
    ) -> np.ndarray:
        mating_pool = np.empty(population_size, dtype=Path)
        for i in range(population_size):
            individuals = np.random.choice(population, 2, replace=True)
            if individuals[0].front_pareto < individuals[1].front_pareto:
                winner = individuals[0]
            elif individuals[0].front_pareto > individuals[1].front_pareto:
                winner = individuals[1]
            elif individuals[0].crowding_distance > individuals[1].crowding_distance:
                winner = individuals[0]
            else:
                winner = individuals[1]
            mating_pool[i] = winner
        return mating_pool

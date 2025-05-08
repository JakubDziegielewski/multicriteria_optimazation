from src.path import Path
from src.network import Network, PhysicalNetwork
from src.node import Node
import numpy as np

class Optimizer:
    def __init__(self, first_node_name: str, last_node_name: str, network: Network, population_size: int, crossover_probability: float, mutation_probability: float, generations: int = 100, random_seed:int=0):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        self.network = network
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generations = generations
        self.random_seed = random_seed
    
    def nsga2(self):
        population = np.array([Path(self.first_node_name, self.last_node_name, self.network, self.random_seed) for _ in range(self.population_size)])
        
        
    def crossover(self, path_one: Path, path_two: Path):
        nodes = [Node(name) for name in list(set(path_one.nodes) | set(path_two.nodes))]
        edges = list(set(path_one.edge_path) | set(path_two.edge_path))
        temp_network = PhysicalNetwork(nodes, edges)
        return Path(self.first_node_name, self.last_node_name, temp_network, self.random_seed)

    def mutation(self, path_one: Path):
        generated_path = Path(self.first_node_name, self.last_node_name, self.network, self.random_seed)
        return self.crossover(path_one, generated_path)
    
    def non_dominated_sorting_algorithm(self, population:np.ndarray) -> np.ndarray:
        domination_count = np.zeros(population.size)
        dominated_solutions = [[]] * population.size
        fronts = list()
        front_0 = list()
                    
        
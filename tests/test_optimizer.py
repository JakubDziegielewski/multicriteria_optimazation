import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from src.optimizer import Optimizer
from src.path import Path
from src.edge import PhysicalEdge
from src.network_creator import NetworkCreator


network_creator = NetworkCreator("network_source/test_network.txt")
network = network_creator.create_physical_network()
optimizer = Optimizer("Vancouver", "LasVegas", network, 2, 1, 1, generations=1)
possible_path_nodes = [["Vancouver", "LosAngeles", "LasVegas"], ["Vancouver", "SanFrancisco", "LasVegas"]]

population = np.array(
    [
        Path(
            optimizer.first_node_name,
            optimizer.last_node_name,
            optimizer.network
        )
        for _ in range(optimizer.population_size)
    ]
)
def test_crossover_returns_path():
    first_individual, second_individual = population[0], population[1]
    result = optimizer.crossover(first_individual, second_individual)
    assert result.nodes in possible_path_nodes





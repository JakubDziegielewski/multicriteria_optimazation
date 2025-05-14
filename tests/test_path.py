import pytest
import numpy as np
from src.optimizer import Optimizer
from src.path import Path
from src.edge import PhysicalEdge
from src.network_creator import NetworkCreator

network_creator = NetworkCreator("network_source/test_network.txt")
network = network_creator.create_physical_network()


edges_one = [network.edges[0], network.edges[3]]
edges_two = [network.edges[1], network.edges[5]]


def test_domination():
    edges_one[0].delay = 1
    edges_one[0].error_rate = 0.01
    edges_two[0].delay = 10
    edges_two[0].error_rate = 0.1
    edges_one[1].delay = 1
    edges_one[1].error_rate = 0.01
    edges_two[1].delay = 10
    edges_two[1].error_rate = 0.1
    path_one = Path("Vancouver", "LasVegas", network, edge_path=edges_one)
    path_two = Path("Vancouver", "LasVegas", network, edge_path=edges_two)
    assert path_one > path_two
    
    edges_two[0].delay = 1
    edges_two[0].error_rate = 0.01
    edges_two[1].delay = 1
    edges_two[1].error_rate = 0.01
    path_two = Path("Vancouver", "LasVegas", network, edge_path=edges_two)
    
    assert path_one > path_two
    
    edges_two[0].throughput = 2000
    edges_two[1].throughput = 2000
    path_two = Path("Vancouver", "LasVegas", network, edge_path=edges_two)
    assert not path_one > path_two
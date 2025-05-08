from src.network import Network, PhysicalNetwork
from src.node import PhysicalNode
from src.edge import PhysicalEdge
from numpy.random import random, randint, seed


class NetworkCreator:
    def __init__(self, file_path: str, random_seed = 0):
        self.file_path = file_path
        seed(random_seed)

    def create_network(self) -> Network:
        raise NotImplementedError

    def __read_physical_node__(self, node_string: str) -> PhysicalNode:
        splitted_string = node_string.strip().split(" ")
        return PhysicalNode(
            splitted_string[0], float(splitted_string[2]), float(splitted_string[3])
        )

    def __read_physical_edge__(self, edge_string: str) -> PhysicalEdge:
        splitted_string = edge_string.strip().split(" ")
        return PhysicalEdge(
            splitted_string[0],
            splitted_string[2],
            splitted_string[3],
            int(float(splitted_string[11])),
            randint(0, 10),
            round(random() / 10, 3),
        )

    def create_physical_network(self):
        with open(self.file_path) as f:
            lines = f.readlines()
        first_node_index = lines.index("NODES (\n") + 1
        last_node_index = lines.index(")\n", first_node_index)
        nodes = [
            self.__read_physical_node__(line)
            for line in lines[first_node_index:last_node_index]
        ]
        first_edge_index = lines.index("LINKS (\n", last_node_index) + 1
        last_edge_index = lines.index(")\n", first_edge_index)
        edges = [
            self.__read_physical_edge__(line)
            for line in lines[first_edge_index:last_edge_index]
        ]
        return PhysicalNetwork(nodes, edges)

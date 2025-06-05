from src.network import Network, PhysicalNetwork
from src.node import Node, PhysicalNode
from src.edge import PhysicalEdge
from typing import Tuple
from numpy.random import random, randint


class NetworkCreator:
    def __init__(self, file_path: str):
        self.file_path = file_path
    def create_network(self) -> Network:
        raise NotImplementedError

    def __read_physical_node__(self, node_string: str) -> PhysicalNode:
        splitted_string = node_string.strip().split(" ")
        return PhysicalNode(
            splitted_string[0], float(splitted_string[2]), float(splitted_string[3])
        )

    def __read_physical_edge__(self, edge_string: str, demands: dict) -> PhysicalEdge:
        splitted_string = edge_string.strip().split(" ")
        first_node = splitted_string[2]
        end_node = splitted_string[3]
        throughput = demands[first_node + end_node]
        return PhysicalEdge(
            splitted_string[0],
            first_node,
            end_node,
            throughput,
            randint(0, 10),
            round(random() / 10, 3),
        )

    def _read_demand(self, demand_string: str) -> Tuple[str, int]:
        splitted_string = demand_string.strip().split(" ")
        return splitted_string[2] + splitted_string[3], int(float(splitted_string[6])) * 2 #change units to Mbits/s
    
        

    def _read_demand(self, demand_string: str) -> Tuple[str, int]:
        splitted_string = demand_string.strip().split(" ")
        return splitted_string[2] + splitted_string[3], int(float(splitted_string[6])) * 2 #change units to Mbits/s
    
        
    def create_physical_network(self) -> Network:
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
        demands = {}
        first_demand_index = lines.index("DEMANDS (\n", last_edge_index) + 1
        last_demand_index = lines.index(")\n", first_demand_index)
        for line in lines[first_demand_index:last_demand_index]:
            demand = self._read_demand(line)
            demands[demand[0]] = demand[1]
        demands = {}
        first_demand_index = lines.index("DEMANDS (\n", last_edge_index) + 1
        last_demand_index = lines.index(")\n", first_demand_index)
        for line in lines[first_demand_index:last_demand_index]:
            demand = self._read_demand(line)
            demands[demand[0]] = demand[1]
        edges = [
            self.__read_physical_edge__(line, demands)
            for line in lines[first_edge_index:last_edge_index]
        ]
        return PhysicalNetwork(nodes, edges)

    def create_full_mesh_network(self, number_of_nodes: int) -> Network:
        nodes = [Node(str(id)) for id in range(number_of_nodes)]
        edges = []
        for first_node in range(number_of_nodes):
            for second_node in range(first_node + 1, number_of_nodes):
                first_id = str(first_node)
                second_id = str(second_node)
                edge_one = PhysicalEdge(f"L_{first_id}_{second_id}", first_id, second_id, randint(100, 1000), randint(0, 10), round(random() / 10, 3))
                edge_two = PhysicalEdge(f"L_{second_id}_{first_id}", second_id, first_id, randint(100, 1000), randint(0, 10), round(random() / 10, 3))
                edges.append(edge_one)
                edges.append(edge_two)
        return PhysicalNetwork(nodes, edges)
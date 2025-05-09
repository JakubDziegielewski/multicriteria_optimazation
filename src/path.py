from src.network import Network
from numpy.random import shuffle, seed


class Path:
    def __init__(
        self,
        first_node_name: str,
        last_node_name: str,
        network: Network,
        random_seed: int = 0,
    ):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        if last_node_name == first_node_name:
            raise ValueError("Starting Node and Destination Node are the same")
        self.edge_path = self.depth_first_search(
            network, first_node_name, last_node_name, random_seed=random_seed
        )
        self.throughput = min([edge.throughput for edge in self.edge_path])
        self.delay = sum([edge.delay for edge in self.edge_path])
        self.error_rate = round(sum([edge.error_rate for edge in self.edge_path]), 3)
        self.nodes = self.get_nodes_from_edges()
        self.metrics = [self.throughput, self.delay, self.error_rate]
        self.front_pareto = None
        self.front_index = None
        self.crowding_distance = None

    def depth_first_search(
        self,
        network: Network,
        first_node_name: str,
        last_node_name: str,
        random_seed: int = 0,
    ) -> list:
        next_node_name = first_node_name
        visited_nodes = [next_node_name]
        edge_queue = [[edge] for edge in network.edges_dict[next_node_name]]
        shuffle(edge_queue)
        seed(random_seed)
        while len(edge_queue) > 0:
            current_edges = edge_queue.pop(0)
            next_node_name = current_edges[-1].end_node_name
            if next_node_name == last_node_name:
                return current_edges
            new_edges = network.edges_dict[next_node_name]
            shuffle(new_edges)
            for edge in new_edges:
                if edge.end_node_name not in visited_nodes:
                    visited_nodes.append(next_node_name)
                    edge_queue.insert(0, current_edges + [edge])

    def get_nodes_from_edges(self) -> list:
        return [self.first_node_name] + [edge.end_node_name for edge in self.edge_path]

    def update_nodes(self) -> None:
        self.nodes = self.get_nodes_from_edges()

    def __gt__(self, other) -> bool:
        if self.throughput < other.throughput:
            return False
        if self.error_rate > other.error_rate:
            return False
        if self.delay > other.delay:
            return False
        return (
            self.throughput > other.throughput
            or self.error_rate < other.error_rate
            or self.delay < other.delay
        )

    def __eq__(self, other) -> bool:
        return self.nodes == other.nodes

    def __hash__(self):
        return hash(self.nodes)
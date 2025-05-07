from src.network import Network


class Path:
    def __init__(self, first_node_name: str, last_node_name: str, network: Network):
        self.first_node_name = first_node_name
        self.last_node_name = last_node_name
        if last_node_name == first_node_name:
            raise ValueError("Starting Node and Destination Node are the same")
        self.edge_path = self.depth_first_search(
            network, first_node_name, last_node_name
        )
        self.throughput = min([edge.throughput for edge in self.edge_path])
        self.delay = sum([edge.delay for edge in self.edge_path])
        self.error_rate = round(sum([edge.error_rate for edge in self.edge_path]), 3)
        self.nodes = [first_node_name] + [edge.end_node_name for edge in self.edge_path]

    def depth_first_search(
        self, network: Network, first_node_name: str, last_node_name: str
    ) -> None:
        next_node_name = first_node_name
        visited_nodes = [next_node_name]
        edge_queue = [[edge] for edge in network.edges_dict[next_node_name]]
        while len(edge_queue) > 0:
            current_edges = edge_queue.pop(0)
            next_node_name = current_edges[-1].end_node_name
            if next_node_name == last_node_name:
                return current_edges
            if next_node_name not in visited_nodes:
                visited_nodes.append(next_node_name)
                new_edges = network.edges_dict[next_node_name]
                for edge in new_edges:
                    edge_queue.append(current_edges + [edge])

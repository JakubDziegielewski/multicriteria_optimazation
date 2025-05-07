class Edge:
    def __init__(self, id:str, start_node_name: str, end_node_name: str):
        self.id = id
        self.start_node_name = start_node_name
        self.end_node_name = end_node_name
    def __repr__(self):
        return f"id: {self.id}, start node: {self.start_node_name}, end node: {self.end_node_name}"


class PhysicalEdge(Edge):
    def __init__(
        self,
        id: str,
        start_node_name: str,
        end_node_name: str,
        throughput: int,
        delay: int,
        error_rate: float,
    ):
        super().__init__(id, start_node_name, end_node_name)
        self.throughput = throughput
        self.delay = delay
        self.error_rate = error_rate
    def __repr__(self):
        return f"{super().__repr__()}, Throughput: {self.throughput}, Latency: {self.delay}, Error rate: {self.error_rate}"

from src.node import Node, PhysicalNode
from src.edge import Edge, PhysicalEdge


class Network:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges
        self.edges_dict = {node.name: [] for node in nodes}
        for edge in edges:
            self.edges_dict[edge.start_node_name].append(edge)

    def __repr__(self):
        return f"Nodes:\n{"\n".join([str(node) for node in self.nodes])}\n\nEdges:\n{"\n".join([str(edge) for edge in self.edges])}\n"


class PhysicalNetwork(Network):
    def __init__(self, nodes: list[PhysicalNode], edges: list[PhysicalEdge]):
        super().__init__(nodes, edges)

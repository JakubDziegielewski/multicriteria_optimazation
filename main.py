from src.network_creator import NetworkCreator
from src.path import Path

network_creator = NetworkCreator("network_source\janos-us-ca", random_seed=0)
network = network_creator.create_physical_network()

path = Path("Montreal", "LosAngeles", network)
for p in path.edge_path:
    print(p)
print(f"Throughput: {path.throughput}, Delay: {path.delay}, Error rate: {path.error_rate}")
print(path.nodes)
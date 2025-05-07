from src.network_creator import NetworkCreator
from src.path import Path
from numpy.random import seed

network_creator = NetworkCreator("network_source\janos-us-ca")
network = network_creator.create_physical_network()

path = Path("Vancouver", "Dallas", network)
for p in path.edge_path:
    print(p)
print(f"Throughput: {path.throughput}, Delay: {path.delay}, Error rate: {path.error_rate}")
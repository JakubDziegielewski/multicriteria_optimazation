from src.network_creator import NetworkCreator
from src.optimizer import Optimizer

network_creator = NetworkCreator("network_source/janos-us-ca", random_seed=0)
network = network_creator.create_physical_network()
optimizer = Optimizer("SaltLakeCity", "Miami", network, 10, 0.2, 0.2, generations=10)
fronts = optimizer.nsga2()
for front in fronts:
    print(len(front.nodes))
print(f"Size of front zero: {len(fronts)}")
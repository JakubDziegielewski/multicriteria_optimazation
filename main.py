from src.network_creator import NetworkCreator
from src.optimizer import Optimizer
import pandas as pd

network_creator = NetworkCreator("network_source/janos-us-ca", random_seed=0)
network = network_creator.create_physical_network()

optimizer = Optimizer("SaltLakeCity", "Miami", network, 10, 0.2, 0.3, generations=45)
fronts = optimizer.nsga2()
for path in fronts:
    print(len(path.nodes))

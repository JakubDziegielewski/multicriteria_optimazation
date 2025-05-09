from src.network_creator import NetworkCreator
from src.optimizer import Optimizer
import numpy as np

np.random.seed(0)
network_creator = NetworkCreator("network_source/janos-us-ca", random_seed=0)
network = network_creator.create_physical_network()
optimizer = Optimizer("SaltLakeCity", "Miami", network, 20, 0.1, 0.1, generations=20)
fronts = optimizer.nsga2()
for path in fronts:
    print(len(path.nodes))

from src.network_creator import NetworkCreator
from src.optimizer import Optimizer

network_creator = NetworkCreator("network_source/janos-us-ca", random_seed=0)
network = network_creator.create_physical_network()

optimizer = Optimizer("LosAngeles", "Winnipeg", network, 100, 0.01, 0.01)
optimizer.nsga2()
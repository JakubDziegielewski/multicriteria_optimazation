from src.network_creator import NetworkCreator
from src.optimizer import Optimizer
from src.ISPEA2Optimizer import ISPEA2Optimizer
from src.metrics import calculate_hypervolume

# -- Tworzenie sieci --
network_creator = NetworkCreator("network_source/janos-us-ca")
network = network_creator.create_physical_network()

# -- NSGA-II --
optimizer = Optimizer("Portland", "Miami", network, 10, 0.2, 0.3, generations=10)
front_nsga2 = optimizer.nsga2()

print("NSGA-II Front:")
for path in front_nsga2:
    print(f"Nodes: {len(path.nodes)}")

print(f"Size of NSGA-II front: {len(front_nsga2)}\n")

# -- ISPEA2 --
ispea2 = ISPEA2Optimizer("Portland", "Miami", network, 10, 0.2, 0.3, generations=10)
front_ispea2 = ispea2.run()

print("ISPEA2 Front:")
for path in front_ispea2:
    print(f"Nodes: {len(path.nodes)}")

print(f"Size of ISPEA2 front: {len(front_ispea2)}\n")

# -- Transformacja metryk: throughput → -throughput (dla minimalizacji)
def transform_metrics(front):
    for path in front:
        throughput, delay, error = path.metrics
        path.metrics = [-throughput, delay, error]
    return front

front_nsga2 = transform_metrics(front_nsga2)
front_ispea2 = transform_metrics(front_ispea2)

# -- Punkt referencyjny dla HV (większy niż najgorsze metryki)
reference_point = [0, 1000, 1.0]

# -- Obliczanie HV
hv_nsga2 = calculate_hypervolume(front_nsga2, reference_point)
hv_ispea2 = calculate_hypervolume(front_ispea2, reference_point)

# -- Wyniki
print(f"NSGA-II HV: {hv_nsga2:.4f}")
print(f"ISPEA2   HV: {hv_ispea2:.4f}")

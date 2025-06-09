import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from src.metrics import calculate_hypervolume
from src.optimizer import Optimizer
from src.ISPEA2Optimizer import ISPEA2Optimizer
from src.network_creator import NetworkCreator
import random


runs = 10
reference_point = [0, 1000, 1.0]

hv_nsga2_values = []
hv_ispea2_values = []


# network_creator = NetworkCreator("network_source/janos-us-ca")
full_mesh_network_creator = NetworkCreator()
# network = network_creator.create_physical_network()
network = full_mesh_network_creator.create_full_mesh_network(30)

for i in range(runs):
    print(f"Run {i + 1}/{runs}")
    seed = 42 + i
    random.seed(seed)
    np.random.seed(seed)

    # nsga2_opt = Optimizer("Portland", "Miami", network, 10, 0.2, 0.3, generations=10)
    nsga2_opt = Optimizer("1", "2", network, 10, 0.2, 0.3, generations=10)
    # ispea2_opt = ISPEA2Optimizer("Portland", "Miami", network, 10, 0.2, 0.3, generations=10)
    ispea2_opt = ISPEA2Optimizer("1", "2", network, 10, 0.2, 0.3, generations=10)

    front_nsga2 = nsga2_opt.nsga2()
    front_ispea2 = ispea2_opt.run()

    def transform(front):
        for ind in front:
            ind.metrics = [-ind.metrics[0], ind.metrics[1], ind.metrics[2]]
        return front

    front_nsga2 = transform(front_nsga2)
    front_ispea2 = transform(front_ispea2)

    hv_nsga2 = calculate_hypervolume(front_nsga2, reference_point)
    hv_ispea2 = calculate_hypervolume(front_ispea2, reference_point)

    hv_nsga2_values.append(hv_nsga2)
    hv_ispea2_values.append(hv_ispea2)


mean_nsga2 = np.mean(hv_nsga2_values)
std_nsga2 = np.std(hv_nsga2_values)
mean_ispea2 = np.mean(hv_ispea2_values)
std_ispea2 = np.std(hv_ispea2_values)

print(f"\nNSGA-II HV: mean = {mean_nsga2:.4f}, std = {std_nsga2:.4f}")
print(f"ISPEA2   HV: mean = {mean_ispea2:.4f}, std = {std_ispea2:.4f}")


plt.figure(figsize=(8, 5))
plt.bar(['NSGA-II', 'ISPEA2'], [mean_nsga2, mean_ispea2],
        yerr=[std_nsga2, std_ispea2], capsize=10, color=['#1f77b4', '#ff7f0e'])
plt.ylabel('Hypervolume (HV)')
plt.title(f'Porównanie Hypervolume ({runs} uruchomień)')
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("hv_comparison.png")
plt.show()

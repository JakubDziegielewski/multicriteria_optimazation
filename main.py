from src.network import PhysicalNetwork
from src.network_creator import NetworkCreator

network_creator = NetworkCreator("network_source\janos-us-ca")
network = network_creator.create_physical_network()


#print(network)
for k,v in network.edges_dict.items():
    print(k, v, "\n")
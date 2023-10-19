import networkx as nx
import numpy as np
import pandas as pd 
from itertools import combinations
import community

def KO_algorithm(graph):
    # Step 1: Community Detection
    partition = community.best_partition(graph)

    # Step 2: Community Boundary Identification
    boundary_nodes = set()
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        different_communities = set(partition[n] for n in neighbors if partition[n] != partition[node])
        if different_communities:
            boundary_nodes.add(node)

    # Step 3: Node Transfer
    updated_partition = partition.copy()
    for node in boundary_nodes:
        best_community = partition[node]  # Initially, the node's current community is considered the best
        best_modularity = community.modularity(partition, graph)  # Current modularity value

        for neighbor in graph.neighbors(node):
            transferred_partition = partition.copy()
            transferred_partition[node] = partition[neighbor]  # Transfer node to neighbor's community

            transferred_modularity = community.modularity(transferred_partition, graph)
            if transferred_modularity > best_modularity:
                best_modularity = transferred_modularity
                best_community = partition[neighbor]

        updated_partition[node] = best_community

    # Step 4: Modularity Evaluation
    final_modularity = community.modularity(updated_partition, graph)

    return updated_partition, final_modularity

# Example usage
# Assuming you have a membership_graph representing the network

# Create a NetworkX graph from the membership_graph
graph = nx.read_edgelist("../test_membership_graph.csv", delimiter=",")

# Apply the KO algorithm
updated_partition, final_modularity = KO_algorithm(graph)

# Print the final modularity value and the community assignments
print("Final Modularity:", final_modularity)
# print("Community Assignments:")
# for node, community_id in updated_partition.items():
#     print("Node:", node, "Community:", community_id)


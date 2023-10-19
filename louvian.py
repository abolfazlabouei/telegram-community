import pandas as pd
import networkx as nx
import community
from datetime import datetime

def detect_communities(G):
    """Detects communities in a graph using the Louvain algorithm and saves nodes in community dictionaries."""
    # Detect communities using Louvain algorithm
    start_time = datetime.now()
    partition = community.best_partition(G)
    end_time = datetime.now()
    runtime = (end_time - start_time).total_seconds()
    # Create an empty dictionary to store communities
    communities = {}

    # Iterate over nodes and their corresponding communities
    for node, community_id in partition.items():
        # Add the node to the community dictionary
        if community_id not in communities:
            communities[community_id] = [node]
        else:
            communities[community_id].append(node)

    # Print nodes in each community
    # for community_id, nodes in communities.items():
    #     print("Community:", community_id, "Nodes:", nodes)

    # Calculate modularity
    modularity = community.modularity(partition, G)
    print("Modularity:", modularity)
    nx.set_node_attributes(G, partition, 'community')
    with open('node_community_Louvain.txt', 'w') as f:
        for node in G.nodes():
            f.write(f'{node} {G.nodes[node]["community"]}\n')
            
    # Print runtime
    print("Runtime: {:.2f} seconds".format(runtime))
    return communities

if __name__ == '__main__':
    # Load the dataset into a pandas dataframe
    G = nx.read_edgelist("test_membership_graph.csv", delimiter=",")

    # Detect communities in the graph and save nodes in community dictionaries
    communities = detect_communities(G)

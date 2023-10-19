import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from datetime import datetime

def detect_communities(G):
    """Detects communities in a graph using the Girvan-Newman algorithm and saves nodes in community dictionaries."""
    # Detect communities using Girvan-Newman algorithm
    start_time = datetime.now()
    communities_generator = nx.algorithms.community.girvan_newman(G)
    partition = tuple(sorted(c) for c in next(communities_generator))
    end_time = datetime.now()
    runtime = (end_time - start_time).total_seconds()

    # Convert the partition to a dictionary format
    partition_dict = {}
    for idx, comm in enumerate(partition):
        for node in comm:
            partition_dict[node] = idx

    # Calculate modularity
    modularity = community_louvain.modularity(partition_dict, G)

    # Plot modularity
    modularity_data = {
        'Girvan-Newman': modularity
    }
    plt.bar(modularity_data.keys(), modularity_data.values())
    plt.xlabel('Algorithm')
    plt.ylabel('Modularity')
    plt.title('Modularity Comparison')
    plt.savefig('modularity_plot.png')
    plt.show()

    # Print runtime
    print("Runtime: {:.2f} seconds".format(runtime))

    # Save the partition as node attributes
    nx.set_node_attributes(G, partition_dict, 'community')

    # Visualize the graph with community colors
    pos = nx.spring_layout(G)
    node_colors = [partition_dict[node] for node in G.nodes()]
    nx.draw_networkx(G, pos=pos, node_color=node_colors, cmap='tab10')
    plt.title('Community Detection with Girvan-Newman Algorithm')
    plt.savefig('community_visualization.png')
    plt.show()

if __name__ == '__main__':
    # Load the membership network from the CSV file
    G = nx.read_edgelist('membership_graph.csv', delimiter=',')

    # Detect communities in the graph and save nodes in community dictionaries
    detect_communities(G)
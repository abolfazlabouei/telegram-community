import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from datetime import datetime

def detect_communities(G):
    """Detects communities in a graph using the Leiden algorithm and saves nodes in community dictionaries."""
    # Detect communities using Leiden algorithm
    start_time = datetime.now()
    partition = community_louvain.best_partition(G, resolution=1.0, random_state=42)
    end_time = datetime.now()
    runtime = (end_time - start_time).total_seconds()

    # Calculate modularity
    modularity = community_louvain.modularity(partition, G)
    print(modularity)
    # Plot modularity
    # modularity_data = {
    #     'Leiden': modularity
    # }
    # plt.bar(modularity_data.keys(), modularity_data.values())
    # plt.xlabel('Algorithm')
    # plt.ylabel('Modularity')
    # plt.title('Modularity Comparison')
    # plt.savefig('modularity_plot.png')
    # plt.show()

    # Print runtime
    print("Runtime: {:.2f} seconds".format(runtime))

    # Save the partition as node attributes
    nx.set_node_attributes(G, partition, 'community')
    with open('node_community_Leiden.txt', 'w') as f:
        for node in G.nodes():
            f.write(f'{node} {G.nodes[node]["community"]}\n')

    # # Visualize the graph with community colors
    # pos = nx.spring_layout(G)
    # node_colors = [partition[node] for node in G.nodes()]
    # nx.draw_networkx(G, pos=pos, node_color=node_colors, cmap='tab10')
    # plt.title('Community Detection with Leiden Algorithm')
    # plt.savefig('community_visualization.png')
    # plt.show()


if __name__ == '__main__':
    # Load the membership network from the CSV file
    G = nx.read_edgelist('membership_graph.csv', delimiter=',')

    # Detect communities in the graph and save nodes in community dictionaries
    detect_communities(G)
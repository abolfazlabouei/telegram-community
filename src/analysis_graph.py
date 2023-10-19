# import networkx as nx
# import matplotlib.pyplot as plt

# def analyze_graph(G):
#     """Analyzes a graph and prints its properties."""
#     # Number of nodes
#     num_nodes = G.number_of_nodes()
#     num_edges = G.number_of_edges()
#     print("Number of nodes:", num_nodes)
#     print("Number of edges:", num_edges)

#     # Cluster coefficient
#     cluster_coefficient = nx.average_clustering(G)
#     print("Cluster coefficient:", cluster_coefficient)

#     # Average degree
#     avg_degree = sum(dict(G.degree()).values()) / num_nodes
#     print("Average degree:", avg_degree)

#     # Get the top 10 degree nodes
#     # top_10_degree_nodes = sorted(dict(G.degree()).items(), key=lambda x: x[1], reverse=True)[:10]
#     # print("Top 10 Degree Nodes:", top_10_degree_nodes)

#     # Degree distribution
#     degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
#     degree_count = nx.degree_histogram(G)
#     plt.bar(range(len(degree_count)), degree_count, width=0.8, color='b')
#     plt.xlabel("Degree")
#     plt.ylabel("Count")
#     plt.title("Degree Distribution")
#     plt.show()

# if __name__ == '__main__':
#     # Load the membership network from the CSV file
#     G = nx.read_edgelist('membership_graph.csv', delimiter=',')

#     # Analyze the graph and print its properties
#     analyze_graph(G)

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def analyze_graph(G):
    """Analyzes a graph and prints its properties."""
    # Number of nodes and edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print("Number of nodes:", num_nodes)
    print("Number of edges:", num_edges)

    # Cluster coefficient
    # cluster_coefficient = nx.average_clustering(G)
    # print("Cluster coefficient:", cluster_coefficient)

    # Degree distribution
    degree_sequence = np.array([d for n, d in G.degree()])
    degree_count = np.bincount(degree_sequence)
    degrees = np.arange(len(degree_count))
    plt.bar(degrees, degree_count, width=0.8, color='b')
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.title("Degree Distribution")
    
    # Save the degree distribution plot as an image file
    plt.savefig("degree_distribution.png")
    
    # plt.show()

if __name__ == '__main__':
    # Load the membership network from the CSV file
    G = nx.read_edgelist('../test_membership_graph.csv', delimiter=',')
    
    # Analyze the graph and print its properties
    analyze_graph(G)
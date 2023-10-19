import numpy as np
import networkx as nx
from collections import defaultdict


def modularity_matrix(adj_matrix):
    k = adj_matrix.sum(axis=1)
    m = k.sum()
    B = adj_matrix - np.outer(k, k) / m
    return B


def modularity(communities, adj_matrix):
    m = adj_matrix.sum()
    Q = 0
    for i in range(len(communities)):
        Ki = adj_matrix[i].sum()
        for j in range(len(communities)):
            Kj = adj_matrix[j].sum()
            Aij = adj_matrix[i][j]
            if i == j:
                Q += (Aij - Ki * Kj / m) / m
            else:
                Q += Aij / m - Ki * Kj / (2 * m) ** 2
    return Q


def get_neighbors(node, adj_matrix):
    return np.where(adj_matrix[node])[0]


def agglomerate_nodes(nodes, adj_matrix):
    neighbors = set(np.concatenate([get_neighbors(node, adj_matrix) for node in nodes]))
    communities = []
    while nodes:
        node = nodes.pop()
        comm = {node}
        while True:
            improved = False
            for neighbor in get_neighbors(node, adj_matrix):
                if neighbor in comm:
                    continue
                new_comm = comm | {neighbor}
                q = modularity([new_comm] + [c for c in communities if c != comm], adj_matrix)
                if q > modularity([comm] + [c for c in communities if c != comm], adj_matrix):
                    comm = new_comm
                    improved = True
                    break
            if not improved:
                break
        communities.append(comm)
        nodes -= comm
    return communities, neighbors


def agglomerate_communities(communities, adj_matrix):
    n = len(adj_matrix)
    node_to_comm = np.zeros(n, dtype=np.int)
    comm_to_nodes = defaultdict(set)
    for i, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = i
            comm_to_nodes[i].add(node)
    new_adj_matrix = np.zeros((len(communities), len(communities)))
    for i, nodes in comm_to_nodes.items():
        for j, neighbors in enumerate(agglomerate_nodes(nodes, adj_matrix)[1]):
            if i == j:
                new_adj_matrix[i][i] = adj_matrix[list(nodes)][:, list(nodes)].sum()
            else:
                new_adj_matrix[i][j] = adj_matrix[list(nodes)][:, list(neighbors)].sum()
    return node_to_comm, new_adj_matrix


def louvain_method(G, n=None):
    adj_matrix = nx.adjacency_matrix(G).toarray()
    node_to_comm = np.arange(len(adj_matrix))
    while True:
        communities, neighbors = agglomerate_nodes(set(np.arange(len(adj_matrix))), adj_matrix)
        if len(communities) == len(set(node_to_comm)):
            break
        node_to_comm, adj_matrix = agglomerate_communities(communities, adj_matrix)
    true_partition = [{i} for i in range(len(adj_matrix))]
    true_comms = {c: c for c in node_to_comm}
    return true_partition

G = nx.read_edgelist("membership_graph.csv", delimiter=",")
# Run the Louvain algorithm
partition = louvain_method(G)
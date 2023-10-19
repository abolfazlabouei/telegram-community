import pandas as pd
import networkx as nx
import community

# Load the membership graph from the CSV file
G = nx.read_edgelist('membership_graph.csv', delimiter=',')

# Detect communities using a community detection algorithm (e.g., Leiden algorithm)
def detect_communities(G):
    partition = community.best_partition(G)

    # Create a dictionary to store community labels for nodes
    node_communities = {}

    # Iterate over nodes and their corresponding communities
    for node, community_id in partition.items():
        # Assign the community label to the node
        node_communities[node] = community_id

    return node_communities

# Generate recommendations based on community and network topology
def generate_recommendations(user):
    # Detect communities in the membership graph
    communities = detect_communities(G)

    # Find the community of the user
    user_community = communities[user]

    # Get the members of the user's community
    community_members = [node for node, community in communities.items() if community == user_community]

    # Calculate the number of common groups between the user and each community member
    common_groups = {}
    for member in community_members:
        common_groups[member] = len(set(G.neighbors(user)) & set(G.neighbors(member)))

    # Sort the community members based on the number of common groups in descending order
    sorted_members = sorted(common_groups, key=common_groups.get, reverse=True)

    # Generate recommendations by selecting items/groups from the top community members
    recommendations = []
    for member in sorted_members:
        member_groups = set(G.neighbors(member))
        user_groups = set(G.neighbors(user))
        recommendations.extend(member_groups - user_groups)

    return recommendations

# Example usage
user = '463203851'
recommendations = generate_recommendations(user)
print("Recommendations for", user, ":", recommendations)
import pandas as pd
import networkx as nx

class TelegramMembershipGraph:
    def __init__(self, data):
        self.data = data
        self.G = nx.Graph()

    def _add_users(self, users):
        # Add nodes for each user
        self.G.add_nodes_from(users)

    def _add_edges(self, members):
        # Add edges between users that share a common group
        count = 0
        for group in set([d['group_id'] for d in members]):
            group_members = [d for d in members if d['group_id'] == group]
            for i, user1 in enumerate(group_members):
                for user2 in group_members[i+1:]:
                    self.G.add_edge(user1['user_id'], user2['user_id'], group_id=group)
                    count += 1
                    if count % 100000 == 0:
                        print(f"Processed {count} edges...")

    def build_graph(self, num_rows):
        # Use the first 'num_rows' from the data
        data = self.data[:num_rows]

        # Get a set of unique users and members
        users = set([d['user_id'] for d in data])
        members = data

        self._add_users(users)
        self._add_edges(members)

    def save_edges(self, filename):
        # Save edges as CSV file
        df_edges = pd.DataFrame(self.G.edges(data=True), columns=['source', 'target', 'group_id'])
        df_edges.to_csv(filename, index=False, header=True)

if __name__ == '__main__':
    # Load the dataset into a pandas dataframe
    df = pd.read_csv('subtacts.csv')
    df.columns = ['user_id', 'group_id', 'post']

    df.to_csv('modified_dataset.csv', index=False)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict('records')

    # Create a membership graph object
    graph = TelegramMembershipGraph(data)

    # Build the graph using the first 1000 rows and save the edges to a file
    graph.build_graph(10000)
    graph.save_edges('test_membership_graph.csv')





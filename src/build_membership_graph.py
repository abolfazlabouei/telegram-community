import pandas as pd
import networkx as nx

class TelegramMembershipGraph:
    def __init__(self, data):
        self.data = data
        self.G = nx.Graph()

    def _add_users(self):
        # Add nodes for each user
        users = set([d['user_id'] for d in self.data])
        self.G.add_nodes_from(users)

    def _add_edges(self):
        # Add edges between users that share a common group
        count = 0
        for group in set([d['group_id'] for d in self.data]):
            members = [d['user_id'] for d in self.data if d['group_id'] == group]
            for i, user1 in enumerate(members):
                for user2 in members[i+1:]:
                    self.G.add_edge(user1, user2)
                    count += 1
                    if count % 1000 == 0:
                        print(f"Processed {count} edges...")

    def build_graph(self):
        self._add_users()
        self._add_edges()

    def save_edges(self, filename):
        # Save edges as CSV file
        df_edges = pd.DataFrame(self.G.edges(), columns=['source', 'target'])
        df_edges.to_csv(filename, index=False, header=True)

if __name__ == '__main__':
    # Load the dataset into a pandas dataframe
    df = pd.read_csv('subtacts.csv', nrows=1000)
    df.columns = ['user_id', 'group_id', "post"]

    df.to_csv('modified_dataset.csv', index=False)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict('records')

    # Create a membership graph object
    graph = TelegramMembershipGraph(data)

    # Build the graph and save the edges to a file
    graph.build_graph()
    graph.save_edges('test_membership_graph.csv')
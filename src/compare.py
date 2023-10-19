import matplotlib.pyplot as plt

def plot_modularity_comparison(louvain_modularity, leiden_modularity):
    algorithms = ['Louvain', 'Leiden']
    modularity_values = [louvain_modularity, leiden_modularity]

    # Set the figure size
    plt.figure(figsize=(6,4))

    # Adjust the width of the bars
    bar_width = 0.5

    plt.bar(algorithms, modularity_values, color='b', width=bar_width)
    plt.xlabel('Algorithm')
    plt.ylabel('Runtime')
    # plt.title('Louvain vs. Leiden Runtime Comparison')

    # Save the plot as an image file
    plt.savefig('modularity_comparison.png', bbox_inches='tight')

    plt.show()

# Example usage
louvain_runtime = 1051.31
leiden_runtime = 483.79 

plot_modularity_comparison(louvain_runtime, leiden_runtime)
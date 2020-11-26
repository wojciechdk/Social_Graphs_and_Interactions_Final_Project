import matplotlib.pyplot as plt
import networkx as nx
import wojciech as w


def plot_distribution_of_attribute(G: nx.Graph,
                                   instance,
                                   instance_label,
                                   attribute_name):
    if instance == 'node':
        attribute_values = G.nodes[instance_label][attribute_name]
    elif instance == 'edge':
        attribute_values = G.edges[instance_label][attribute_name]
    else:
        raise ValueError(f'Invalid instance "{instance}"')

    figure, axes = w.empty_figure()
    axes.hist(attribute_values, bins=100)
    axes.set_title(f'Distribution of attribute: "{attribute_name}" for '
                   f'{instance}: "{instance_label}"',
                   fontdict={'size': 18})
    axes.set_xlabel(attribute_name.capitalize(), fontdict={'size': 14})
    axes.set_ylabel('Count', fontdict={'size': 14})

    axes.spines['top'].set_color('white')
    axes.spines['right'].set_color('white')
    axes.set_facecolor("white")

    plt.show()

    return axes
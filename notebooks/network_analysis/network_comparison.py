import json
import library_functions as lf
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import powerlaw
import wojciech as w

from config import Config
from fa2 import ForceAtlas2
from operator import itemgetter
from pandas_profiling import ProfileReport
from pathlib import Path

# %% Create graphs
g_wiki = lf.create_graph_wiki()
g_reddit = lf.create_graph_reddit()

#%%
# reddit_data = lf.load_data_reddit()
#
# max_matches = 0
# label_max = ''
# for post_label, post in reddit_data.items():
#     if len(post['matches']) > max_matches:
#         max_matches = len(post['matches'])
#         label_max = post_label
#
# post_with_most_matches = reddit_data[label_max]


# %% Plot degree distribution summary
graphs_to_show = [g_reddit, g_wiki, w.graph.erdos_renyi_like(g_reddit)]
graph_names = ['Reddit', 'Wiki', 'Random like Reddit']
graph_colors = ['red', 'blue', 'green']

w.graph.plot_degree_distribution_summary(graphs_to_show,
                                         graph_names=graph_names,
                                         graph_colors=graph_colors,
                                         x_lim_lin=(-2, 100),
                                         x_lim_log=(0.9, 1000)
                                         )

# %% Most central nodes Wiki
for centrality in ['degree', 'in-degree', 'out-degree', 'betweenness',
                   'eigenvector']:
    w.graph.most_central_nodes(g_wiki, centrality, n=10, printout=True)

# %% Most central nodes Reddit
for centrality in ['degree', 'betweenness', 'eigenvector']:
    w.graph.most_central_nodes(g_reddit, centrality, n=10, printout=True)

# %% In vs out degree Wiki
w.graph.plot_in_vs_out_degree(g_wiki,
                              plot_type='heatmap',
                              colormap_norm='log')
plt.show()

# %% Force Atlas plot Wiki
# w.graph.plot_force_atlas_2(w.graph.remove_isolates(g_wiki),
#                            node_size='by degree',
#                            node_color=np.array([[0, 0, 1, 0.5]]),
#                            edge_color=np.array([[0, 0, 0, 0.1]]),
#                            alpha=None,
#                            iterations=100,
#                            outboundAttractionDistribution=True)
# plt.show()

# %% Find most often occurring edges
# edges_count = nx.get_edge_attributes(g_wiki, "count")
# edges_count_sorted = sorted(edges_count.items(),
#                             key=itemgetter(1),
#                             reverse=True)


# %% Create alternative reddit graphs
# Positive
g_reddit_positive = g_reddit.copy()
conditions_not_positive = {'polarity': lambda x: np.median(x) < 0.2}
edges_not_positive = w.graph.get_edges_by_attribute(g_reddit_positive,
                                                    conditions_not_positive)
g_reddit_positive.remove_edges_from(edges_not_positive)

# Negative
g_reddit_negative = g_reddit.copy()
conditions_not_negative = {'polarity': lambda x: np.median(x) > -0.2}
edges_not_negative = w.graph.get_edges_by_attribute(g_reddit_negative,
                                                    conditions_not_negative)
g_reddit_negative.remove_edges_from(edges_not_negative)

# %% Plot distribution of attributes
figure = plt.figure(figsize=(12, 8))
axes = figure.gca()

w.graph.plot_distribution(
    g_reddit,
    quantity='attribute',
    attribute_object='edge',
    attribute_name='polarity',
    attribute_function=np.median,
    attribute_function_name='median',
    plot_type='bar',
    axes=axes,
    bins=100
)

plt.show()

# %% Degree distribution of Reddit plots
graphs_to_show = [g_reddit, g_reddit_positive, g_reddit_negative]
graph_names = ['Reddit', 'Reddit positive', 'Reddit negative']
graph_colors = ['red', 'green', 'blue']

w.graph.plot_degree_distribution_summary(graphs_to_show,
                                         graph_names=graph_names,
                                         graph_colors=graph_colors,
                                         x_lim_lin=(-2, 100),
                                         x_lim_log=(0.9, 1000)
                                         )


# %% Degree stats
graphs = [g_reddit, g_reddit_positive, g_reddit_negative]
graph_names = ['Reddit', 'Reddit Positive', 'Reddit Negative']

degree_stats = dict()
for graph, graph_name in zip(graphs, graph_names):
    print(f'\n{graph_name}:')
    degree_stats[graph_name] = w.graph.degree_statistics(graph, printout=True)

# %% Most central nodes in different Reddit Graphs
graphs = [g_reddit, g_reddit_positive, g_reddit_negative]
graph_names = ['Reddit', 'Reddit Positive', 'Reddit Negative']
centralities = ['degree']

for graph, graph_name in zip(graphs, graph_names):
    print(f'\n{graph_name}:')
    for centrality in centralities:
        w.graph.most_central_nodes(graph, centrality, n=10, printout=True)

# %% Save graphs to pickle
nx.readwrite.gpickle.write_gpickle(g_reddit, Config.Path.reddit_graph)
nx.readwrite.gpickle.write_gpickle(g_wiki, Config.Path.wiki_digraph)
# %% Let's look at the GCC's and undirected graphs for the following.

gcc_wiki_dir = w.graph.largest_connected_component(g_wiki)
gcc_reddit = w.graph.largest_connected_component(g_reddit)

# %%
gcc_wiki = gcc_wiki_dir.to_undirected()

nx.readwrite.gpickle.write_gpickle(gcc_reddit, Config.Path.reddit_gcc)
nx.readwrite.gpickle.write_gpickle(gcc_wiki, Config.Path.wiki_gcc)

# %%

import json
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import powerlaw
import wojciech as w

from fa2 import ForceAtlas2
from operator import itemgetter
from pandas_profiling import ProfileReport
from pathlib import Path
from library_functions.create_graph_reddit import create_graph_reddit
from library_functions.create_graph_wiki import create_graph_wiki
from library_functions.load_data_reddit import load_data_reddit
from library_functions.load_data_wiki import load_data_wiki
from library_functions.load_substance_names import load_substance_names
from library_functions.save_synonym_mapping import save_synonym_mapping
import library_functions.plotly_draw
from config import Config

#%% Load substance names
substance_names = load_substance_names()

#%% Load data
wiki_data = load_data_wiki()
drug_database_reddit = load_data_reddit()

# %% Synonym Mapping
save_synonym_mapping(wiki_data)

# %% Create graphs
g_wiki = create_graph_wiki(wiki_data, substance_names)
g_reddit = create_graph_reddit(drug_database_reddit, wiki_data,
                               substance_names)

#%% Plot degree distribution
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

#%% Most central nodes Reddit
for centrality in ['degree', 'betweenness', 'eigenvector']:
    w.graph.most_central_nodes(g_reddit, centrality, n=10, printout=True)


# %% In vs out degree Wiki
w.graph.plot_in_vs_out_degree(g_wiki,
                              plot_type='scatter')
plt.show()

#%% Force Atlas plot Wiki
# w.graph.plot_force_atlas_2(w.graph.remove_isolates(g_wiki),
#                            node_size='by degree',
#                            node_color=np.array([[0, 0, 1, 0.5]]),
#                            edge_color=np.array([[0, 0, 0, 0.1]]),
#                            alpha=None,
#                            iterations=100,
#                            outboundAttractionDistribution=True)
# plt.show()

#%% Find most often occurring edges
# edges_count = nx.get_edge_attributes(g_wiki, "count")
# edges_count_sorted = sorted(edges_count.items(),
#                             key=itemgetter(1),
#                             reverse=True)


# %%

# Save graphs to pickle

nx.readwrite.gpickle.write_gpickle(g_reddit, Config.Path.reddit_graph)
nx.readwrite.gpickle.write_gpickle(g_wiki, Config.Path.wiki_digraph)
# %%

# Let's look at the GCC's and undirected graphs for the following.

gcc_wiki_dir = w.graph.largest_connected_component(g_wiki)
gcc_reddit = w.graph.largest_connected_component(g_reddit)
# %%

gcc_wiki = gcc_wiki_dir.to_undirected()


nx.readwrite.gpickle.write_gpickle(gcc_reddit, Config.Path.reddit_gcc)
nx.readwrite.gpickle.write_gpickle(gcc_wiki, Config.Path.wiki_gcc)
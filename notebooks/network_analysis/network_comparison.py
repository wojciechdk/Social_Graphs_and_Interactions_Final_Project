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

#%% Plot Degree Distribution Wiki
w.graph.plot_degree_distribution_summary(g_wiki,
                                         title='Wikipedia',
                                         title_y_position=0.985,
                                         x_lim_lin=(-2, 200))

#%% Plot Degree Distribution Reddit
w.graph.plot_degree_distribution_summary(g_reddit,
                                         title='Reddit',
                                         x_lim_lin=(-2, 200))

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

#%% Compare degree dist
Gs = [g_wiki, g_reddit]
G_names = ['Wikipedia', 'Reddit']
G_colors = ['Blue', 'Red']
direction = None

figure, axes_all = plt.subplots(1, 2,
                                sharex='col', sharey='col',
                                figsize=(12, 5))

# Initialize min and max founders
max_y_data = 0
max_y_data_without_0_degree = 0
min_y_data_without_0_degree = 1


def format_axes(axes):
    axes.spines['top'].set_color('white')
    axes.spines['right'].set_color('white')
    axes.xaxis.grid(which="both", linewidth=0.5)
    axes.yaxis.grid(which="both", linewidth=0.5)
    axes.xaxis.label.set_fontsize(12)
    axes.yaxis.label.set_fontsize(12)
    axes.title.set_fontsize(14)


# Lin-lin axes
axes = axes_all[0]
for G, G_name, G_color in zip(Gs, G_names, G_colors):
    _, (degrees, distribution) = w.graph.plot_degree_distribution(
        G,
        direction=direction,
        axis_scaling='lin-lin',
        plot_type='scatter',
        as_probability_distribution=True,
        color=G_color,
        marker_size=40,
        label=G_name,
        axes=axes,
        annotate=['x_label', 'y_label']
    )

    format_axes(axes)

    max_y_data = np.max((np.max(distribution), max_y_data))
    max_y_data_without_0_degree = np.max((np.max(distribution[1:]),
                                          max_y_data_without_0_degree))
    min_y_data_nonzero = np.min((np.min(distribution[distribution != 0]),
                                 min_y_data_without_0_degree))

axes.legend(G_names)
axes.set_ylim((0, max_y_data + 0.05))
axes.set_xlim((-2, 100))

# Log-log axes
legend_log_log = list()
axes = axes_all[1]
for G, G_name, G_color in zip(Gs, G_names, G_colors):
    w.graph.plot_degree_distribution(
        G,
        direction=direction,
        axis_scaling='log-log',
        plot_type='scatter',
        as_probability_distribution=True,
        color=G_color,
        marker_size=40,
        label=G_name,
        axes=axes,
        annotate=['x_label']
    )

    # Power-law slope
    alpha = powerlaw.Fit(w.graph.degrees(G, direction=direction)).alpha
    legend_log_log.append(fr'{G_name}, $\alpha$ = {alpha:.2f}')

format_axes(axes)
axes.legend(legend_log_log)

axes.set_ylim((
    np.power(10, np.floor(np.log10(min_y_data_nonzero))),
    np.power(10, np.ceil(np.log10(max_y_data_without_0_degree)))
))

plt.show()

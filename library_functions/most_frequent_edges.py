import networkx as nx
import numpy as np
import pandas as pd

from IPython.core.display import display
from operator import itemgetter


def most_frequent_edges(graphs: nx.Graph,
                        n=None,
                        as_pandas=False,
                        printout=False):

    if not isinstance(graphs, dict):
        graphs = {'Graph 1': graphs}

    edges_sorted = dict()
    for graph_name, graph in graphs.items():
        edges_count = nx.get_edge_attributes(graph, "count")
        edges_count_sorted = sorted(edges_count.items(),
                                    key=itemgetter(1),
                                    reverse=True)

        if n is not None:
            edges_count_sorted = \
                edges_count_sorted[:min(len(edges_count_sorted), n)]

        edges_sorted[graph_name] = edges_count_sorted

    if as_pandas:
        column_names = list(edges_sorted.keys())
        max_length = max([len(value) for value in edges_sorted.values()])
        index = np.arange(max_length) + 1
        data = np.empty((max_length, len(edges_sorted)))
        edges_sorted_pandas = pd.DataFrame(data, columns=column_names)
        edges_sorted_pandas.set_index(pd.Index(index))

    if printout:
        if as_pandas:
            display(edges_sorted_pandas)
        else:
            print('\nMost frequent edges:')

            for graph_name, edges_count_sorted in edges_sorted.items():
                print(f'\n{graph_name}:')
                for index, (edge, count) in enumerate(edges_count_sorted):
                    print(f'\t{index + 1}. {edge}, {count} occurrences')

    if as_pandas:
        return edges_sorted_pandas
    else:
        return edges_sorted

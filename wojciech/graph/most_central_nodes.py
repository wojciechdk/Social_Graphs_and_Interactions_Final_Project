import networkx as nx
import numpy as np
import pandas as pd

from operator import itemgetter
from typing import Union, List, Tuple

def most_central_nodes(G: nx.Graph,
                       measures: Union[str, List, Tuple] = None,
                       n: int = np.inf,
                       printout: bool = False,
                       as_pandas: bool = False
                       ) -> Union[dict, pd.DataFrame]:

    # Set default measures.
    if measures is None:
        if G.is_directed():
            measures = ["degree",
                        "in-degree",
                        "out-degree",
                        "betweenness",
                        "eigenvector"]
        else:
            measures = ["degree",
                        "betweenness",
                        "eigenvector"]

    if isinstance(measures, str):
        measures = [measures]

    most_linked_dict = dict()
    for measure in measures:
        if measure == 'degree':
            most_linked = sorted(G.degree, key=itemgetter(1), reverse=True)

        elif measure == 'in-degree':
            most_linked = sorted(G.in_degree, key=itemgetter(1), reverse=True)

        elif measure == 'out-degree':
            most_linked = sorted(G.out_degree, key=itemgetter(1), reverse=True)

        elif measure == 'betweenness':
            most_linked = sorted(nx.betweenness_centrality(G).items(),
                                 key=itemgetter(1), reverse=True)

        elif measure == 'eigenvector':
            most_linked = sorted(nx.eigenvector_centrality(G).items(),
                                 key=itemgetter(1), reverse=True)
        else:
            raise ValueError(f'Unknown centrality measure: "{measure}"')

        most_linked_dict[measure] = most_linked[:min(n, len(most_linked))]

    if as_pandas:
        max_length = 0
        for most_linked in most_linked_dict.values():
            if len(most_linked) > max_length:
                max_length = len(most_linked)

        columns = list()
        data = np.empty((max_length, len(most_linked_dict) * 2), dtype=object)

        for measure_idx, (measure, most_linked) \
                in enumerate(most_linked_dict.items()):

            columns.append((measure.capitalize(), 'Drug'))
            columns.append((measure.capitalize(), 'Score'))

            data[:len(most_linked), measure_idx * 2] = \
                list(map(itemgetter(0), most_linked))
            data[:len(most_linked), measure_idx * 2 + 1] =\
                list(map(itemgetter(1), most_linked))

        most_linked_pandas = \
            pd.DataFrame(data,
                         columns=pd.MultiIndex.from_tuples(columns),
                         index=np.arange(data.shape[0]) + 1)

    if printout:
        if as_pandas:
            display(most_linked_pandas)
        else:
            for measure, most_linked in most_linked_dict.items():
                print(f'\nNodes with highest {measure} centrality:')
                for node, centrality_score in most_linked:
                    print(f'\t{node}: {centrality_score:.3f}')

    if as_pandas:
        return most_linked_pandas
    else:
        return most_linked_dict
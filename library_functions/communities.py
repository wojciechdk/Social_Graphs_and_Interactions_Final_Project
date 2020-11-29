#%%

from typing import Optional, Tuple, Union
import community
import networkx as nx
from infomap import Infomap

# %%


def assign_louvain_communities(
    reddit_graph, wiki_graph=None, reddit_edge_weight="count"
) -> Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]:
    """Calculate communities using the louvain algorithm and assign them as property to the graphs node.
    if two graphs are given, also assign one graph's communities to the other's.

    Args:
        reddit_graph ([type]): [description]
        wiki_graph ([type], optional): [description]. Defaults to None.

    Returns:
        Union[nx.Graph, Tuple[nx.Graph, nx.Graph]]: [description]
    """
    reddit_partition = community.best_partition(reddit_graph, weight=reddit_edge_weight)
    if wiki_graph:
        wiki_partition = community.best_partition(wiki_graph)
    for node in reddit_graph:
        reddit_graph.nodes[node]["louvain_community_reddit"] = reddit_partition[node]
        if wiki_graph:
            # Also add the community from the other graph to allow comparing
            try:
                reddit_graph.nodes[node]["louvain_community_wiki"] = wiki_partition[
                    node
                ]
            except:
                reddit_graph.nodes[node]["louvain_community_wiki"] = -1
    if wiki_graph:  # %%
        for node in wiki_graph:
            wiki_graph.nodes[node]["louvain_community_wiki"] = wiki_partition[node]

            # Also add the community from the other graph to allow comparing
            try:
                wiki_graph.nodes[node]["louvain_community_reddit"] = reddit_partition[
                    node
                ]
            except:
                wiki_graph.nodes[node]["louvain_community_reddit"] = -1

    return (
        (reddit_graph, reddit_partition, wiki_graph, wiki_partition)
        if wiki_graph
        else (reddit_graph, reddit_partition)
    )


def get_infomap_communities(graph: nx.Graph, reddit_edge_weight=None):
    im = Infomap("--flow-model undirected -N 10 --prefer-modular-solution")

    ## im only works with numerical ids, so we need to save a mapping

    ids_to_names = {}
    names_to_ids = {}

    for index, node in enumerate(graph.nodes):
        ids_to_names[index] = node
        names_to_ids[node] = index
        im.add_node(index, name=node)

    # iterate over edges and add them to the im tree, optionally adding the weight
    for e1, e2, data in graph.edges(data=True):
        e1_id = names_to_ids[e1]
        e2_id = names_to_ids[e2]
        weight = data[reddit_edge_weight] if reddit_edge_weight else None
        link = (e1_id, e2_id, weight) if weight else (e1_id, e2_id)
        im.add_link(*link)

    im.run()
    for node in im.tree:
        if node.is_leaf:
            graph.nodes[ids_to_names[node.node_id]][
                "infomap_community"
            ] = node.module_id

    return graph


# %%

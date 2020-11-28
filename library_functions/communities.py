#%%

from typing import Optional, Tuple, Union
import community
import networkx as nx

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
    # %%
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

    return (reddit_graph, wiki_graph) if wiki_graph else reddit_graph
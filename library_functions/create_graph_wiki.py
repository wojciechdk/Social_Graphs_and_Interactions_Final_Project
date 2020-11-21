import networkx as nx


def create_graph_wiki(wiki_data, substance_names):
    g_wiki = nx.DiGraph()
    g_wiki.add_nodes_from(substance_names, categories=[])

    # Assign categories from Wikipedia to drugs
    for index_drug, drug in enumerate(wiki_data['name']):
        if drug in g_wiki.nodes:
            g_wiki.nodes[drug]['categories'] = \
                wiki_data['categories'][index_drug]

    for index_drug, drug in enumerate(wiki_data['name']):
        if drug not in g_wiki.nodes:
            continue

        for drug_to_link_to, n_links in wiki_data['links'][index_drug].items():
            if drug_to_link_to in g_wiki.nodes:
                g_wiki.add_edge(drug, drug_to_link_to, count=n_links)

    return g_wiki

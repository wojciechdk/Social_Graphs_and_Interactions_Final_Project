import networkx as nx


def create_graph_reddit(drug_database_reddit, wiki_data, substance_names):
    g_reddit = nx.Graph()
    g_reddit.add_nodes_from(substance_names)

    # Assign categories from Wikipedia to drugs
    for index_drug, drug in enumerate(wiki_data['name']):
        if drug in g_reddit.nodes:
            g_reddit.nodes[drug]['categories'] = \
                wiki_data['categories'][index_drug]

    # Link drugs
    for reddit_post in drug_database_reddit.values():
        link_drugs(g_reddit,
                   reddit_post['matches'],
                   reddit_post['polarity'],
                   reddit_post['subjectivity'])

    return g_reddit


def link_drugs(G: nx.Graph, list_of_drugs, polarity, subjectivity):
    if len(list_of_drugs) <= 1:
        return G
    else:
        for index in range(len(list_of_drugs)):
            drug = list_of_drugs[index]
            other_drugs = list_of_drugs[(index + 1):]

            for other_drug in other_drugs:
                if (drug in G.nodes) & (other_drug in G.nodes):
                    G.add_edge(drug, other_drug,
                               polarity=polarity,
                               subjectivity=subjectivity)

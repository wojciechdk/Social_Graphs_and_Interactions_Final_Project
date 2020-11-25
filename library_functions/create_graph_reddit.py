import library_functions as lf
import networkx as nx


def create_graph_reddit():
    drug_database_reddit = lf.load_data_reddit()
    wiki_data = lf.load_data_wiki()
    substance_names = lf.load_substance_names()

    g_reddit = nx.Graph()
    g_reddit.add_nodes_from(substance_names)

    # Assign categories from Wikipedia to drugs
    for index_drug, drug in enumerate(wiki_data['name']):
        if drug in g_reddit.nodes:
            g_reddit.nodes[drug]['count'] = 0
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

            # Increase the count
            G.nodes[drug]['count'] += 0

            for other_drug in other_drugs:
                if (drug in G.nodes) & (other_drug in G.nodes):
                    edge = (drug, other_drug)
                    if G.has_edge(*edge):
                        G.edges[edge]['count'] += 1
                        G.edges[edge]['polarity'].append(polarity)
                        G.edges[edge]['subjectivity'].append(subjectivity)
                    else:
                        G.add_edge(*edge,
                                   count=1,
                                   polarity=[polarity],
                                   subjectivity=[subjectivity])

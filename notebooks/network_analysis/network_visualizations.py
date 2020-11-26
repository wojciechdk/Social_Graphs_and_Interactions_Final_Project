
# %%
import community
from fa2 import ForceAtlas2
from networkx.readwrite.adjlist import read_adjlist
from library_functions import  plotly_draw
import networkx as nx
from config import Config
import wojciech as w
import library_functions as lf
import importlib
#%%
# graph_reddit : nx.Graph
# graph_wiki : nx.Graph
# graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_gcc)
# graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)

graph_reddit = lf.create_graph_reddit()
graph_wiki = lf.create_graph_wiki()


graph_reddit = w.graph.largest_connected_component(graph_reddit)
# %%




positions_reddit = lf.get_fa2_layout(graph=graph_reddit, edge_weight_attribute="count")
# positions_reddit = forceatlas2.forceatlas2_networkx_layout(graph_reddit, pos=None, iterations=1000)
# %%
importlib.reload(plotly_draw)
from library_functions import  plotly_draw

# plotly_draw.draw_graph_plotly(
#     graph = graph_wiki,
#     positions=positions_wiki
# )
# %%
plotly_draw.draw_graph_plotly(
    graph=  graph_reddit,
    positions=positions_reddit,
    node_size_attribute="degree",
    edge_weight_attribute="count"
)

# %%
plotly_draw.draw_graph_plotly(
    graph=  graph_reddit,
    positions=positions_reddit,
    node_size_attribute="degree",
    node_color_attribute="louvain_community_wiki"
)
# %%
plotly_draw.draw_graph_plotly(
    graph=  graph_wiki,
    positions=positions_wiki,
    node_size_attribute="degree",
    node_color_attribute="louvain_community_wiki"
)
# %%

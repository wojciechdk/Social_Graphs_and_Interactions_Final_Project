
# %%
import community
from fa2 import ForceAtlas2
import bokeh
from library_functions import  plotly_draw
import networkx as nx
from config import Config
import wojciech as w

#%%
graph_reddit : nx.Graph
graph_wiki : nx.Graph
graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_gcc)
graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)


forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=True,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=0.5,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=1,
                        strongGravityMode=True,
                        gravity=0.001,

                        # Log
                        verbose=True)

positions_wiki = forceatlas2.forceatlas2_networkx_layout(graph_wiki, pos=None, iterations=1000)
# positions_reddit = forceatlas2.forceatlas2_networkx_layout(graph_reddit, pos=None, iterations=1000)
# %%


plotly_draw.draw_graph_plotly(
    graph = graph_wiki,
    positions=positions_wiki
)
# %%
plotly_draw.draw_graph_plotly(
    graph=  graph_reddit,
    positions=positions_reddit
)
# %%

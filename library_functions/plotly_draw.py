#%%

from typing import Dict, List, Tuple, Union
from networkx.drawing import layout
from networkx.generators import line
import plotly.graph_objects as go
import networkx as nx
import json
from config import Config

G = nx.random_geometric_graph(200, 0.125)
# %%
with open(Config.Path.contents_per_substance, "r+") as f:
    contents_per_substance =json.load(f)
with open(Config.Path.urls_per_substance, "r+") as f:
    url_per_substance =json.load(f)

def get_edge_trace(
    graph: nx.Graph,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
    edge_weight_attribute: str = None,
):
    edges_x = []
    edges_y = []

    for edge in graph.edges:
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edges_x += [x0, x1, None]
        edges_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edges_x,
        y=edges_y,
        line={"width": 0.5, "color": "black"},
        hoverinfo="none",
        mode="lines",
    )

    return edge_trace


def split_text_at(text :str, length: int) -> str :
    words = text.split()

    results = []
    line_length = 0
    for word in words:
        if line_length < length:
            results.append(word)
            line_length += len(word)
        else: 
            results.append("<br>")
            results.append(word)
            line_length = len(word)

    return " ".join(results )

    
def get_nodes_hover(graph: nx.Graph) -> List[str]:
    node_hovers = []

    for name , data in graph.nodes(data=True):
        hover = f"Nootropic: {name}, Degree: {graph.degree(name)}. <br>"

        if "categories" in data:
            hover += f"\n Part of {len(data['categories'])} categories. <br><br>"


        hover += f"\"{split_text_at(contents_per_substance[name][:120], 40)}...\"<br> <br> <br> "

        hover += f"Read more: {url_per_substance[name]}"
        node_hovers.append(hover)
    return node_hovers


def get_nodes_trace(
    graph: nx.Graph,
    node_weight_attribute: str = None,
    node_color_attribute: str = None,
    node_size_attribute: str = None,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
):
    nodes_x = []
    nodes_y = []
    for node in graph.nodes:
        nodes_x.append(positions[node][0])
        nodes_y.append(positions[node][1])

    hovers = get_nodes_hover(graph)

    node_names = list(graph.nodes)
    node_trace = go.Scatter(
        x=nodes_x, y=nodes_y, text=hovers, mode="markers", hoverinfo="text"
    )

    if node_color_attribute:
        pass

    return node_trace


def draw_graph_plotly(
    graph: nx.Graph,
    positions: Dict[Union[str, int], Tuple[int, int]] = None,
    edge_weight_attribute: str = None,
    edges_only: bool = False,
):

    # If no positions are passed, compute spring layout positioning
    if not positions:
        positions = nx.layout.spring_layout(G, weight=edge_weight_attribute)

    edge_trace = get_edge_trace(
        graph=graph, positions=positions, edge_weight_attribute=edge_weight_attribute
    )
    node_trace = get_nodes_trace(graph=graph, positions=positions)

    data = [edge_trace] if edges_only else [edge_trace, node_trace]
    figure = go.Figure(
        data=data,
        layout=go.Layout(
            showlegend=False,
            margin={
                "l": 20,
                "r": 20,
                "t": 25,
                "b": 25
            },
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        ),
    )
    return figure



import matplotlib.pyplot as plt
import networkx as nx
import wojciech as w
from typing import Any, Callable, Dict, Iterable, Tuple, Union


def plot_comparison_of_attribute_distributions(
        graphs: Dict[str, nx.Graph],
        attribute_name: str,
        attribute_parent: str,
        attribute_function: Callable[['str'], Any] = None,
        attribute_function_name: str = '',
        as_probability_distribution: bool = False,
        bar_width_scaling: float = 1,
        bins: Union[int, Iterable[Union[int, float]]] = 100,
        x_limit: Tuple[Union[float, int], Union[float, int]] = None,
        fig_width: Union[float, int] = 8,
        show: bool = True
):
    # Create subplots.
    figure_size = (fig_width, fig_width / 3 * len(graphs) + 1)
    figure, axess = plt.subplots(len(graphs), 1,
                                 figsize=figure_size,
                                 sharex='all',
                                 sharey='all')

    # Plot distributions.
    for index, ((graph_name, graph), axes) \
            in enumerate(zip(graphs.items(), axess)):

        # Create the figure title.
        figure.suptitle(f'Distribution of the {attribute_parent} attribute: '
                        f'"{attribute_name}"',
                        y=min(0.98 + 0.003 * (len(graphs) - 1), 0.995),
                        size=20)

        # Plot the degree distribution in the chosen axes.
        w.graph.plot_distribution(
            graph,
            quantity='attribute',
            attribute_name=attribute_name,
            attribute_parent=attribute_parent,
            attribute_function=attribute_function,
            attribute_function_name=attribute_function_name,
            as_probability_distribution=as_probability_distribution,
            plot_type='bar',
            bar_width_scaling=bar_width_scaling,
            bins=bins,
            axes=axes,
            annotate=False
        )

        # Annotate the graphs.
        axes.set_title(graph_name)

        if as_probability_distribution:
            axes.set_ylabel('Probability of value')
        else:
            axes.set_ylabel('Count')

        if index == len(graphs) - 1:
            if attribute_function is not None:
                axes.set_xlabel(f'{attribute_function_name}({attribute_name})')
            else:
                axes.set_xlabel(f'{attribute_name}')

        if x_limit is not None:
            axes.set_xlim(x_limit)

        # Format the axes.
        axes.spines['top'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.set_facecolor('white')
        axes.xaxis.label.set_fontsize(12)
        axes.yaxis.label.set_fontsize(12)
        axes.title.set_fontsize(14)

    # Adjust the layout
    figure.tight_layout()

    # Display the graph.
    if show:
        plt.show()

    return axess

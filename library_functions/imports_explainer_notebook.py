# %%
import numpy as np
import pandas as pd
import networkx as nx
import warnings
import random
import wojciech as w
from tqdm.auto import tqdm

from IPython.core.interactiveshell import InteractiveShell
from IPython.display import Markdown, display


try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config

warnings.filterwarnings("ignore")


def printmd(string):
    display(Markdown(string))


# Maximum of rows to show for the pandas tables
pd.options.display.max_rows = 100

# Show all code outputs in the cell outputs
InteractiveShell.ast_node_interactivity = "all"
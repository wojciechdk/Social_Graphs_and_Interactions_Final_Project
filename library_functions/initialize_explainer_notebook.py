# Imports
import library_functions as lf
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import warnings
import wojciech as w

from fa2 import ForceAtlas2
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import Markdown, display
from library_functions.config import Config


# Define a function that will print a markdown text.
def printmd(string):
    display(Markdown(string))


# Disable warnings
warnings.filterwarnings('ignore')

# Define maximum of rows to show for the pandas tables
pd.options.display.max_rows = 100

# Show all code outputs in the cell outputs
InteractiveShell.ast_node_interactivity = "all"

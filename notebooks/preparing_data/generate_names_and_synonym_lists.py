# %%

# Add wojciech's library to path:

import sys
sys.path.append("../../../")

##% 
# For normal python files
from ...library_functions import load_data_wiki, save_synonym_mapping
# %%
# for notebooks:
# from library_functions import load_data_wiki, save_synonym_mapping

# %%
from pathlib import Path 
root = Path("/home/ldorigo/MEGA/DTU/Q2/social_graphs/Social_Graphs_Exercises/project")
wiki_data = load_data_wiki.load_data_wiki(root=root)

# %%

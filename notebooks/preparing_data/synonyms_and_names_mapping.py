# %%
from config import Config
import json 
from library_functions import load_data_wiki, save_synonym_mapping
# %%


wiki_data = load_data_wiki.load_data_wiki()
# %%
save_synonym_mapping.save_synonym_mapping(wiki_data)
save_synonym_mapping.save_substance_names(wiki_data)
# %%

import json
from config import Config


def save_synonym_mapping(wiki_data):
    """Save a mapping from synonyms to substance names

    Args:
        wiki_data (Dict): Flat dict of substance names
    """
    
        # Small snippet to save an inverse mapping from synonyms to names
    synonym_mapping = {}

    for index, name in enumerate(wiki_data["name"]):
        for synonym in wiki_data["synonyms"][index]:
            synonym_mapping[synonym] = name
        # Also map from the substance to itself
        synonym_mapping[name] = name

    with open(Config.Path.synonym_mapping, "w+") as f:
        json.dump(synonym_mapping, f, indent=2)

def save_substance_names(wiki_data):
    """Save the list of all substance names to a json file.

    Args:
        wiki_data (Dict): Dict containing the wikipedia data (flat)
    """
    with open(Config.Path.substance_names, "w+") as f:
        json.dump(wiki_data["name"], f, indent=2)

def save_contents(wiki_data):
    with open(Config.Path.contents_per_substance, "w+") as f:
        json.dump(dict(zip(wiki_data["name"], wiki_data["content"])), f)

def save_urls(wiki_data):
    with open(Config.Path.urls_per_substance, "w+") as f:
        json.dump(dict(zip(wiki_data["name"], wiki_data["url"])), f)
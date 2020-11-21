import json
from config import Config


def save_synonym_mapping(wiki_data):
    # Small snippet to save an inverse mapping from synonyms to names
    synonym_mapping = {}

    for index, name in enumerate(wiki_data["name"]):
        for synonym in wiki_data["synonyms"][index]:
            synonym_mapping[synonym] = name
        # Also map from the substance to itself
        synonym_mapping[name] = name

    with open(Config.Path.synonym_mapping, "w+") as f:
        json.dump(synonym_mapping, f, indent=2)

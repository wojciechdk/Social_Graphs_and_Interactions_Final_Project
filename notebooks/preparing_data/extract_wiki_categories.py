# %%
from typing import List, Set
from config import Config
import json
from library_functions import load_data_wiki
import sys

sys.path.append("..")
from mediawiki.mediawiki import MediaWiki

# %%
wiki_data = load_data_wiki()
# %%


with open(Config.Path.psychoactive_category_tree_clean, "r") as f:
    ct = json.load(f)


psychological_effect_root = [
    "Anxiogenics",
    "Anxiolytics",
    "Aphrodisiacs",
    "Depressogenics",
    "Entactogens and empathogens",
    "Mood stabilizers",
    "Oneirogens",
    "Psychoanaleptics",
    "Psycholeptics" "Antidepressants‎",
    "Stimulants",
]
# %%
psychological_effect_map = {
    "Antidepressants": [
        "Reversible inhibitors of MAO-A",
        "Azapirones",
        "Bicyclic antidepressants",
        "Monoamine oxidase inhibitors",
        "Noradrenergic and specific serotonergic antidepressants",
        "Norepinephrine-dopamine reuptake inhibitors",
        "Selective serotonin reuptake inhibitors",
        "Serotonin-norepinephrine reuptake inhibitors",
        "Tetracyclic antidepressants",
        "Tricyclic antidepressants",
    ],
    "Stimulants": [
        "Herbal and fungal stimulants",
        "RTI compounds",
        "Sympathomimetic amines",
        "Pyrrolidinophenones‎",
        "Masticatories‎",
        "Tobacco",
    ],
}
# %%
mw = MediaWiki()

ct = mw.categorytree("Psychoactive drugs by mechanism of action", depth=15)

#%%
ct = ct['Psychoactive drugs by mechanism of action']

# %%
def build_category_mapping(category):
    def extract_categories(tree, current: Set[str]) -> Set[str]:
        for subcategory in tree["sub-categories"]:
            if subcategory not in current:
                current.union(extract_categories(tree["sub-categories"][subcategory], current))
                current.add(subcategory)
        return current

    ct = mw.categorytree(category, depth=15)
    ct = ct[category]

    results = {
        key: extract_categories(ct["sub-categories"][key], set())
        for key in ct["sub-categories"].keys()
    }
    return results

# %%
categories_mechanism = build_category_mapping('Psychoactive drugs by mechanism of action')
# %%
categories_effects = build_category_mapping('Drugs by psychological effects')

# %%

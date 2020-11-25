from pathlib import Path


class Config:

    class Path:

        # Project root
        project_root = Path(__file__).parent

        # Shared data:
        shared_data_folder = project_root / 'shared_data'

        dietary_supplements_category_tree_clean = \
            shared_data_folder / 'dietary_supplements_category_tree_clean.json'

        dietary_supplements_category_tree_raw = \
            shared_data_folder / 'dietary_supplements_category_tree_raw.json'

        full_category_tree_clean = \
            shared_data_folder / 'full_category_tree_clean.json'

        full_wiki_data = \
            shared_data_folder / 'full_wiki_data.json'

        psychoactive_category_tree_clean = \
            shared_data_folder / 'psychoactive_category_tree_clean.json'

        psychoactive_category_tree_raw = \
            shared_data_folder / 'psychoactive_category_tree_raw.json'

        reddit_data_with_NER = shared_data_folder / 'reddit_data_with_NER.json'

        reddit_data_with_NER_and_sentiment = \
            shared_data_folder / 'reddit_data_with_NER_and_sentiment.json'

        substance_names = shared_data_folder / 'substance_names.json'

        synonym_mapping = shared_data_folder / 'synonym_mapping.json'


        # Wiki data:
        wiki_data_folder = shared_data_folder / 'wikipedia_data'


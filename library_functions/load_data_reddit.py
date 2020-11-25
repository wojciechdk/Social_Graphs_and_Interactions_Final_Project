import json
from config import Config


def load_data_reddit():
    with open(Config.Path.reddit_data_with_NER_and_sentiment) as file:
        drug_database_reddit = json.load(file)

    return drug_database_reddit

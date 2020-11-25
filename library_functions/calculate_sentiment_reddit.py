import json

from config import Config
from textblob import TextBlob
from tqdm import tqdm


def calculate_sentiment_reddit():
    with open(Config.Path.reddit_data_with_NER) as file:
        drug_database_reddit = json.load(file)

    for post_id, post in tqdm(drug_database_reddit.items()):
        analysis = TextBlob(post['content'])
        post['polarity'] = analysis.polarity
        post['subjectivity'] = analysis.subjectivity

    with open(Config.Path.reddit_data_with_NER_and_sentiment, 'w+') as file:
        json.dump(drug_database_reddit, file)

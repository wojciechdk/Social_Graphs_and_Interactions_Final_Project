#%%
import json
import os
from pathlib import Path
from psaw import PushshiftAPI
# %%
api = PushshiftAPI()
# %%
reddit_path = Path.cwd().joinpath("reddit_data")
os.mkdir(reddit_path)
# %%
reddit_comments_path = reddit_path.joinpath("comments")
reddit_submissions_path = reddit_path.joinpath("submissions")

os.mkdir(reddit_comments_path)
os.mkdir(reddit_submissions_path)
# %%

def save_submissions(submission):
    relevant_dict = {
        "title": submission.title,
        "author": submission.author,
        "timestamp": submission.created,
        "id": submission.id,
    }
    try:
        relevant_dict["content"]= submission.selftext
    except :
        relevant_dict["content"] = ""
    with open(reddit_submissions_path.joinpath(relevant_dict["id"] + ".json"), "w+") as f: 
        json.dump(relevant_dict, f)
# %%
all_submissions = api.search_submissions(subreddit="nootropics", filter=["title","author","created_utc","id","selftext","url"])
# %%
for i, sub in enumerate(all_submissions):

    if i % 100 == 0:
        print(f"Downloading submissions {i} - {i+100}.")

    save_submissions(sub)
# %%

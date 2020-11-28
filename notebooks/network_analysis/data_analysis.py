# %%
import json
import library_functions as lf
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import powerlaw
import wojciech as w

from config import Config
from fa2 import ForceAtlas2
from operator import itemgetter
from pandas_profiling import ProfileReport
from pathlib import Path

#%%
reddit_data = lf.load_data_reddit()

content_length = [len(post['content']) for post in reddit_data.values()]

figure, axes = w.empty_figure()

axes.hist(content_length,
          bins=np.linspace(0, 5000, 501))

plt.show()

#%%
nonempty_posts_less_than_25 = [(post['content'], post['matches'])
                               for post in reddit_data.values()
                               if 0 < len(post['content']) < 25]

posts_polarity_0 = [(post['content'], len(post['content']), post['matches'])
                    for post in reddit_data.values()
                    if post['polarity'] == 0]



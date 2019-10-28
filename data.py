# %%
DEBUG = True

# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import streamlit as st

# %% [markdown]
# A simple script to grabs all authors and papers name

# %%
url = 'https://nips.cc/Conferences/2019/AcceptedPapersInitial'
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

titles= list(map(lambda x:x.text, soup.select("div > p > b")))
authors=list(map(lambda x:x.text, soup.select("div > p > i")))

if DEBUG:
    titles = titles[:10]
    authors = authors[:10]


# %%
papers_df = pd.DataFrame(list(zip(titles, authors)),columns=['Title', 'Author'])
# Output to a csv
# papers_df.to_csv('papers.csv', index=False)

# %%
# class Paper:
#     def __init__(self, title, author):
#         self.title=title
#         self.author=author
    
#     def __repr__(self):
#         return f"Title: {self.title} \nAuthor(s): {self.author}\n"

# %%
class Filter:
    def __init__(self, papers):
        self.papers = papers_df
    
    def __call__(self, filter_str):
        print('call')
        result = self.filter_by_text(filter_str)
        return result
    
    def __getattr__(self, name):
        print('overload attr')
        return getattr(self.papers,name)
        
    def filter_by_text(self, filter_str):
        filter_str = filter_str.lower()
        filters = filter_str.split(",")
        filters = "|".join(filters)
        idx = self.Author.str.lower().str.contains(filters)
        return self.papers[idx]
    
    def filter_by_keyword(self, filter_str):
        result = []
        filters = filter_str.split(",")
        for paper in self.papers:
            for author in paper.author:
                for filter in filters:
                    if filter in author:
                        result.append(paper)
                        continue

        return result



# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]

# %%
filter =Filter(papers_df)

# %% [markdown]
# # keyword

# %%
keywords_df = pd.read_csv('handcounted_inst.csv')
keywords = keywords_df.keywords

# %% [markdown]
# # Embedding

# %%
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

# Compute a representation for each message, showing various lengths supported.
messages = titles

# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

with tf.Session() as session:
  session.run([tf.global_variables_initializer(), tf.tables_initializer()])
  message_embeddings = session.run(embed(messages))

#   for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
#     print("Message: {}".format(messages[i]))
#     print("Embedding size: {}".format(len(message_embedding)))
#     message_embedding_snippet = ", ".join(
#         (str(x) for x in message_embedding[:3]))
#     print("Embedding: [{}, ...]\n".format(message_embedding_snippet))


# %%
message_embeddings.shape

# %%
if DEBUG:
    np.save('embeddings_debug.npy', message_embeddings)
else:
    np.save('embeddings.npy', message_embeddings)
    

# %%
titles[0]

# %%

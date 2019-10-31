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
url = "https://nips.cc/Conferences/2019/AcceptedPapersInitial"
url="https://nips.cc/Conferences/2019/Schedule?type=Poster"
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")


# %%
# # Save HTML in case their UI change again :(
# with open("poster.html", "wb") as f:
#   f.write(res.content)

# %%
posters_soup=soup.find_all("div", class_="maincard narrower Poster")
print(f"Found {len(c)} posters!!!")
if DEBUG:
    posters_soup=posters_soup[:5]

# %%
example = posters_soup[0]


# %%
def get_event_type(poster):  
        return poster.find_all(class_="maincardHeader")[0].text

def get_details(poster):  
        return poster.find_all(class_="maincardHeader")[1].text

    
def get_category(poster):  
        return poster.find_all(class_="maincardHeader")[2].text
    
def get_authors(poster):
    return poster.find(class_="maincardFooter").text

    
def get_titles(poster):  
        return poster.find(class_="maincardBody").text


# %%
posters_soup[0]

# %%
fn_list = [get_event_type, get_details,get_titles,get_category, get_authors]

for fn in fn_list:
    print(fn.__name__,": ", fn(example))

# %%
posters_list = []

# %%
for poster in posters_soup:
    columns = []
    for fn in fn_list:
        columns.append(fn(poster))
    posters_list.append(columns)

# %%
cols = [
    "event_type","time","title","category","author"
]

# %%
posters = pd.DataFrame(posters_list,columns=cols)
posters['location'] = posters['time'].copy()

# %%
posters.head().T


# %%
# Output to a csv
# posters.to_csv('posters.csv', index=False)

# %%
class Filter:
    def __init__(self, papers):
        self.papers = papers_df

    def __call__(self, filter_str):
        print("call")
        result = self.filter_by_text(filter_str)
        return result

    def __getattr__(self, name):
        print("overload attr")
        return getattr(self.papers, name)

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
filter = Filter(posters)

# %% [markdown]
# # Embeddings with Google Universal Sentence Encoder

# %%
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

# Compute a representation for each message, showing various lengths supported.
messages = posters['title'].tolist()


# %%
module_url = (
    "https://tfhub.dev/google/universal-sentence-encoder/2"
)  # @param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)



# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    message_embeddings = session.run(embed(messages))


# %%
for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
    print("Message: {}".format(messages[i]))
    print("Embedding size: {}".format(len(message_embedding)))
    message_embedding_snippet = ", ".join(
        (str(x) for x in message_embedding[:3]))
    print("Embedding: [{}, ...]\n".format(message_embedding_snippet))
    break


# %%
if DEBUG:
    np.save("embeddings_debug.npy", message_embeddings)
else:
    np.save("embeddings.npy", message_embeddings)


# %%
corr = np.inner(message_embeddings, message_embeddings) # calculate the correlation with dot product

# %%

if DEBUG:
    np.save("corr_debug.npy", corr)
    np.save("titles_debug.npy", titles)
    np.save("authors_debug.npy", authors)
    
else:
    np.save("corr.npy", corr)
    np.save("titles.npy", titles)
    np.save("authors.npy", authors)

# %%

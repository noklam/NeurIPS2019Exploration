# %%
DEBUG = True

# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import streamlit as st

# %% [markdown]
# A simple script to grabs all authors and posters
#  name

# %%
# url = "https://nips.cc/Conferences/2019/AcceptedpostersInitial" # The site is changed :(
url = "https://nips.cc/Conferences/2019/Schedule?type=Poster"
base_url = "https://nips.cc"
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")


# %%
# # Save HTML in case their UI change again :(
# with open("poster.html", "wb") as f:
#   f.write(res.content)

# %%
posters_soup = soup.find_all("div", class_="maincard narrower Poster")
print(f"Found {len(posters_soup)} posters!!!")
if DEBUG:
    posters_soup = posters_soup[:5]

# %%
example = posters_soup[0]


# %%
def get_titles(poster):
    return poster.find(class_="maincardBody").text


def get_authors(poster):
    return poster.find(class_="maincardFooter").text


def get_event_type(poster):
    return poster.find_all(class_="maincardHeader")[0].text


def get_details(poster):
    return poster.find_all(class_="maincardHeader")[1].text


def get_category(poster):
    return poster.find_all(class_="maincardHeader")[2].text

def get_href(poster):
    return base_url + poster.find("a", href=True).attrs.get('href', None)


# %%
fn_list = [get_titles, get_authors, get_category, get_event_type, get_details, get_href]

for fn in fn_list:
    print(fn.__name__, ": ", fn(example))

# %%
posters_list = []

# %%
for poster in posters_soup:
    columns = []
    for fn in fn_list:
        columns.append(fn(poster))
    posters_list.append(columns)

# %%
cols = ["title", "author", "category", "event_type", "time", "link"]

# %%
posters = pd.DataFrame(posters_list, columns=cols)
posters["location"] = posters["time"].copy()

# %% [markdown]
# # Clean up the data a little bit

# %% [markdown]
# I know this is not the most elegant way to clean up the data... but that's not the point here. :)
# Most data are fine, but we can clean up the time column and category a little bit.

# %%
posters["time"] = posters["time"].str.split("@").str[0].str.strip()
posters["location"] = posters["location"].str.split("@").str[1]
posters["location"] = posters["location"].str.split("#").str[0].str.strip()
posters["category"] = posters["category"].str.split("\n").str[-2]
posters["sub_category"] = posters["category"].copy().str.split("--").str[-1].str.strip()
posters["category"] = posters["category"].str.split("--").str[-2].str.strip()


# %%
# # Output to a csv
if DEBUG:
    posters.to_csv("posters_debug.csv", index=False)
else:
    posters.to_csv("posters.csv", index=False)
    

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
messages = posters["title"].tolist()


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
    message_embedding_snippet = ", ".join((str(x) for x in message_embedding[:3]))
    print("Embedding: [{}, ...]\n".format(message_embedding_snippet))
    break


# %%
if DEBUG:
    np.save("embeddings_debug.npy", message_embeddings)
else:
    np.save("embeddings.npy", message_embeddings)


# %%
corr = np.inner(
    message_embeddings, message_embeddings
)  # calculate the correlation with dot product

# %%
if DEBUG:
    np.save("corr_debug.npy", corr)
else:
    np.save("corr.npy", corr)

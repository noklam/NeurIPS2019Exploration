# %%
DEBUG = True
n = 5
# %%
import re
import pandas as pd
import streamlit as st
import numpy as np

# %% [markdown]
# A simple script to grabs all authors and papers name

# %%
if DEBUG:
    corr=np.load("corr_debug.npy")
 
else:
    corr=np.load("corr.npy")
    
posters = pd.read_csv('posters.csv')

# %%
posters.head().T

class Filter:
    def __init__(self, posters, corr):
        self.posters = posters
        self.corr = corr
    def __call__(self, filter_str):
        print("call")
        result = self.filter_by_text(filter_str)
        return result

    def __getattr__(self, name):
        return getattr(self.posters, name)

    def _get_filters(self, filter_str):
        filters = filter_str.lower().split(",")
        return "|".join(filters)

    def filter_by_text_input(self, filter_str):
        filters = self._get_filters(filter_str)
        booleans_author = self.author.str.lower().str.contains(filters)
        booleans_title = self.title.str.lower().str.contains(filters)
        return (booleans_author) & (booleans_title)

    def get_result_by_idx(self, idxs):
        return self.posters[idxs]

    def feel_luck(self):
        n = len(self.posters)
        idxs = np.random.randint(low=0, high=n-1, size=n)
        return self.get_result_by_idx(idxs)

    def filter_by_similarity(self, query_idx):
        poster_idxs = self.corr[query_idx, :].argsort()[::-1][1:n+1]  # Top N ignore the paper itself
        poster = self.posters.loc[poster_idxs]
        poster["Similarity Score"] = corr[query_idx, poster_idxs]
        return poster


# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]
width = 10
st.header("NeurIPS 2019")
st.subheader("Dec 8 - Dec 14")
st.text(
    "This year, the NeurIPS has an record-breaking number of accepted paper, __1429__ accepted papers!! \nIt is impossible to scan all the papers, instead of going through the list, I make a little search engine to search paper effectively"
)
# %%
filter = Filter(posters, corr)

# %%
filter_input = st.sidebar.text_input("Filter by author")
st.write("Filter by search query", filter.filter_by_text_input(filter_input))
# %%
box = st.sidebar.selectbox("Select by box", ["1","2","3"])
st.write("Filter by Date", filter.filter_by_text_input(box))

# %%
st.write("Hello")

## Sidebar for Select Top N Results
top_n = [3, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)

# %%
st.write(f"Top {n} similar result to", filter.filter_by_similarity(1))
# %%
if DEBUG:
    st.write("top_n", n)
    st.write("search_query", filter_input)
# %%

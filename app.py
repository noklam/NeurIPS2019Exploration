# %%
DEBUG = True
n = 10
# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import streamlit as st
import numpy as np

# %% [markdown]
# A simple script to grabs all authors and papers name

# %%
url = "https://nips.cc/Conferences/2019/AcceptedPapersInitial"
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

titles = list(map(lambda x: x.text, soup.select("div > p > b")))
authors = list(map(lambda x: x.text, soup.select("div > p > i")))

if DEBUG:
    titles = titles[:10]
    authors = authors[:10]

# %%
papers_df = pd.DataFrame(list(zip(titles, authors)), columns=["Title", "Author"])
# Output to a csv
# papers_df.to_csv('papers.csv', index=False)


class Filter:
    def __init__(self, papers, corr):
        self.papers = papers_df
        self.corr = corr

    def __call__(self, filter_str):
        print("call")
        result = self.filter_by_text(filter_str)
        return result

    def __getattr__(self, name):
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

    def filter_by_similarity(self, idx):
        idxs = self.corr[idx, :].argsort()[::-1][1:n+1]  # Top N ignore the paper itself
        paper = self.papers.loc[idxs]
        paper["Similarity Score"] = corr[idxs]
        return paper


# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]
width = 10
st.header("NeurIPS 2019")
st.subheader("Dec 8 - Dec 14")
st.text(
    "This year, the NeurIPS has an record-breaking number of accepted paper, __1429__ accepted papers!! \nIt is impossible to scan all the papers, instead of going through the list, I make a little search engine to search paper effectively"
)
search_query = st.text_area(
    "You can use the sidebar to search for interested paper by title or author, and get a list of top n similar papers."
)
st.write(search_query)

# %%
if DEBUG:
    corr = np.load("corr_debug.npy")
else:
    corr = np.load("corr.npy")
filter = Filter(papers_df, corr)

# %% [markdown]
# # keyword

# %%
keywords_df = pd.read_csv("handcounted_inst.csv")

# %%
keywords = keywords_df.keywords

# %%
st.dataframe(filter.filter_by_text(keywords[1]), width=10)

# %%
keywords_df.keywords
# %%
filter_input = st.sidebar.text_input("Filter by author")
st.write("Filter by search query", filter.filter_by_text(filter_input))
box = st.sidebar.selectbox("Select by box", keywords)
st.write("Filter by keywords", filter.filter_by_text(box))
st.sidebar.text(f"Keywords: {box}")
# %%
st.write("Hello")

# %%
## Sidebar for Select Top N Results
top_n = [5, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)

st.write(f"Top {n} similar result to", filter.filter_by_similarity(1))

if DEBUG:
    st.write("top_n", n)
    st.write("search_query", search_query)
# %%

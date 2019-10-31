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
    titles=np.load("titles_debug.npy")
    authors=np.load("authors_debug.npy")
    
else:
    corr=np.load("corr.npy")
    titles=np.load("titles.npy")
    authors=np.load("authors.npy")
    
posters = pd.read_csv('posters.csv')

# %%
posters.head().T

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

    def _get_filters(self, filter_str):
        filters = filter_str.lower().split(",")
        return "|".join*(filters)

    def filter_by_text_input(self, filter_str):
        filters = self._get_filters(filter_str)
        booleans_author = self.Author.str.lower().str.contains(filters)
        booleans_title = self.Title.str.lower().str.contains(filters)
        return (booleans_author) & (booleans_title)

    def get_result_by_idx(self, idxs):
        return self.papers[idxs]

    def feel_luck(self):
        n = len(self.papers)
        idxs = np.random.randint(low=0, high=n-1, size=n)
        return self.get_result_by_idx(idxs)

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

# %%
pe

# %%
papers_df = pd.DataFrame(list(zip(titles, authors)), columns=["Title", "Author"])
filter = Filter(papers_df, corr)

# %% [markdown]
# # keyword

# %%
keywords_df = pd.read_csv('handcounted_inst.csv')
keywords = keywords_df['keywords']

# %%
st.title('Hello~')
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

## Sidebar for Select Top N Results
top_n = [5, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)
# %%
filter.papers.shape

# %%
st.write(f"Top {n} similar result to", filter.filter_by_similarity(1))
# %%
if DEBUG:
    st.write("top_n", n)
    st.write("search_query", search_query)
# %%

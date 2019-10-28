# %%
DEBUG =True

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
url = 'https://nips.cc/Conferences/2019/AcceptedPapersInitial'
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

titles= list(map(lambda x:x.text, soup.select("div > p > b")))
authors=list(map(lambda x:x.text, soup.select("div > p > i")))


# %%
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
if DEBUG:
    corr = np.load('corr_debug.npy')
else:
    corr = np.load('corr.npy')


# %%
class Filter:
    def __init__(self, papers, corr):
        self.papers = papers_df
        self.corr = corr
    
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
    def filter_by_similarity(self, idx):
        n=5 # Top 10 similarity
        idxs=self.corr[idx,].argsort()[::-1][1:n+1] # Ignore the paper itself
        papers = self.papers.iloc[idxs]
        papers['Similarity Score'] = self.corr[idx,idxs]
        return papers


# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]

# %%
filter = Filter(papers_df, corr)

# %% [markdown]
# # keyword

# %%
keywords_df = pd.read_csv('handcounted_inst.csv')
keywords = keywords_df.keywords

# %%
st.title('Hello~')

# %%
filter_input = st.text_input('Filter by author')
st.write(filter.filter_by_text(filter_input))
box = st.sidebar.selectbox('Select by box', keywords)
st.write(filter.filter_by_text(box))
st.sidebar.text(f"Keywords: {box}")
# %%
st.write('Hello')

# %%
filter.filter_by_similarity(1)

# %%

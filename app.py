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
        idx = self.Author.str.lower().str.contains(filter_str)
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

# %%
keywords = keywords_df.keywords

# %%
filter.filter_by_text(keywords[1])

# %%
keywords_df.keywords

# %%
st.title('Hello~')

# %%
filter_input = st.text_input('Filter by author')
st.write(filter.filter_by_text(filter_input))

# %%
st.write('Hello')
authorauthor
# %%

# %%

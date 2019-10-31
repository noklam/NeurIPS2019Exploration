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


@st.cache
def load_data():
    posters = pd.read_csv('posters.csv')
    return posters

class Filter:
    def __init__(self, posters, corr):
        self.posters = posters
        self.corr = corr
        self.search_query = ""
        self.date = None
        self.similar = None
        self.time = ""
        self.location=""
        self.category=""
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

    def get_filter_result(self,filter_str):
        booleans = self.filter_by_text_input(filter_str)
        return self.get_result_by_idx(booleans)

    def get_result_by_idx(self, idxs):
        return self.posters.loc[idxs]

    def feel_lucky(self, query):
        n = len(self.posters)
        n_array = np.arange(n)
        idxs = np.random.permutation(n)
        return self.get_result_by_idx(idxs)
        
    def pick_one(self):
        n = len(self.posters)
        n_array = np.arange(n)
        idxs = np.random.choice(n)
        return  self.get_result_by_idx(idxs)['title']

    def filter_by_similarity(self, query_idx):
        poster_idxs = self.corr[query_idx, :].argsort()[::-1][1:n+1]  # Top N ignore the paper itself
        poster = self.posters.loc[poster_idxs]
        result = pd.DataFrame()
        result['Similarity Score'] = corr[query_idx, poster_idxs]
        result = pd.concat([result, poster], axis=1)
        return result


# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]
width = 10
st.image("imgs/neurips.png", use_column_width=True)
st.header("NeurIPS 2019")
st.text("Dec 8 - Dec 14")
st.header("Introduction")
st.markdown("> 1428, the number of accepted papers of NeurIPS in 2019.")

st.write(" ")
st.markdown("It is impossible to scan all the papers, instead of going through the list, you can use this app to help you to find the paper you are interested.")
st.markdown(
    "You can use the sidebar to search for interested paper by title or author, and get a list of top n similar papers. If you have no idea to start, just click the '__Feel Lucky__' button on the side, it will pick a paper for you and show the most similar results to you.")


# %%
# filter = Filter(load_data(), corr)
posters = pd.read_csv('posters.csv')
filter = Filter(posters, corr)

# Lucky Button
# %%
# if not filter.search_query:
    # filter.search_query = filter.pick_one()

lucky_button=st.sidebar.button("Feel Lucky", 'HI')
if lucky_button:
    filter.search_query = filter.pick_one()
    st.sidebar.text(filter.search_query)
st.sidebar.text(lucky_button)

# %%
# Search query
filter.search_query = st.sidebar.text_input("Search by title/author, use ',' to separate your crteria. For example, you can search 'jeff, dean' as two crteria", filter.search_query)
st.subheader("Your search result")
st.write(filter.get_filter_result(filter.search_query))



# %%
st.subheader(f"Your top search result is:")
search_result = filter.get_filter_result(filter.search_query)
if not search_result.empty:
    st.markdown(f"__{search_result.iloc[0].title}__")
else:
    st.markdown(f"No matched records, try modify your search query _{filter.search_query}_ or clean up the filter")
st.write(f"The Top {n} similar posters to this are:", filter.filter_by_similarity(1))


# filter.feel_lucky(1)

# Sidebar filter for time
time = filter.posters['time'].unique()
time = np.insert(time, 0, 'All')
st.sidebar.selectbox("Filter by time", time)

# Sidebar filter for venue
location = filter.posters['location'].unique()
location = np.insert(location, 0, 'All')
st.sidebar.selectbox("Filter by venue", location)

# Sidebar filter for category
category = filter.posters['category'].unique()
category = np.insert(category, 0, 'All')
st.sidebar.selectbox("Filter by category", category)


## Sidebar for Select Top N Results
top_n = [3, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)



# %%
if DEBUG:
    st.sidebar.text("DEBUG")
    st.sidebar.text(f"top_n: {n}")
    st.sidebar.text(f"search_query: {filter.search_query}")

st.markdown(f"GitHub: https://github.com/noklam/NeurIPS2019Exploration")
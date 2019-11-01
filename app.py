# %%
# %load_ext autoreload
# %autoreload 2

# %%
DEBUG = True
# %%
import re
import pandas as pd
import streamlit as st
import numpy as np
from filter import Filter

# %% [markdown]
# A simple script to grabs all authors and papers name

# %%
if DEBUG:
    corr = np.load("corr_debug.npy")

else:
    corr = np.load("corr.npy")


@st.cache
def load_data():
    posters = pd.read_csv("posters.csv")
    return posters


# class Filter:
#     def __init__(self, posters, corr):
#         self.posters = posters
#         self.corr = corr
#         self.search_query = ""
#         self.date = None
#         self.similar = None
#         self.time = ""
#         self.location = ""
#         self.category = ""
#         self.n = 5

#     def __call__(self, filter_str):
#         print("call")
#         result = self.filter_by_text(filter_str)
#         return result

#     def _get_filters(self, filter_str):
#         filters = filter_str.lower().split(",")
#         print("".join([f"(?={filter})" for filter in filters]))
#         return "".join([f"(?={filter})" for filter in filters])

#     def filter_by_text_input(self, filter_str):
#         filters = self._get_filters(filter_str)
#         booleans_author = self.posters.author.str.lower().str.contains(filters)
#         # booleans_author = [self.posters.author.str.lower().str.contains(filter) ]
#         # booleans_author = self.posters.author.str.lower().str.contains(filters)
#         booleans_title = self.posters.title.str.lower().str.contains(filters)
#         booleans_category = self.posters.category.str.lower().str.contains(filters)
#         return (booleans_author) | (booleans_title) | (booleans_category)

#     def get_filter_result(self, filter_str):
#         booleans_query = self.filter_by_text_input(filter_str)
#         booleans_time = self.posters.time.str.lower().str.contains(self.time)
#         booleans_location = self.posters.location.str.lower().str.contains(self.location)
#         booleans_category = self.posters.category.str.lower().str.contains(self.category)
#         booleans_result = (booleans_query) & (booleans_time) & (booleans_location) & (booleans_category)
#         return self.get_result_by_idx(booleans_result)

#     def pick_one(self):
#         n = len(self.posters)
#         idx = np.random.choice(n)
#         self.idx = idx
#         return self.get_result_by_idx(idx)["title"]

#     def filter_by_similarity(self, query_idx):
#         # query_idx = (self.posters[self.posters.title==query]).index
#         poster_idxs = self.corr[query_idx, :].argsort()[::-1][1 : n + 1]  # Top N exclude the paper itself
#         poster = self.posters.loc[poster_idxs]
#         result = pd.DataFrame()
#         result["Similarity Score"] = corr[query_idx, poster_idxs]
#         result = pd.concat([result, poster], axis=1)
#         return result
    
#     def get_result_by_idx(self, idxs):
#         # Filter Top n results
#         return self.posters.loc[idxs].iloc[: self.n]


# %%
# papers = [Paper(t,a) for t,a in zip(titles, authors)]
width = 10
st.image("imgs/neurips.png", use_column_width=True)
st.header("NeurIPS 2019")
st.text("Dec 8 - Dec 14")
st.header("Introduction")
st.markdown("> 1428, the number of accepted papers of NeurIPS in 2019.")

st.write(" ")
st.markdown(
    "It is impossible to scan all the papers, instead of going through the list, you can use this app to help you to find the paper you are interested."
)
st.markdown(
    "You can use the sidebar to search for interested paper by title or author, and get a list of top n similar papers. If you have no idea to start, just click the '__Feel Lucky__' button on the side, it will pick a paper for you and show the most similar results to you."
)
st.markdown("_Note: currently streamlit (this app is built with streamlit) do not have custom config for column width, so it will be a little bit weird when the text is long. I will fix this once they have implemented the feature._")

# %%
# filter = Filter(load_data(), corr)
posters = pd.read_csv("posters.csv")
# posters['author'] = posters['author'].str.replace("·", "")
del posters['event_type']
filter = Filter(posters, corr)

# Lucky Button
# %%
# filter.time = "All"
# assert filter._time == ""
# filter.location ="random"
# assert filter._location == "random"

# %%
# lucky_button = st.sidebar.button("Feel Lucky", "HI")
# if lucky_button:
#     filter.search_query = filter.pick_one()
# st.sidebar.text(lucky_button)

# %% [markdown]
# # Search query

# %% [markdown]
# # Sidebar

# %%
# Sidebar filter for time
time = filter.posters["time"].unique()
time.sort()
time = np.insert(time, 0, "All")
filter.time = st.sidebar.selectbox("Filter by time", time)

# Sidebar filter for venue
location = filter.posters["location"].unique()
location.sort()
location = np.insert(location, 0, "All")
filter.location = st.sidebar.selectbox("Filter by venue", location)

# Sidebar filter for category
category = filter.posters["category"].unique()
category.sort()
category = np.insert(category, 0, "All")
filter.category = st.sidebar.selectbox("Filter by category", category)

## Sidebar for Select Top N Results
top_n = [5, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)
filter.n = n

# %% [markdown]
# # Sidebar
# %%
filter.search_query = st.sidebar.text_input(
    "Search by title/author, use ',' to separate your crteria(s). For example, you can search 'jeff, dean'",
    filter.search_query
)

# Show extra columns
st.sidebar.text("Show Extra Columns:")
button_location = st.sidebar.checkbox("location")
button_time = st.sidebar.checkbox("time")
button_category = st.sidebar.checkbox("category")

# Reset button
# button_reset = st.sidebar.button("Reset", filter.reset())



# %% [markdown]
# # Filter Logic

# %%
# filter.search_query ="123,1234"
# assert filter._get_filters() == "(?=123)(?=1234)"

# filter.search_query="Shiyu chang" # case insensitive
# assert (filter.posters.author.str.lower().str.contains(filter._get_filters())).sum() > 0
# assert (filter.filter_by_text_input()).sum() > 0

# filter.location = " East Exhibition Hall B + C #1"
# assert filter.posters.location.str.contains(filter._location,regex=False).sum() > 0



# %%
def run():

    st.subheader("Your search result")
    filter.get_filter_result()

    def show_search_result(filter):
        try:
            result = filter.search_result.copy()
            if not button_location:
                del result['location']
            if not button_time:
                del result['time']
            if not button_category:
                del result['category']
            st.table(result)
        except:
            search_result = pd.DataFrame()
            st.write("No search result :(")

    show_search_result(filter)
    # %%
    st.subheader(f"Your top search result is:")
    # search_result = filter.get_filter_result()

    # %%
    # # Debug only
    # filter.reset()
    # booleans_query = filter.filter_by_text_input()
    # booleans_time = filter.posters.time.str.lower().str.contains(filter.time, regex=False)
    # booleans_location = filter.posters.location.str.lower().str.contains(filter.location, regex=False)
    # booleans_category = filter.posters.category.str.lower().str.contains(filter.category, regex=False)
    # booleans_result = (booleans_query) & (booleans_time) & (booleans_location) & (booleans_category)
    # assert booleans_result.sum() > 0

    # %%
    if not filter.search_result.empty:
        st.markdown(f"__{filter.search_result.iloc[0].title}__")
        # st.write(search_result.head(1).index.values[0])
        st.write(
            f"The Top {filter.n} similar posters to this are:")
        result = filter.filter_by_similarity(filter.search_result)
        if not button_location:
            del result['location']
        if not button_time:
            del result['time']
        if not button_category:
            del result['category']
        st.table(result)
    else:
        st.markdown(
            f"No matched records, try modify your search query _ {filter.search_query}_or clean up the filter"
        )

run()

# %%
if DEBUG:
    st.sidebar.text("DEBUG")
    st.sidebar.text(f"top_n: {filter.n}")
    st.sidebar.text(f"search_query: {filter.search_query}")
    st.sidebar.text(f"location {filter.location} ")
    st.sidebar.text(f"category {filter.category}")
    st.sidebar.text(f"time {filter.time}")
    st.sidebar.text(f"button_location {button_location}")

st.markdown(f"GitHub: https://github.com/noklam/NeurIPS2019Exploration")

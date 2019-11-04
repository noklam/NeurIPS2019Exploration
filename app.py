# %%
# %load_ext autoreload
# %autoreload 2

# %%
global DEBUG
DEBUG = False
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
    if DEBUG:
        posters = pd.read_csv("posters_debug.csv")
    else:
        posters = pd.read_csv("posters.csv")

    del posters['event_type']
    return posters

# %%
# GA Traffic
ga = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-83544344-6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-83544344-6');
</script>
"""
# st.markdown(ga, unsafe_allow_html=True)


width = 10
st.image("imgs/neurips.png", use_column_width=True)
st.title("NeurIPS 2019 Explorer")
st.text("Dec 8 - Dec 14")
st.header("Introduction")
st.markdown("> 1428, the number of accepted papers of NeurIPS in 2019.")

st.write(" ")
st.markdown(
    "With only 1 month from NeurIPS, it is impossible to scan all the papers. Instead of going through the list, you can use this app to help you to find the paper you are interested."
)
st.markdown(
    "You can use the sidebar to search for interested paper by title or author, and get a list of top n similar papers. If you have no idea to start, just click the '__Feel Lucky__' button on the side, it will pick a paper for you and show the most similar results to you."
)

# %%
# filter = Filter(load_data(), corr)
# posters = pd.read_csv("posters.csv")
# posters['author'] = posters['author'].str.replace("·", "")
# del posters['event_type']
filter = Filter(load_data(), corr)

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
# Info
st.sidebar.header("About App")
st.sidebar.info("A Simple search engine for NeurIPS 2019")

# %%
# Sidebar filter for time
time = filter.posters["time"].unique()
# time.sort()
time = np.insert(time, 0, "All")
filter.time = st.sidebar.selectbox("Filter by time", time)

# Sidebar filter for venue
# location = filter.posters["location"].unique()
# location.sort()
# location = np.insert(location, 0, "All")
# filter.location = st.sidebar.selectbox("Filter by venue", location)

# Sidebar filter for category
category = filter.posters["category"].unique()
category.sort()
category = np.insert(category, 0, "All")
filter.category = st.sidebar.selectbox("Filter by category", category)

# Sidebar filter for category
sub_category = filter.posters[filter.posters['category'].str.lower().str.contains(filter.category)]["sub_category"].unique()
sub_category.sort()
sub_category = np.insert(sub_category, 0, "All")
filter.sub_category = st.sidebar.selectbox("Filter by sub-category", sub_category)

## Sidebar for Select Top N Results
top_n = [10, 10, 15, 20]
n = st.sidebar.selectbox("Show Top N Result", top_n)
filter.n = n





# %% [markdown]
# # Sidebar
# %%
st.sidebar.header("Search by text")
filter.searh_qeury2 = st.sidebar.multi
filter.search_query = st.sidebar.text_input(
    "Search by title/author, use ',' to separate your crteria(s). For example, you can search 'jeff, dean'",
    filter.search_query
)

# Show extra columns
st.sidebar.text("Show Extra Columns:")
# button_location = st.sidebar.checkbox("location")
button_location = False
button_time = st.sidebar.checkbox("time")
button_category = st.sidebar.checkbox("category")
button_sub_category = st.sidebar.checkbox("sub_category")
button_link = st.sidebar.checkbox("link")

# Lucky button
button_lucky = st.sidebar.button("Lucky!")

# Warning
st.sidebar.warning("_Note: Currently the rendering of dataframe is a bit weird as no config can be set with streamlit. Once they have introduce the configuration I will fix the issue_")


# Info
st.sidebar.text("Built with Streamlit")
st.sidebar.text("Maintained by @noklam")
st.sidebar.text("I use GA to track the web traffic of the site")



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


    if button_lucky:
        st.subheader("Your paper lottery result")
        filter.feel_lucky()
    else:
        st.subheader("Your search result")
        filter.get_filter_result()

    def show_search_result(filter, button_lucky):
        try:
            if button_lucky:
                result = filter.search_result
            else:
                result = filter.search_result.copy()
            if not button_location:
                del result['location']
            if not button_time:
                del result['time']
            if not button_category:
                del result['category']
            if not button_sub_category:
                del result['sub_category']
            if not button_link:
                del result['link'], result['poster'], result['slides'], result['video']
            # st.write(result.to_html(scape=False, index=False),unsafe_allow_html=True)
            # result.to_html(scape=False, index=False)
            st.write(result.to_html(index=False),unsafe_allow_html=True)
        except:
            search_result = pd.DataFrame()
            st.table("No search result :(")
    
    show_search_result(filter, button_lucky)
    # %%tfilter
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
        if not button_sub_category:
            del result['sub_category']
        if not button_link:
            del result['link'], result['poster'], result['slides'], result['video']
        # st.table(result)
        st.write(result.to_html(index=False),unsafe_allow_html=True)
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
    st.sidebar.text(f"{filter.category, filter.posters.shape, filter.corr.shape}")


st.markdown("If you found bugs or have any suggestion, please let me know.")
st.markdown(f"GitHub: https://github.com/noklam/NeurIPS2019Exploration")

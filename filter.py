import pandas as pd

class Filter:
    def __init__(self, posters, corr):
        self.posters = posters
        self.corr = corr
        self.search_query = ""
        self.n = 5
        self._location = ""
        self._time=""
        self._category=""
        self._sub_category=""
        self.search_result=""

    def reset(self):
        self._location = ""
        self._time = ""
        self._category = ""
        self._sub_category = ""
        self.search_query=""

    def _get_filters(self):
        filter_str = self.search_query
        if not filter_str:
            return ""
        filters = filter_str.lower().split(",")
        # print("".join([f"(?={filter})" for filter in filters]))
        return "".join([f"(?={filter})" for filter in filters])

    def filter_by_text_input(self):
        filters = self._get_filters()
        booleans_author = self.posters.author.str.lower().str.contains(filters)
        booleans_title = self.posters.title.str.lower().str.contains(filters)
        # booleans_category = self.posters.category.str.lower().str.contains(filters)
        return (booleans_author) | (booleans_title) 
    
    def get_filter_result(self):
        booleans_query = self.filter_by_text_input()
        booleans_time = self.posters.time.str.lower().str.contains(self.time, regex=False)
        booleans_location = self.posters.location.str.lower().str.contains(self.location, regex=False)
        booleans_category = self.posters.category.str.lower().str.contains(self.category, regex=False)
        booleans_sub_category = self.posters.category.str.lower().str.contains(self.sub_category, regex=False)
        booleans_result = (booleans_query) & (booleans_time) & (booleans_location) & (booleans_category) & (booleans_sub_category)
        return self.get_result_by_idx(booleans_result)
        
    def get_result_by_idx(self, idxs):
        # Filter Top n results
        result = self.posters.loc[idxs].iloc[: self.n]
        self.search_result = result
        return self.search_result

    def filter_by_similarity(self, search_result):
        if search_result.empty:
            return
        query_idx = search_result.index[0]
        poster_idxs = self.corr[query_idx, :].argsort()[::-1][1: self.n + 1]  # Top N exclude the paper itself
        result = self.posters.iloc[poster_idxs]
        result["Similarity Score"] = self.corr[query_idx, poster_idxs]
        cols = result.columns.values.tolist()
        cols.insert(0, cols.pop())
        result = result.reindex(columns= cols)
        return result

    @property
    def location(self):
        return self._location
    @property
    def time(self):
        return self._time
    @property
    def category(self):
        return self._category
    @property
    def sub_category(self):
        return self._sub_category
    @location.setter
    def location(self, x):
        if x=="All":
            self._location=""
        else:
            self._location=x.lower()
    @time.setter
    def time(self, x):
        if x=="All":
            self._time=""
        else:
            self._time=x.lower()
    @category.setter
    def category(self, x):
        if x=="All":
            self._category=""
        else:
            self._category=x.lower()

    @category.setter
    def sub_category(self, x):
        if x=="All":
            self._sub_category=""
        else:
            self._sub_category=x.lower()
    def feel_lucky(self):
        self.search_result=self.posters.sample(n=1)
        print('Feeling Lucky!!')
        return "test"
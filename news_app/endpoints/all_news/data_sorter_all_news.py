import datetime

from news_app.endpoints.support.abstract_sorters import ABSSorter
from news_app.models.internal.news import NewsItem
from news_app.models.response.all_news_response.news_listed import NewsResponse


class DataSorter(ABSSorter):
    def make_news_list(self):
        self._convert_data()
        self._map_comments()
        response_model = self._fill_response_model()

        return response_model

    def _fill_response_model(self):
        response_news_model = NewsResponse()

        current_dt = datetime.datetime.now()
        for single_news in self.news_dict.values():
            if self._check_conditions(single_news, current_dt):
                response_news = single_news.to_response_model_all_news()
                response_news_model.news.append(response_news)

        response_news_model.sort_news_by_date()
        response_news_model.count_news()

        return response_news_model

    def _check_conditions(self, single_news: NewsItem, current_dt: datetime.datetime):
        if single_news.deleted:
            return False
        if single_news.date > current_dt:
            return False

        return True

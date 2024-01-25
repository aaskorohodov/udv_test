import datetime
from typing import Optional

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem
from news_app.models.response.news_listed import NewsResponse, NewsItemResponse


class DataSorter:
    def __init__(self, comments_and_news: dict):
        self.comments_list: list[CommentItem] = comments_and_news['comments']
        self.news_list: list[NewsItem] = comments_and_news['news']
        self.comments_dict: Optional[dict[int, CommentItem]] = {}
        self.news_dict: Optional[dict[int, NewsItem]] = {}

    def make_news_list(self):
        self._convert_data()
        self._map_comments()
        response_model = self._fill_response_model()

        return response_model

    def _convert_data(self):
        for comment in self.comments_list:
            self.comments_dict[comment.id] = comment

        for news in self.news_list:
            self.news_dict[news.id] = news

    def _map_comments(self):
        for comment in self.comments_dict.values():
            if comment.id in self.news_dict:
                single_news = self.news_dict[comment.news_id]
                single_news.comments.append(comment)

    def _fill_response_model(self):
        response_news_model = NewsResponse()

        current_dt = datetime.datetime.now()
        for single_news in self.news_dict.values():
            if self._check_conditions(single_news, current_dt):
                response_news = single_news.to_response_model()
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

from typing import Optional

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class ABSSorter:
    def __init__(self, comments_and_news: dict):
        self.comments_list: list[CommentItem] = comments_and_news['comments']
        self.news_list: list[NewsItem] = comments_and_news['news']
        self.comments_dict: Optional[dict[int, CommentItem]] = {}
        self.news_dict: Optional[dict[int, NewsItem]] = {}

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

        for single_news in self.news_dict.values():
            single_news.sort_comments_by_date()

from datetime import datetime
from typing import List
from pydantic import BaseModel


class NewsItemResponse(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    deleted: bool
    comments_count: int


class NewsResponse(BaseModel):
    news: List[NewsItemResponse] = []
    news_count: int = 0

    def sort_news_by_date(self):
        self.news.sort(key=lambda x: x.date, reverse=True)

    def count_news(self):
        self.news_count = len(self.news)

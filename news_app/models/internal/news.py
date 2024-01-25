from datetime import datetime

from pydantic import BaseModel

from news_app.models.internal.comments import CommentItem
from news_app.models.response.all_news_response.news_listed import NewsItemResponse
from news_app.models.response.news_by_id_response.specific_news import SpecificNews


class NewsItem(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    deleted: bool
    comments: list[CommentItem] = []

    def sort_comments_by_date(self):
        self.comments.sort(key=lambda x: x.date, reverse=True)

    def to_response_model_all_news(self) -> NewsItemResponse:
        return NewsItemResponse(
            id=self.id,
            title=self.title,
            date=self.date,
            body=self.body,
            deleted=self.deleted,
            comments_count=len(self.comments)
        )

    def to_response_model_news_by_id(self) -> SpecificNews:
        specific_news_response = SpecificNews(
            id=self.id,
            title=self.title,
            date=self.date,
            body=self.body,
            deleted=self.deleted,
            comments=[],
            comments_count=len(self.comments)
        )
        for comment in self.comments:
            specific_news_response.comments.append(comment.to_response_model_news_by_id())

        return specific_news_response

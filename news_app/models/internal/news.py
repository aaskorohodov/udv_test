from datetime import datetime

from pydantic import BaseModel

from news_app.models.internal.comments import CommentItem
from news_app.models.response.news_listed import NewsItemResponse


class NewsItem(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    deleted: bool
    comments: list[CommentItem] = []

    def sort_comments_by_date(self):
        self.comments.sort(key=lambda x: x.date, reverse=True)

    def to_response_model(self) -> NewsItemResponse:
        return NewsItemResponse(
            id=self.id,
            title=self.title,
            date=str(self.date),
            body=self.body,
            deleted=self.deleted,
            comments_count=len(self.comments)
        )

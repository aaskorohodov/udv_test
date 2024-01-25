from datetime import datetime

from pydantic import BaseModel

from news_app.models.response.news_by_id_response.specific_news import CommentItemResponse


class CommentItem(BaseModel):
    id: int
    news_id: int
    title: str
    date: datetime
    comment: str

    def to_response_model_news_by_id(self) -> CommentItemResponse:
        return CommentItemResponse(
            id=self.id,
            news_id=self.news_id,
            title=self.title,
            date=self.date,
            comment=self.comment
        )

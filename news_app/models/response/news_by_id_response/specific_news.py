from datetime import datetime

from pydantic import BaseModel


class CommentItemResponse(BaseModel):
    id: int
    news_id: int
    title: str
    date: datetime
    comment: str


class SpecificNews(BaseModel):
    id: int
    title: str
    date: datetime
    body: str
    deleted: bool
    comments: list[CommentItemResponse] = []
    comments_count: int = 0

from datetime import datetime

from pydantic import BaseModel


class CommentItem(BaseModel):
    id: int
    news_id: int
    title: str
    date: datetime
    comment: str

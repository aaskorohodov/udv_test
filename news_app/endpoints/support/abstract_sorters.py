from typing import Optional, TypedDict, List

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class CommentsAndNewsDict(TypedDict):
    """Словарь с новостями и комментариями в сыром виде"""

    comments: List[CommentItem]
    news: List[NewsItem]


class ABSSorter:
    """Базовый класс для обработки сырых данных с новостями и комментариями. Хранит общие методы

    Attributes:
        comments_list: Список сырых комментариев
        news_list: Список сырых новостей
        comments_dict: Словарь вида [comment_id: CommentItem]
        news_dict: Словарь вида [news_id: NewsItem]"""

    def __init__(self, comments_and_news: CommentsAndNewsDict):
        """Раскладывает входные данные по коллекциям с новостями и комментариями

        Args:
            comments_and_news: Сырые данные с новостями и комментариями, полученные из 'базы'"""

        self.comments_list: list[CommentItem] = comments_and_news['comments']
        self.news_list: list[NewsItem] = comments_and_news['news']
        self.comments_dict: Optional[dict[int, CommentItem]] = {}
        self.news_dict: Optional[dict[int, NewsItem]] = {}

    def _convert_data(self) -> None:
        """Превращает списки с новостями и комментариями в словари вида [id: Model]"""

        for comment in self.comments_list:
            self.comments_dict[comment.id] = comment

        for news in self.news_list:
            self.news_dict[news.id] = news

    def _map_comments(self) -> None:
        """Складывает комментарии в новости (Nested Model) и сортируем комментарии по дате в рамках новости"""

        for comment in self.comments_dict.values():
            if comment.id in self.news_dict:
                single_news = self.news_dict[comment.news_id]
                single_news.comments.append(comment)

        for single_news in self.news_dict.values():
            single_news.sort_comments_by_date()

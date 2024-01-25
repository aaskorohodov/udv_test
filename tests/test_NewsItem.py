import datetime
import random
import time
import unittest

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem
from news_app.models.response.all_news_response.news_listed import NewsItemResponse
from news_app.models.response.news_by_id_response.specific_news import SpecificNews, CommentItemResponse


class TestNewsItem(unittest.TestCase):
    """Тестирует NewsItem"""

    def setUp(self) -> None:
        """Создаем NewsItem и наполняем его 100 штуками CommentItem, каждый с разным временем"""

        self.news_item = NewsItem(
            id=1,
            title='t1',
            date=datetime.datetime.now(),
            body='text',
            deleted=False,
            comments=[],
        )

        for i in range(100):
            ci = CommentItem(
                id=i,
                news_id=1,
                title=f't{i}',
                date=datetime.datetime.now(),
                comment=f'comment {i}',
            )
            self.news_item.comments.append(ci)
            time.sleep(0.01)  # Чтобы время каждого CommentItem отличалось

        # Перемешиваем, чтобы комментарии стояли не по порядку их времени
        random.shuffle(self.news_item.comments)

    def test_sort_comments_by_date(self):
        """Проверяем, что комментарии отсортированы по времени"""

        self.news_item.sort_comments_by_date()

        last_known_dt = None
        for comment in self.news_item.comments:
            if last_known_dt:
                self.assertGreater(last_known_dt, comment.date)
            last_known_dt = comment.date

    def test_to_response_model_all_news(self):
        """Проверяем, что NewsItem корректно превращается в NewsItemResponse"""

        news_item_response = self.news_item.to_response_model_all_news()
        self.assertIsInstance(news_item_response, NewsItemResponse)

        self.assertEqual(news_item_response.id, self.news_item.id)
        self.assertEqual(news_item_response.title, self.news_item.title)
        self.assertEqual(news_item_response.date, self.news_item.date)
        self.assertEqual(news_item_response.body, self.news_item.body)
        self.assertEqual(news_item_response.deleted, self.news_item.deleted)
        self.assertEqual(news_item_response.comments_count, len(self.news_item.comments))

    def test_to_response_model_news_by_id(self):
        """Проверяем, что NewsItem корректно превращается в SpecificNews"""

        specific_news = self.news_item.to_response_model_news_by_id()
        self.assertIsInstance(specific_news, SpecificNews)

        self.assertEqual(specific_news.id, self.news_item.id)
        self.assertEqual(specific_news.title, self.news_item.title)
        self.assertEqual(specific_news.date, self.news_item.date)
        self.assertEqual(specific_news.body, self.news_item.body)
        self.assertEqual(specific_news.deleted, self.news_item.deleted)
        self.assertEqual(specific_news.comments_count, len(self.news_item.comments))

        # Проверяем, что каждый комментарий превращается в CommentItemResponse
        for el in specific_news.comments:
            self.assertIsInstance(el, CommentItemResponse)


if __name__ == '__main__':
    unittest.main()

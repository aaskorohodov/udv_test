import datetime
import unittest

from news_app.models.internal.comments import CommentItem
from news_app.models.response.news_by_id_response.specific_news import CommentItemResponse


class TestMyShinyDBReader(unittest.TestCase):
    """Тестирует MyShinyDBReader"""

    def setUp(self) -> None:
        """Создаем CommentItem"""

        self.comment_item = CommentItem(
            id=123,
            news_id=321,
            title='some title',
            date=datetime.datetime(year=2024, month=1, day=2, hour=3, minute=4, second=5, microsecond=123456),
            comment='some comment'
        )

    def test_to_response_model_news_by_id(self):
        """Проверяем, что CommentItem.to_response_model_news_by_id() создает что мы ожидаем и не теряет данные"""

        comment_item_response = self.comment_item.to_response_model_news_by_id()

        self.assertIsInstance(comment_item_response, CommentItemResponse)

        self.assertEqual(self.comment_item.id, comment_item_response.id)
        self.assertEqual(self.comment_item.news_id, comment_item_response.news_id)
        self.assertEqual(self.comment_item.title, comment_item_response.title)
        self.assertEqual(self.comment_item.date, comment_item_response.date)
        self.assertEqual(self.comment_item.comment, comment_item_response.comment)


if __name__ == '__main__':
    unittest.main()

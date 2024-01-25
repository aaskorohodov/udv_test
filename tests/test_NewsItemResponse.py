from datetime import datetime

import random
import time
import unittest

from news_app.models.response.all_news_response.news_listed import NewsResponse, NewsItemResponse


class TestNewsResponse(unittest.TestCase):
    """Тестирует NewsResponse"""

    def setUp(self) -> None:
        """Создает NewsResponse и наполняет его данными (NewsItemResponse в количестве 100 штук с разной DT)"""

        self.news_response_model = NewsResponse()

        # Создаем 100 штук новостей, выжидая паузу между каждой, чтобы дата отличалась
        for i in range(100):
            dt = datetime.now()
            news_item_response_model = NewsItemResponse(
                id=i,
                title=f't_1',
                date=dt,
                body=f'Text_{i}',
                deleted=False,
                comments_count=0
            )
            self.news_response_model.news.append(news_item_response_model)
            time.sleep(0.01)

        # Перемешиваем список новостей, чтобы дата не стояла по возрастанию
        random.shuffle(self.news_response_model.news)

    def test_sort_news_by_date(self):
        """Проверяет, что сортировка по дате работает"""

        self.news_response_model.sort_news_by_date()

        last_known_time = None
        for news_item_response_model in self.news_response_model.news:
            if last_known_time:
                self.assertGreater(last_known_time, news_item_response_model.date)
            last_known_time = news_item_response_model.date

    def test_count_news(self):
        """Проверяем, что счетчик новостей выдает корректное число"""

        self.news_response_model.count_news()
        self.assertEqual(100, self.news_response_model.news_count)


if __name__ == '__main__':
    unittest.main()

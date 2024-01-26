import datetime
import time
import unittest

from news_app.endpoints.all_news.data_sorter_all_news import DataSorter
from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem
from news_app.models.response.all_news_response.news_listed import NewsItemResponse


class TestDataSorter(unittest.TestCase):
    """Тестируем DataSorter"""

    def setUp(self) -> None:
        """Создаем несколько новостей и комментариев для тестирования"""

        self.comments_and_news = {
            'comments': [],
            'news': []
        }

        for i in range(100):
            ci = CommentItem(
                id=i,
                news_id=1,
                title=f't{i}',
                date=datetime.datetime.now(),
                comment=f'comment {i}',
            )
            self.comments_and_news['comments'].append(ci)
            time.sleep(0.01)  # Чтобы время каждого CommentItem отличалось
        for i in range(100):
            ci = CommentItem(
                id=i,
                news_id=2,
                title=f't{i}',
                date=datetime.datetime.now(),
                comment=f'comment {i}',
            )
            self.comments_and_news['comments'].append(ci)
            time.sleep(0.01)  # Чтобы время каждого CommentItem отличалось
        for i in range(100):
            ci = CommentItem(
                id=i,
                news_id=3,
                title=f't{i}',
                date=datetime.datetime.now(),
                comment=f'comment {i}',
            )
            self.comments_and_news['comments'].append(ci)
            time.sleep(0.01)  # Чтобы время каждого CommentItem отличалось

        ni = NewsItem(
            id=1,
            title='t1',
            date=datetime.datetime.now(),
            body='text',
            deleted=False,
            comments=[],
        )
        self.comments_and_news['news'].append(ni)
        time.sleep(0.01)
        ni2 = NewsItem(
            id=2,
            title='t2',
            date=datetime.datetime.now(),
            body='text',
            deleted=False,
            comments=[],
        )
        self.comments_and_news['news'].append(ni2)
        time.sleep(0.01)
        ni3 = NewsItem(
            id=3,
            title='t3',
            date=datetime.datetime.now(),
            body='text',
            deleted=True,
            comments=[],
        )
        self.comments_and_news['news'].append(ni3)
        time.sleep(0.01)
        ni4 = NewsItem(
            id=4,
            title='t4',
            date=datetime.datetime(year=2050, month=1, day=1, hour=1, minute=1),
            body='text',
            deleted=False,
            comments=[],
        )
        self.comments_and_news['news'].append(ni4)

        ni5 = NewsItem(
            id=5,
            title='t5',
            date=datetime.datetime.now(),
            body='text',
            deleted=False,
            comments=[],
        )
        self.comments_and_news['news'].append(ni5)
        time.sleep(0.01)
        ni6 = NewsItem(
            id=6,
            title='t6',
            date=datetime.datetime.now(),
            body='text',
            deleted=False,
            comments=[],
        )
        self.comments_and_news['news'].append(ni6)
        time.sleep(0.01)

        self.sorter = DataSorter(self.comments_and_news)

    def test_all(self):
        """Проверяем, что в возвращенной модели все так, как мы ожидаем"""

        result = self.sorter.make_news_list()

        # Проверяем, что новости превращены в подходящую к отправке модель
        for news in result.news:
            self.assertIsInstance(news, NewsItemResponse)

        # Проверяем, что всего в отправку попало 4 новости (минус 1 с датой в будущем и минус 1 deleted=True)
        self.assertEqual(len(result.news), 4)

        # Проверяем, что новости отсортированы по дате
        last_known_dt = None
        for news in result.news:
            if last_known_dt:
                self.assertGreater(last_known_dt, news.date)
            last_known_dt = news.date

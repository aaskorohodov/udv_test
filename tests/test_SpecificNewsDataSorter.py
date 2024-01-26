import datetime
import time
import unittest

from fastapi import HTTPException

from news_app.endpoints.news_by_id.data_sorter_specific_news import SpecificNewsDataSorter
from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class TestSpecificNewsDataSorter(unittest.TestCase):
    """Тестируем SpecificNewsDataSorter"""

    def setUp(self) -> None:
        """Создаем 2 новости и 100 разных комментариев к каждой"""

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

        self.sorter = SpecificNewsDataSorter(self.comments_and_news)

    def test_check_news_is_ok(self):
        """Проверяем, что поднимаются исключения и что они содержат корректный ситуации текст"""

        # Запускаем сортировку
        self.sorter.get_specific_news(1)

        # Просим новость, которой нет в коллекции
        news_id_that_is_not_there = 100500
        # Use assertRaises to check if the expected exception is raised
        with self.assertRaises(HTTPException) as context:
            self.sorter._check_news_is_ok(news_id_that_is_not_there)
        expected_msg = f'404: No such news with id {news_id_that_is_not_there} found in our shiny DB!\n'
        self.assertEqual(expected_msg, str(context.exception))

        # Просим удаленную новость
        first_news = self.sorter.news_dict.get(1)
        first_news.deleted = True
        with self.assertRaises(HTTPException) as context:
            self.sorter._check_news_is_ok(1)
        expected_msg = f'404: News with id {1} was deleted! We are very sorry.\n'
        self.assertEqual(expected_msg, str(context.exception))

        # Просим новость из будущего
        second_news = self.sorter.news_dict.get(2)
        future_dt = datetime.datetime(year=2050, month=1, day=1, hour=1, minute=1)
        second_news.date = future_dt
        with self.assertRaises(HTTPException) as context:
            self.sorter._check_news_is_ok(2)
        expected_msg = f'404: News with id {2} is not ready for publication yet, but it will be on ' \
                       f'{future_dt.__str__()}, wait a bit please!\n'
        self.assertEqual(expected_msg, str(context.exception))


if __name__ == '__main__':
    unittest.main()

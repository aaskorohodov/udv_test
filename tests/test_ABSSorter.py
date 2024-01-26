import datetime
import time
import unittest

from news_app.endpoints.support.abstract_sorters import ABSSorter
from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class TestABSSorter(unittest.TestCase):
    """Тестируем Базовый класс-сортировщик"""

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

        self.sorter = ABSSorter(self.comments_and_news)

    def test_init(self):
        """Проверяем, что новости и комментарии раскладываются туда, куда мы ожидаем"""

        # Разложили по своим коллекциям
        self.assertEqual(self.sorter.comments_list, self.comments_and_news['comments'])
        self.assertEqual(self.sorter.news_list, self.comments_and_news['news'])

        # Разложили то, что ожидали (не перепутали)
        for el in self.sorter.comments_list:
            self.assertIsInstance(el, CommentItem)
        for el in self.sorter.news_list:
            self.assertIsInstance(el, NewsItem)

        # Прочие коллекции оставили пустыми
        self.assertFalse(self.sorter.comments_dict)
        self.assertFalse(self.sorter.news_dict)

    def test_convert_data(self):
        """Проверяем, как сортировщик раскладывает сырые данные по словарям"""

        self.sorter._convert_data()

        for news_id, news_item in self.sorter.news_dict.items():
            self.assertEqual(news_id, news_item.id)
            self.assertIsInstance(news_item, NewsItem)

        for comment_id, comment_item in self.sorter.comments_dict.items():
            self.assertEqual(comment_id, comment_item.id)
            self.assertIsInstance(comment_item, CommentItem)

    def test_map_comments(self):
        """Проверяем, корректно ли комментарии кладутся в новости (к коректным новостям)"""

        self.sorter._map_comments()

        for news_item in self.sorter.news_dict.values():
            overall_comments_number = 0  # Сколько всего комментариев. Ожидаем 100, потому что сделали 100
            previous_known_dt = None     # Время последнего комментария. Чтобы проверить, что они отсортированы
            for comment in news_item.comments:
                overall_comments_number += 1
                self.assertIsInstance(comment, CommentItem)
                if previous_known_dt:
                    self.assertGreater(previous_known_dt, comment.date)
                previous_known_dt = comment.date
            self.assertEqual(overall_comments_number, 100)


if __name__ == '__main__':
    unittest.main()

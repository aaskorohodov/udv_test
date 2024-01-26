import asyncio
import datetime
import json
import os
import unittest

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem
from news_app.utils.db_reader import MyShinyDBReader


class TestMyShinyDBReader(unittest.IsolatedAsyncioTestCase):
    """Тестирует MyShinyDBReader"""

    def setUp(self) -> None:
        os.environ['DB_FOLDER_NAME'] = 'fixtures'
        os.environ['COMMENTS_PATH'] = 'comments.json'
        os.environ['NEWS_PATH'] = 'news.json'

        self.comments_path = 'comments.json'
        self.news_path = 'news.json'

        self.db_reader = MyShinyDBReader()

        # Затыкаем нежелательный метод, чтобы получать путь к фикстурам при тестировании
        self.db_reader._get_path_to_db_file = self.mock_for_get_path_to_db_file

    def mock_for_get_path_to_db_file(self, file_name: str) -> str:
        """Mock для метода MyShinyDBReader._get_path_to_db_file() чтобы он возвращал путь к фикстурам"""

        module_dir = os.path.dirname(os.path.abspath(__file__))
        fixtures_path = os.path.join(module_dir, 'fixtures')
        file_path = os.path.join(fixtures_path, file_name)

        return file_path

    def test_env_been_read(self):
        """Проверяет, что MyShinyDBReader умеет читать переменные окружения"""

        os.environ['DB_FOLDER_NAME'] = 'fixtures'
        os.environ['COMMENTS_PATH'] = 'comments.json'
        os.environ['NEWS_PATH'] = 'news.json'
        db_reader = MyShinyDBReader()

        self.assertEqual(db_reader._db_folder_name, 'fixtures')
        self.assertEqual(db_reader._comments_path, 'comments.json')
        self.assertEqual(db_reader._news_path, 'news.json')

    def test_read_jsons(self):
        """Проверяет, что MyShinyDBReader корректно читает json"""

        comments_from_db_reader = self.db_reader._read_json(self.comments_path)
        news_from_db_reader = self.db_reader._read_json(self.news_path)

        path_to_comments_from_fixtures = self.mock_for_get_path_to_db_file(self.comments_path)
        with open(path_to_comments_from_fixtures, 'r') as f:
            comments_from_fixtures = json.load(f)

        path_to_news_from_fixtures = self.mock_for_get_path_to_db_file(self.news_path)
        with open(path_to_news_from_fixtures, 'r') as f:
            news_from_fixtures = json.load(f)

        self.assertEqual(comments_from_fixtures, comments_from_db_reader)
        self.assertEqual(news_from_fixtures, news_from_db_reader)

    def test_create_models_from_list(self):
        """Проверяем, что MyShinyDBReader умеет превращать данные в модели, и делает это корректно"""

        raw_data = [
            {
                "id": 1,
                "news_id": 1,
                "title": "comment_1",
                "date": "2019-01-02T21:58:25",
                "comment": "Comment text 1"
            },
            {
                "id": 2,
                "news_id": 1,
                "title": "comment_2",
                "date": "2020-01-02T21:58:25",
                "comment": "Comment text 2"
            }
        ]
        expected_result = [
            CommentItem(
                id=1,
                news_id=1,
                title="comment_1",
                date=datetime.datetime(2019, 1, 2, 21, 58, 25),
                comment="Comment text 1"
            ),
            CommentItem(
                id=2,
                news_id=1,
                title="comment_2",
                date=datetime.datetime(2020, 1, 2, 21, 58, 25),
                comment="Comment text 2"
            ),
        ]
        result = asyncio.run(self.db_reader._create_models_from_list(raw_data, CommentItem))
        self.assertIsInstance(result, list)
        for el in result:
            self.assertIsInstance(el, CommentItem)
        self.assertEqual(expected_result, result)

    def test_read_news(self):
        """Проверяем, что db_reader._read_news() возвращает модели NewsItem"""

        result = asyncio.run(self.db_reader._read_news())
        self.assertNotEqual(0, len(result))
        for el in result:
            self.assertIsInstance(el, NewsItem)

    async def test_read_comments(self):
        """Проверяем, что db_reader._read_comments возвращает модели CommentItem"""

        result = await self.db_reader._read_comments()
        self.assertNotEqual(0, len(result))
        for el in result:
            self.assertIsInstance(el, CommentItem)

    def test_read_news_and_comments(self):
        """"""

        result = asyncio.run(self.db_reader.read_news_and_comments())
        self.assertEqual(2, len(result))

        comments = result.get('comments')
        news = result.get('news')
        self.assertTrue(comments)
        self.assertTrue(news)

        for el in comments:
            self.assertIsInstance(el ,CommentItem)
        for el in news:
            self.assertIsInstance(el, NewsItem)


if __name__ == '__main__':
    unittest.main()

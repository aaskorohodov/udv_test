import asyncio
import json
import os

from pydantic import ValidationError, BaseModel

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class MyShinyDBReader:
    """Имитирует подключение к DB. Вместо DB читает json'ы.

    Notes:
        Предполагается, что DB всегда возвращает то, что задано в условиях задачи – неизмененное содержание двух json.
        Кажется, что в боевых условиях, можно было бы прочитать комментарии и новости сразу, подходящим SQL-запросом.

        НО ЭТОТ ИМИТАТОР КОННЕКТОРА БУДЕТ ПРОСТО ЧИТАТЬ ФАЙЛЫ, non-async."""

    def __init__(self):
        """Читает пути до файлов-json из переменных окружения"""

        self._db_folder_name: str = os.environ.get('DB_FOLDER_NAME')
        self._comments_path: str = os.environ.get('COMMENTS_PATH')
        self._news_path: str = os.environ.get('NEWS_PATH')

    async def read_news_and_comments(self) -> dict[str, list[CommentItem], str,  list[NewsItem]]:
        """Имитирует выполнение двух запросов к DB на получение комментариев и новостей.

        Notes:
            Имитируя запросы к базе, делает из параллельно, т.к. при чтении из базы это было бы обосновано.
        Returns:
            Dict с двумя ключами, под каждым из которых список с комментариями и новостями (Модели)."""

        comments, news = await asyncio.gather(
            self._read_comments(),
            self._read_news()
        )

        return {'comments': comments, 'news': news}

    async def _read_comments(self) -> list[CommentItem]:
        """Читает файл с комментариями и формирует из него модели

        Returns:
            Список с моделями комментариев (внутренние модели, Data-классы)"""

        comments_dict = self._read_json(self._comments_path)['comments']
        comments_models = self._create_models_from_list(comments_dict, CommentItem)

        # noinspection PyTypeChecker
        return comments_models

    async def _read_news(self) -> list[NewsItem]:
        """Читает файл с новостями и формирует из него модели

        Returns:
            Список с моделями новостей (внутренние модели, Data-классы)"""

        news_dict = self._read_json(self._news_path)['news']
        news_models = self._create_models_from_list(news_dict, NewsItem)

        # noinspection PyTypeChecker
        return news_models

    def _create_models_from_list(self, raw_data: list[dict], base_model: type[BaseModel]) -> list[BaseModel]:
        """Превращает переданный список словарей в желаемую (переданную) модель

        Пропускает всё, что не может превратить в модель. Потому что в raw_data есть news_count и comments_count

        Args:
            raw_data: Список словарей, где словари представляют модели
            base_model: Ссылка на класс модели, в которые надо превратить переданные словари
        Returns:
            Список с моделями"""

        result = []
        for raw_dict in raw_data:
            try:
                model = base_model.model_validate(raw_dict)
                result.append(model)
            except ValidationError:
                pass

        return result

    def _read_json(self, file_name: str) -> dict:
        """Читает json по переданному пути

        Args:
            file_name: Путь к файлу с json
        Returns:
            Словарь, прочитанный из файла"""

        db_file_path = self._get_path_to_db_file(file_name)

        with open(db_file_path, 'r') as raw:
            json_file = json.load(raw)

        return json_file

    def _get_path_to_db_file(self, file_name: str) -> str:
        """Формирует путь до нужного запрошенного файла. Предполагается, что файл будет лежать в my_shiny_db

        Args:
            Имя файла (comment.json/news.json)
        Returns:
            ABS-путь до желаемого файла."""

        module_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.abspath(os.path.join(module_dir, '..'))
        db_dir = os.path.join(app_dir, self._db_folder_name)
        file_path = os.path.join(db_dir, file_name)

        return file_path

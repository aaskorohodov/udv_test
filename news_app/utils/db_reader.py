import asyncio
import json
import os

from pydantic import ValidationError, BaseModel

from news_app.models.internal.comments import CommentItem
from news_app.models.internal.news import NewsItem


class MyShinyDBReader:
    def __init__(self):
        self.db_folder_name: str = 'my_shiny_db'
        self.comments_path: str = 'comments.json'
        self.news_path: str = 'news.json'

    async def read_news_and_comments(self) -> dict[str, list[CommentItem], str,  list[NewsItem]]:

        comments, news = await asyncio.gather(
            self._read_comments(),
            self._read_news()
        )

        return {'comments': comments, 'news': news}

    async def f1(self):
        await asyncio.sleep(1)

    async def f2(self):
        await asyncio.sleep(1)

    async def _read_comments(self) -> list[CommentItem]:
        comments_dict = self._read_json(self.comments_path)['comments']
        comments_models = self._create_models_from_list(comments_dict, CommentItem)
        # noinspection PyTypeChecker
        return comments_models

    async def _read_news(self) -> list[NewsItem]:
        news_dict = self._read_json(self.news_path)['news']
        news_models = self._create_models_from_list(news_dict, NewsItem)
        # noinspection PyTypeChecker
        return news_models

    def _create_models_from_list(self, raw_data: list[dict], base_model: type[BaseModel]) -> list[BaseModel]:
        result = []
        for raw_dict in raw_data:
            try:
                model = base_model.model_validate(raw_dict)
                result.append(model)
            except ValidationError:
                pass

        return result

    def _read_json(self, file_name: str) -> dict:
        db_file_path = self._get_path_to_db_file(file_name)

        with open(db_file_path, 'r') as raw:
            json_file = json.load(raw)

        return json_file

    def _get_path_to_db_file(self, file_name: str) -> str:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.abspath(os.path.join(module_dir, '..'))
        db_dir = os.path.join(app_dir, self.db_folder_name)
        file_path = os.path.join(db_dir, file_name)

        return file_path

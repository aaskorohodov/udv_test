from fastapi import APIRouter

from news_app.endpoints.all_news.data_sorter_all_news import DataSorter
from news_app.utils.db_reader import MyShinyDBReader


router = APIRouter()


@router.get("/")
async def get_news():
    """Возвращает все новости"""

    # Читаем данные (имитируем чтение базы)
    db_reader = MyShinyDBReader()
    comments_and_news = await db_reader.read_news_and_comments()

    # Обрабатываем прочитанные данные, формируем модель для ответа
    data_sorter = DataSorter(comments_and_news)
    response_model = data_sorter.make_news_list()

    return response_model

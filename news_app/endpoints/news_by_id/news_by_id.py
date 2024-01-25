from fastapi import APIRouter

from news_app.endpoints.news_by_id.data_sorter_specific_news import SpecificNewsDataSorter
from news_app.utils.db_reader import MyShinyDBReader

router = APIRouter()


@router.get("/news/{news_id}")
async def get_news_by_id(news_id: int):
    db_reader = MyShinyDBReader()
    comments_and_news = await db_reader.read_news_and_comments()

    specific_news_sorter = SpecificNewsDataSorter(comments_and_news)
    result = specific_news_sorter.get_specific_news(news_id)

    return result

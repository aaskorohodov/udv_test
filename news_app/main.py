from fastapi import FastAPI


news_app = FastAPI()

from news_app.endpoints.all_news import all_news
from news_app.endpoints.news_by_id import news_by_id

news_app.include_router(all_news.router)
news_app.include_router(news_by_id.router)

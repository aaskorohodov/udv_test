from fastapi import FastAPI
from news_app.main import news_app
from news_app.utils.env_setter import EnvSetter


# Строим инстанс приложения и подключаем роутеры
root_app = FastAPI()
root_app.include_router(news_app.router)

# Для запуска в режиме разработки
if __name__ == "__main__":
    import uvicorn

    # Читаем переменные окружения (пути к файлам-json)
    EnvSetter.set_envs(__file__)

    uvicorn.run(root_app, host="127.0.0.1", port=8000)

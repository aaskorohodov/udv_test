from fastapi import FastAPI
from news_app.main import news_app

# Create an instance of FastAPI
root_app = FastAPI()


# Include the FastAPI app from the app directory
root_app.include_router(news_app.router)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app at the root level
    uvicorn.run(root_app, host="127.0.0.1", port=8000)

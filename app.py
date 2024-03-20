"""
The main file of the FastAPI application.
Here we connect all the paths and the logic of the API.
"""
import uvicorn
from fastapi import FastAPI

from src import country, temperature, favourite

app = FastAPI(root_path="/api",
              title="Countries API",
              description="This is a simple API that returns a list of countries.",
              version="1.0")

app.include_router(country.router)
app.include_router(favourite.router)


@app.get("/")
async def root():
    """
    This is the root path of the API. It returns a simple message.
    :return:
    """
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000)

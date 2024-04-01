"""
The main file of the FastAPI application.
Here we connect all the paths and the logic of the API.
"""
import argparse

import uvicorn
from fastapi import FastAPI

from src import country, favourite

# Create a parser
parser = argparse.ArgumentParser(description="Run the FastAPI application.")
# Add the API key argument
parser.add_argument('--api_key', type=str, required=True,
                    help='The API key for the OpenWeatherMap API.')
# Parse the arguments
args = parser.parse_args()

country.set_api_key(args.api_key)

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
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

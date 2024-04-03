"""
The main file of the FastAPI application.
Here we connect all the paths and the logic of the API.
"""

import argparse

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from src import country, favourite

# Create a parser
parser = argparse.ArgumentParser(description="Run the FastAPI application.")
# Add the API key argument
parser.add_argument(
    "--api_key", type=str, required=True, help="The API key for the OpenWeatherMap API."
)
# Parse the arguments
args = parser.parse_args()

country.set_api_key(args.api_key)

app = FastAPI(
    root_path="/api",
    title="Countries API",
    description="This is a simple API that returns a list of countries.",
    version="1.0",
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(country.router)
app.include_router(favourite.router)

# Documentation routes
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_js_url="./static/swagger-ui-bundle.js",
        swagger_css_url="./static/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url="./static/redoc.standalone.js",
    )


@app.get(
    "/",
    responses={
        200: {
            "description": "Welcome message from the API",
            "content": {
                "application/json": {
                    "example": {"message": "Welcome to Countries API"},
                },
            },
        }
    },
)
async def root():
    """
    This is the root path of the API. It returns a simple message.
    :return:
    """
    return {"message": "Welcome to Countries API"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

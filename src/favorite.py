"""
This module contains API paths related to the favorite countries.
"""

import json

import httpx
from fastapi import APIRouter, Body, Path, Response, status

from src.models import CountryName

REST_COUNTRIES_URL = "https://restcountries.com/v3.1"

favorite_countries = []

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    responses={
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Not found"},
                }
            },
        }
    },
)


@router.get(
    "",
    responses={
        200: {
            "description": "List of favorite countries",
            "content": {
                "application/json": {
                    "example": {"favorites": ["Albania"]},
                    "schema": {
                        "type": "object",
                        "properties": {
                            "favorites": {
                                "type": "array",
                                "items": {"type": "string"},
                            }
                        },
                    },
                }
            },
        }
    },
)
async def get_favorite_countries() -> Response:
    """
    This path will return the list of favorite countries.

    :return: A response with the list of favorite countries.
    """
    return Response(
        status_code=200,
        content=json.dumps({"favorites": favorite_countries}, indent=4),
    )


@router.post(
    "",
    responses={
        200: {
            "description": "Country added to the favorite list",
            "content": {
                "application/json": {
                    "example": {"message": "Albania added to the favorite list"},
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                        },
                    },
                }
            },
        },
        404: {
            "description": "Country not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Country not found"},
                    "schema": {
                        "type": "string",
                        "description": "The error message.",
                    },
                }
            },
        },
        500: {
            "description": "Error parsing the response",
            "content": {
                "application/json": {
                    "example": {"detail": "Error parsing the response"},
                    "schema": {
                        "type": "string",
                        "description": "The error message.",
                    },
                }
            },
        },
    },
)
async def add_favorite(
    country_name: CountryName = Body(
        ..., description="The name of the country", example={"name": "Albania"}
    )
) -> Response:
    """
    This path will add a country to the favorite list.

    :param country_name: The name of the country.

    :return: A response with the result of the operation.
    """
    # Get the country
    url = f"{REST_COUNTRIES_URL}/name/{country_name.name.lower()}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND, content="Country not found"
            )
        try:
            country = response.json()[0]
            favorite_countries.append(country["name"]["common"])
            return Response(
                status_code=status.HTTP_200_OK,
                content=json.dumps(
                    {
                        "message": f"{country['name']['common']} added to the favorite list"
                    },
                    indent=4,
                ),
            )
        except KeyError:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Error parsing the response",
            )


@router.delete(
    "",
    responses={
        200: {
            "description": "Country removed from the favorite list",
            "content": {
                "application/json": {
                    "example": {"message": "Albania removed from the favorite list"},
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                        },
                    },
                }
            },
        },
        404: {
            "description": "Country not found in the favorite list",
            "content": {
                "application/json": {
                    "example": {"detail": "Country not found in the favorite list"},
                    "schema": {
                        "type": "string",
                        "description": "The error message.",
                    },
                }
            },
        },
    },
)
async def delete_favorite(
    country_name: CountryName = Body(
        ..., description="The name of the country", example={"name": "Albania"}
    )
) -> Response:
    """
    This path will remove a country from the favorite list.

    :param country_name: The name of the country.

    :return: A response with the result of the operation.
    """
    if country_name.name in favorite_countries:
        favorite_countries.remove(country_name.name)
        return Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps(
                {"message": f"{country_name.name} removed from the favorite list"},
                indent=4,
            ),
        )
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content="Country not found in the favorite list",
    )

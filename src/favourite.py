"""
This module contains API paths related to the favourite countries.
"""

import json

import httpx
from fastapi import APIRouter, Response, status

from src.models import CountryName

REST_COUNTRIES_URL = "https://restcountries.com/v3.1"

favourite_countries = ["Albania"]

router = APIRouter(prefix="/favourite", tags=["favourite"],
                   responses={404: {"description": "Not found",
                                    "content": {
                                        "plain/text": {"example": "Not found"}}}},
                   )


@router.get("",

            responses={200: {"description": "List of favourite countries",
                             "content":
                                 {"application/json":
                                     {"example": {
                                         "favourite countries": ["Albania"]},
                                         "schema": {
                                             "type": "object",
                                             "properties": {
                                                 "favourite countries": {
                                                     "type": "array",
                                                     "items": {
                                                         "type": "string"
                                                     }
                                                 }
                                             }

                                         }}}}
                       })
async def get_favourite_countries() -> Response:
    """
    This path will return the list of favourite countries.

    :return: A response with the list of favourite countries.
    """
    return Response(status_code=200,
                    content=json.dumps({"favourite countries": favourite_countries},
                                       indent=4))


@router.post("",
             responses={
                 200: {"description": "Country added to the favourite list",
                       "content": {"application/json": {
                           "example": {
                               "message": "Albania added to the favourite list"},
                       }}},
                 404: {"description": "Country not found",
                       "content": {"plain/text": {
                           "example": "Country not found",
                       }}},
                 500: {"description": "Error parsing the response",
                       "content": {"plain/text": {
                           "example": "Error parsing the response",
                       }}},
             })
async def add_favourite(country_name: CountryName) -> Response:
    """
    This path will add a country to the favourite list.

    :param country_name: The name of the country.

    :return: A response with the result of the operation.
    """
    # Get the country
    url = f"{REST_COUNTRIES_URL}/name/{country_name.name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content="Country not found")
        try:
            country = response.json()[0]
            favourite_countries.append(country["name"]["common"])
            return Response(status_code=status.HTTP_200_OK,
                            content=json.dumps(
                                {
                                    "message": f"{country['name']['common']} "
                                               f"added to the favourite list"},
                                indent=4))
        except KeyError:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content="Error parsing the response")


@router.delete("",
               responses={
                   200: {"description": "Country removed from the favourite list",
                         "content": {"application/json": {
                             "example": {
                                 "message": "Albania removed from the favourite list"},
                         }}},
                   404: {"description": "Country not found in the favourite list",
                         "content": {"plain/text": {
                             "example": "Country not found in the favourite list",
                         }}},
               })
async def delete_favourite(country_name: CountryName) -> Response:
    """
    This path will remove a country from the favourite list.

    :param country_name: The name of the country.

    :return: A response with the result of the operation.
    """
    if country_name.name in favourite_countries:
        favourite_countries.remove(country_name.name)
        return Response(status_code=status.HTTP_200_OK,
                        content=json.dumps(
                            {
                                "message": f"{country_name.name} "
                                           f"removed from the favourite list"},
                            indent=4)
                        )
    return Response(status_code=status.HTTP_404_NOT_FOUND,
                    content="Country not found in the favourite list")

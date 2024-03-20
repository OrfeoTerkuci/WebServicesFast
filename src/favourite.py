"""
This module contains API paths related to the favourite countries.
"""

import json
import httpx

from fastapi import APIRouter, Response
from src.models import CountryName

REST_COUNTRIES_URL = "https://restcountries.com/v3.1"

favourite_countries = ["Albania"]

router = APIRouter(prefix="/favourite", tags=["favourite"],
                   responses={404: {"description": "Not found"}})


@router.post("")
async def add_favourite(country_name: CountryName):
    """
    This path will add a country to the favourite list.
    :param country_name: The name of the country.
    :return:
    """
    # Get the country
    url = f"{REST_COUNTRIES_URL}/name/{country_name.name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return Response(status_code=response.status_code, content=response.content)
        try:
            country = response.json()[0]
            favourite_countries.append(country["name"]["common"])
            return Response(status_code=response.status_code,
                            content=json.dumps(
                                {"message": "Country added to the favourite list"}))
        except KeyError:
            return Response(status_code=500, content="Error parsing the response")


@router.delete("")
async def delete_favourite(country_name: CountryName):
    """
    This path will remove a country from the favourite list.
    :param country_name: The name of the country.
    :return:
    """
    if country_name.name in favourite_countries:
        favourite_countries.remove(country_name.name)
        return Response(status_code=200, content=json.dumps(
            {"message": "Country removed from the favourite list"}))
    return Response(status_code=500, content=json.dumps(
        {"message": "Country not found in the favourite list"}))


@router.get("")
async def get_favourite_countries():
    """
    This path will return the list of favourite countries.
    :return:
    """
    return Response(status_code=200, content=json.dumps(favourite_countries))

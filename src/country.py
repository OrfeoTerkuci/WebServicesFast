"""
Module for the country resource
"""
import json
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Response

router = APIRouter(prefix="/country", tags=["country"],
                   responses={404: {"description": "Not found"}})

REST_COUNTRIES_URL = "https://restcountries.com/v3.1"
openweathermap_url = "https://api.openweathermap.org/data/2.5/forecast"
quickchart_url = "https://quickchart.io/chart"
api_key = "2272c802c8593cfe75843f203090680f"


@router.get("")
async def get_countries(continent: str = None):
    """
    This path will return a list with all the countries.
    :param continent: The continent to filter the countries.
    :return: A list with the countries.
    """
    if continent:
        url = f"{REST_COUNTRIES_URL}/region/{continent}"
    else:
        url = f"{REST_COUNTRIES_URL}/all"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return Response(status_code=response.status_code, content=response.content)
        try:
            countries = [country["name"]["common"] for country in response.json()]
            return Response(status_code=response.status_code,
                            content=json.dumps(countries))
        except KeyError:
            return Response(status_code=500, content="Error parsing the response")


@router.get("/{country_name}")
async def get_country(country_name: str):
    """
    This path will return the information of a country.
    This information includes:
    - Longitude and latitude of the capital.
    - Population.
    - Area.
    :param country_name: The name of the country.
    :return:
    """
    url = f"{REST_COUNTRIES_URL}/name/{country_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return Response(status_code=response.status_code, content=response.content)
        try:
            country = response.json()[0]
            return Response(status_code=response.status_code,
                            content=json.dumps({"capital": country["capital"],
                                                "latitude":
                                                    country["capitalInfo"]["latlng"][0],
                                                "longitude":
                                                    country["capitalInfo"]["latlng"][1],
                                                "population": country["population"],
                                                "area": country["area"]}))
        except KeyError:
            return Response(status_code=500, content="Error parsing the response")


@router.get("/{country_name}/temperature")
async def get_temperature(country_name: str):
    """
    This path will return the temperature of a country.
    :param country_name: The name of the country.
    :return:
    """
    # Get the country information (latitude and longitude of the capital)
    url = f"{REST_COUNTRIES_URL}/name/{country_name}"

    async with httpx.AsyncClient() as client:
        try:
            # Get the country information
            response = await client.get(url)
            if response.status_code != 200:
                return Response(status_code=response.status_code,
                                content=response.content)

            country = response.json()[0]
            latitude = country["capitalInfo"]["latlng"][0]
            longitude = country["capitalInfo"]["latlng"][1]

            url = (f"{openweathermap_url}?lat={latitude}&lon={longitude}&units=metric"
                   f"&cnt=1&appid={api_key}")
            # Get the forecast
            response = await client.get(url)
            if response.status_code != 200:
                return Response(status_code=response.status_code,
                                content=response.content)
            temperature = response.json()["list"][0]["main"]["temp"]
            return Response(status_code=response.status_code,
                            content=json.dumps(temperature))
        except KeyError:
            return Response(status_code=500, content="Error parsing the response")


@router.get("/{country_name}/forecast/{days}")
async def get_temperature(country_name: str, days: int = 1):
    """
    This path will return the temperature of a country.
    :param days: The number of days to get the forecast. Maximum 5 days.
    :param country_name: The name of the country.
    :return:
    """
    # Get the country information (latitude and longitude of the capital)
    url = f"{REST_COUNTRIES_URL}/name/{country_name}"
    # Check if the number of days is supported
    if not 1 <= days <= 5:
        return Response(status_code=400,
                        content="The number of days must be between 1 and 5")

    async with httpx.AsyncClient() as client:
        try:
            # Get the country information
            response = await client.get(url)
            if response.status_code != 200:
                return Response(status_code=response.status_code,
                                content=response.content)

            country = response.json()[0]
            latitude = country["capitalInfo"]["latlng"][0]
            longitude = country["capitalInfo"]["latlng"][1]

            # Calculate the number of 3-hour intervals
            hours = days * 8 if days <= 5 else 0
            url = (f"{openweathermap_url}?lat={latitude}&lon={longitude}&cnt={hours}&"
                   f"units=metric&appid={api_key}")
            # Get the forecast
            response = await client.get(url)
            if response.status_code != 200:
                return Response(status_code=response.status_code,
                                content=response.content)

            temperature = [forecast["main"]["temp"] for forecast in
                           response.json()["list"]]
        except KeyError:
            return Response(status_code=500, content="Error parsing the response")

        return await get_chart(client, days, temperature)


async def get_chart(client, days, temperature):
    """
    This function will create a chart with the temperature forecast.
    :param client: The HTTP client.
    :param days: The number of days.
    :param temperature: The temperature forecast.
    :return: The chart as a response, or an error response..
    """
    # Create the chart
    chart_param = {'type': 'line',
                   'data': {'labels': translate_hours_to_days(days),
                            'datasets': [{'label': 'Temperature',
                                          'data': temperature}]}}
    params = {
        "version": "2",
        "backgroundColor": "transparent",
        "chart": chart_param
    }
    response = await client.post(quickchart_url, json=params)
    if response.status_code != 200:
        return Response(status_code=response.status_code,
                        content=response.content)
    else:
        return Response(status_code=response.status_code,
                        content=response.content,
                        media_type="image/png")


def translate_hours_to_days(days: int):
    """
    Starting from the current time, it will return the hours of the next days in
    3-hour intervals.
    :param days: The number of days.
    :return: A list with the hours.
    """
    time = datetime.now()
    hours = []
    # Get the hours of the next days from the current time
    # Also add the date to the hours
    for _ in range(days):
        for _ in range(8):
            time += timedelta(hours=3)
            hours.append(time.strftime("%d-%m %H:%M"))

    return hours

"""
This file is used to test the app.
The app is supposed to be running in the background.
"""
import asyncio

import httpx
from app import app

base_url = "http://localhost:8000/api"


async def main():
    """
    Get the currently warmest country in South America.
    :return: The name of the country.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/country?continent=south%20america")
        if response.status_code != 200:
            return response.content
        countries = response.json()
        warmest_country = {"name": "", "temperature": -1000}
        for country in countries:
            response = await client.get(f"{base_url}/country/{country}/temperature")
            if response.status_code != 200:
                return response.content
            temperature = response.json()
            if temperature > warmest_country["temperature"]:
                warmest_country = {"name": country, "temperature": temperature}
        return warmest_country["name"]


if __name__ == "__main__":
    asyncio.run(main())

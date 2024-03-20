"""
This file is used to test the app.
The app is supposed to be running in the background.
"""
import asyncio

import httpx

base_url = "http://localhost:8000/api"


async def main():
    """
    Get the currently warmest country in South America.
    :return: The name of the country.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/countries?continent=south%20america")
        if response.status_code != 200:
            return response.content
        countries = response.json()["countries"]
        print(f"The countries in South America are {', '.join(countries)}")
        warmest_country = {"name": "", "temperature": -1000}
        for country in countries:
            response = await client.get(f"{base_url}/countries/{country}/temperature")
            if response.status_code != 200:
                return response.content
            temperature = response.json()["temperature"]
            print(f"The temperature in {country} is {temperature}")
            if temperature > warmest_country["temperature"]:
                warmest_country = {"name": country, "temperature": temperature}

        print(f"The warmest country in South America at the moment is "
              f"{warmest_country['name']}")

        # Get a graph of the forecast of the temperature for the next 4 days
        response = await client.get(
            f"{base_url}/countries/{warmest_country['name']}/forecast/4")
        if response.status_code != 200:
            return response.content

        # Content is a png image in bytes
        with open(f"forecast_{warmest_country['name']}.png", "wb") as f:
            f.write(response.content)
        print("The forecast image has been saved as forecast.png")


if __name__ == "__main__":
    asyncio.run(main())

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

        patience = 3

        for country in countries:

            # wait 3 turns before giving up
            if patience < 0:
                break

            # Get the temperature of the country
            response = await client.get(f"{base_url}/countries/{country}/temperature")

            # If temperature is not available, try again with another country,
            # but up to 3 times
            if response.status_code != 200:
                print(f"Error getting the temperature for {country}. "
                      f"Is the API key correct?")
                patience -= 1
                continue

            temperature = response.json()["temperature"]
            print(f"The temperature in {country} is {temperature}")
            if temperature > warmest_country["temperature"]:
                warmest_country = {"name": country, "temperature": temperature}

        if warmest_country["temperature"] == -1000:
            print("There was an error getting the temperature for all the countries. "
                  "Is the API key correct?")
            return

        print(f"\nThe warmest country in South America at the moment is "
              f"{warmest_country['name']} with a temperature of "
              f"{warmest_country['temperature']} degrees Celsius.\n")

        print("Obtaining forecast for the next 4 days...")
        # Get a graph of the forecast of the temperature for the next 4 days
        response = await client.get(
            f"{base_url}/countries/{warmest_country['name']}/forecast/4")
        if response.status_code != 200:
            return response.content

        # Content is a png image in bytes
        with open(f"forecast_{warmest_country['name']}.png", "wb") as f:
            f.write(response.content)
        print(f"The forecast image has been saved as "
              f"forecast_{warmest_country["name"]}.png")


if __name__ == "__main__":
    asyncio.run(main())

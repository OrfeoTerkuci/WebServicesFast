"""
This file is used to test the app.
The app is supposed to be running in the background.
"""
import asyncio
import random

import httpx

base_url = "http://localhost:8000/api"


async def run_warmest_country(client: httpx.AsyncClient):
    response = await client.get(f"{base_url}/country?continent=south%20america")
    if response.status_code != 200:
        return response.content
    countries = response.json()["countries"]
    print(f"The countries in South America are {', '.join(countries)}")
    
    # Get the temperature of the countries, and find the warmest one
    warmest_country = {"name": "", "temperature": -1000}
    patience = 3
    
    for country in countries:

        # wait 3 turns before giving up
        if patience < 0:
            break

        # Get the temperature of the country
        response = await client.get(f"{base_url}/country/{country}/temperature")

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

    # Favourite the warmest country
    print(f"Favouriting {warmest_country['name']}...")
    response = await client.post(f"{base_url}/favourite",
                                 json={"name": warmest_country["name"]})
    if response.status_code != 200:
        return response.content
    
    # Test that the country was favourited
    print("Getting favourites...")
    response = await client.get(f"{base_url}/favourite")
    if response.status_code != 200:
        return response.content
    favourites = response.json()["favourites"]
    if warmest_country["name"] in favourites:
        print(f"{warmest_country['name']} was favourited.")
    else:
        print(f"{warmest_country['name']} was not favourited.")
        return

    # Get the forecast for the next 4 days
    print("Obtaining forecast for the next 4 days...")
    # Get a graph of the forecast of the temperature for the next 4 days
    response = await client.get(
        f"{base_url}/country/{warmest_country['name']}/forecast/4")
    if response.status_code != 200:
        return response.content

    # Content is a png image in bytes -> save it to a file
    with open(f"forecast_{warmest_country['name']}.png", "wb") as f:
        f.write(response.content)
    print(f"The forecast image has been saved as forecast_{warmest_country["name"]}.png")


async def run_all_countries(client: httpx.AsyncClient) -> list[str]:
    print("Getting all countries...\n")
    response = await client.get(f"{base_url}/country")
    if response.status_code != 200:
        return []
    countries = response.json()["countries"]
    print(f"The countries are {', '.join(countries)}")
    return countries

async def run_country(client: httpx.AsyncClient, country: str):
    print(f"Getting information for {country}...\n")
    response = await client.get(f"{base_url}/country/{country}")
    if response.status_code != 200:
        return response.content
    print(response.json())
    return response.json()

async def run_country_temperature(client: httpx.AsyncClient, country: str):
    print(f"Getting temperature for {country}...\n")
    response = await client.get(f"{base_url}/country/{country}/temperature")
    if response.status_code != 200:
        return response.content
    temperature = response.json()["temperature"]
    print(f"The temperature in {country} is {temperature}")
    return temperature

async def run_country_forecast(client: httpx.AsyncClient, country: str, days: int):
    print(f"Getting forecast for {country} for the next {days} days...\n")
    response = await client.get(f"{base_url}/country/{country}/forecast/{days}")
    if response.status_code != 200:
        return response.content
    # Content is a png image in bytes
    with open(f"forecast_{country}.png", "wb") as f:
        f.write(response.content)
    print(f"The forecast image has been saved as forecast_{country}.png")
    return response.content

## Favourites

async def run_favourites(client: httpx.AsyncClient):
    print("Getting favourites...\n")
    response = await client.get(f"{base_url}/favourite")
    if response.status_code != 200:
        return response.content
    favourites = response.json()["favourites"]
    if favourites:
        print(f"The favourites are: {', '.join(favourites)}")
    else:
        print("There are no favourites.")
    return favourites

async def run_add_favourite(client: httpx.AsyncClient, country: str):
    print(f"Adding {country} to favourites...\n")
    response = await client.post(f"{base_url}/favourite",
                                 json={"name": country})
    if response.status_code != 200:
        return response.content
    print(response.json())
    return response.json()

async def run_remove_favourite(client: httpx.AsyncClient, country: str):
    print(f"Removing {country} from favourites...\n")
    response = await client.request("DELETE", f"{base_url}/favourite",
                                    json={"name": country})
    if response.status_code != 200:
        return response.content
    print(response.json())
    return response.json()

async def main():
    """
    Get the currently warmest country in South America.
    :return: The name of the country.
    """
    async with httpx.AsyncClient() as client:

        # Get all countries
        countries = await run_all_countries(client)

        # choose a random country
        choice = random.randint(0, len(countries) - 1)
        country: str = countries[choice]

        await run_country(client, country)
        await run_country_temperature(client, country)
        await run_country_forecast(client, country, 4)
        
        # Favourites
        # Favourites are empty
        await run_favourites(client)
        # Add a favourite
        await run_add_favourite(client, country)
        await run_favourites(client)
        # Remove a favourite
        await run_remove_favourite(client, country)
        await run_favourites(client)

        # Get the warmest country in South America
        await run_warmest_country(client)
        

if __name__ == "__main__":
    asyncio.run(main())

# Web services - Weather API

## Description

After a cold winter, you are tired of this cold weather and instead, plan on making a
trip to a warm location. However, your requirements are strict, and you want to travel
to
the country that is currently the warmest. As a result,you first develop an API to find
out what location is currently the warmest.

## Usage

You can run the api by running the script `run_api.sh` and you
can run the script to get the warmest country in South America by running the
script `run_script.sh`. The script will output the warmest country in South America,
and save the image of the forecast as `forecast_<country>.png`.  
Replace `YOUR_API_KEY` with your own API key for openweathermap.

The API key I used is `2272c802c8593cfe75843f203090680f`

**The test script cannot be run without having the API running.**

Recommended to run in WSL or Linux.

```bash
./run_api.sh 2272c802c8593cfe75843f203090680f
```

```bash
./run_script.sh
```

## Documentation

API documentation can be found in the `/docs` route of the API.
The `openapi.json` file containing the OpenAPI documentation can be found in the
`static` folder.

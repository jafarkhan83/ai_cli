from langchain_core.tools import tool
import requests
import os

@tool
def get_whether(city: str) -> str:
    """Get the current temperature for a given city."""

    url = 'https://api.weatherapi.com/v1/current.json'
    params = {
		"key" : os.getenv("WHETHER_API_KEY"),
		"q" : city
	}
    response = requests.get(url=url, params=params)
    return response.json()['current']['temp_c']

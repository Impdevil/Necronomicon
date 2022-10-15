import requests
import os


def GetForecast():  
    url = os.environ.get("WEATHERAPISITE") + "forecast.json?key=" + os.environ.get("WEATHERAPI")+"&q=" + os.environ.get("LOCATION") + "&days=2&aqi=no&alerts=no"
    #print(url)
    responce = requests.get(url)
    results = responce.json()
    forecastdays = results["forecast"]["forecastday"]
    #print()
    #print(forecastdays)
    #print()
    return forecastdays




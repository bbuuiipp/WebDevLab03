import streamlit as st
import pandas as pd
import requests as rq
import CityTranslate as translate
import re


st.header("Weather Forecast!")


def parseAddress(address):
    #captures the individual parts of the string
    correctPattern = r'^(.*?),\s*(.*?),\s*([A-Z]{2})\s*(\d{5})(?:-\d{4})?$'
    #uses re module to match the addresss input to the pattern given
    match = re.match(correctPattern, address)
    if match:
        street, city, state, zipCode = match.groups()
        return {
            "street": street,
            "city": city,
            "state": state,
            "zip": zipCode
        }

address = parseAddress(st.text_input("Enter your full address ('123 Main St, City, ST 12345'): "))
future = st.number_input("How many days in the future do you want to see?: ", min_value = 0, max_value = 13, step = 1)

if address != None:
    weatherInfo = (translate.fetch_weather(address["street"], address["city"], address["state"], address["zip"]))

    data = {"Icon": [], "Day": [], "Description of the Weather": []}
    icons = {"sunny": "☀️", "cloudy": "🌤️", "rainy": "☔", "fog": "🌫️", "temp": "🌡️"}
    for day in weatherInfo:
        if "clear" in day["shortForecast"].lower() or "sun" in day["shortForecast"].lower():
            data["Icon"] = data["Icon"] + [icons["sunny"]]
        elif "cloudy" in day["shortForecast"].lower():
            data["Icon"] = data["Icon"] + [icons["cloudy"]]
        elif "rain" in day["shortForecast"].lower() or "showers" in day["shortForecast"].lower():
            data["Icon"] = data["Icon"] + [icons["rainy"]]
        elif "fog" in day["shortForecast"].lower():
            
            data["Icon"] = data["Icon"] + [icons["fog"]]
        else:
            data["Icon"] = data["Icon"] + [icons["temp"]]
        data["Day"] = data["Day"] + [day["name"]]
        data["Description of the Weather"] = data["Description of the Weather"] + [day["detailedForecast"]]
        if len(data["Day"]) > future:
            break

    df = pd.DataFrame(data)
    st.table(df)
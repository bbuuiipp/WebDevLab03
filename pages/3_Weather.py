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

st.write(translate.fetch_weather(address["street"], address["city"], address["state"], address["zip"]))
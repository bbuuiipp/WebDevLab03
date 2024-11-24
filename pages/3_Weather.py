import streamlit as st
import pandas as pd
import requests as rq
import CityTranslate as translate

st.header("Weather Forecast!")

response = rq.get("https://api.weather.gov/openapi.json")

st.write(translate.fetch_weather("565 Elgaen Ct", "Roswell", "GA", "30075"))
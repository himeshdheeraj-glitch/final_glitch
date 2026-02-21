import requests
import streamlit as st

def my_geolocation(key="loc", default=None):
    """
    A simple geolocation utility that fetches the user's approximate
    location based on their IP address using ipapi.co. This is used
    as a workaround for Streamlit since native browser GPS requires
    special component interactions.
    """
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude")
            }
        else:
            return default
    except Exception as e:
        return default

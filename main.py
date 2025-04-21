import os
import requests
from fastapi import FastAPI

# FastAPI app setup
app = FastAPI()

# Fetch API key and secret from environment variables (replace these if necessary)
DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

# Delta Exchange API URL for options
options_url = "https://api.delta.exchange/v2/options"

# Function to fetch options data from Delta Exchange
def fetch_options_data():
    try:
        # Make a GET request to Delta Exchange API to fetch options data
        response = requests.get(options_url, headers={
            'Authorization': f'Bearer {DELTA_API_KEY}'
        })

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return options data as JSON
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        # Catch any errors and return the message
        return {"error": f"An error occurred: {str(e)}"}

# FastAPI endpoint to return options data
@app.get("/options-data")
async def get_options_data():
    data = fetch_options_data()  # Fetch the data
    return data  # Return the data (will be converted to JSON automatically)
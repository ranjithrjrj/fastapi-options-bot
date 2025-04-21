import os
import requests

# Retrieve API key and secret from environment variables
DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

# Delta Exchange API URL for options
options_url = "https://api.delta.exchange/v2/options"

# Function to fetch options data
def fetch_options_data():
    # Make a request to the Delta Exchange API to fetch options data
    response = requests.get(options_url, headers={
        'Authorization': f'Bearer {DELTA_API_KEY}'
    })
    
    if response.status_code == 200:
        return response.json()  # Return options data as JSON
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

# Example: Fetch options data
options_data = fetch_options_data()

if "error" not in options_data:
    print("Options Data:", options_data)
else:
    print("Error fetching options data:", options_data)
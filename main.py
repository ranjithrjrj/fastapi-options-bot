from fastapi import FastAPI
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()

DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

HEADERS = {
    "api-key": DELTA_API_KEY,
    "api-secret": DELTA_API_SECRET
}

BASE_URL = "https://api.delta.exchange"


def get_option_chain():
    try:
        url = f"{BASE_URL}/v2/options/chains"
        response = requests.get(url, headers=HEADERS)
        print("Status code:", response.status_code)
        print("Response text:", response.text[:500])  # Trim for log safety
        return response.json().get("result", [])
    except Exception as e:
        print(f"Error fetching option chain: {e}")
        return []


def get_filtered_high_vega_options(option_chain, option_type, top_n=10):
    filtered_options = [
        o for o in option_chain
        if o.get("option_type") == option_type and
        o.get("vega") is not None and
        o.get("underlying_asset") == "BTC"
    ]

    sorted_options = sorted(filtered_options, key=lambda x: x["vega"], reverse=True)
    top_options = sorted_options[:top_n]

    return [
        {
            "strike_price": o.get("strike_price"),
            "expiry": o.get("expiry"),
            "vega": o.get("vega"),
            "symbol": o.get("symbol")
        }
        for o in top_options
    ]


@app.get("/")
def root():
    return {"message": "Delta Options Alpha API is working."}


@app.get("/options/high-vega")
def get_high_vega():
    option_chain = get_option_chain()
    if not option_chain:
        return {"error": "No option chain data found."}

    top_calls = get_filtered_high_vega_options(option_chain, "call", 10)
    top_puts = get_filtered_high_vega_options(option_chain, "put", 10)

    return {
        "top_10_high_vega_calls": top_calls,
        "top_10_high_vega_puts": top_puts
    }

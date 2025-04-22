from fastapi import FastAPI
import requests
import os
from typing import List

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
        print("Response text:", response.text)
        return response.json().get("result", [])
    except Exception as e:
        print(f"Error fetching option chain: {e}")
        return []

def get_top_vega_options(options: List[dict], option_type: str, limit: int = 10):
    filtered = [
        o for o in options
        if o.get("option_type") == option_type
        and o.get("underlying_symbol") == "BTCUSD"
        and o.get("vega") is not None
    ]
    sorted_options = sorted(filtered, key=lambda x: x["vega"], reverse=True)
    top = sorted_options[:limit]
    return [
        {
            "strike_price": o["strike_price"],
            "expiry": o["expiry_date"],
            "vega": o["vega"]
        }
        for o in top
    ]

@app.get("/")
def root():
    return {"message": "BTC Options Alpha API is live."}

@app.get("/options/high-vega")
def high_vega():
    all_options = fetch_option_chain()
    if not all_options:
        return {"error": "No option chain data found."}

    # Filter for 3 expiry dates: T, T+1, T+2
    unique_expiries = sorted(set(o["expiry_date"] for o in all_options if o["underlying_symbol"] == "BTCUSD"))
    recent_expiries = unique_expiries[:3]

    filtered_by_expiry = [o for o in all_options if o["expiry_date"] in recent_expiries and o["underlying_symbol"] == "BTCUSD"]

    top_calls = get_top_vega_options(filtered_by_expiry, "call")
    top_puts = get_top_vega_options(filtered_by_expiry, "put")

    return {
        "top_10_high_vega_calls": top_calls,
        "top_10_high_vega_puts": top_puts
    }

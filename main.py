from fastapi import FastAPI
import requests
import os

app = FastAPI()

DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

HEADERS = {
    "api-key": DELTA_API_KEY,
    "api-secret": DELTA_API_SECRET
}

BASE_URL = "https://api.delta.exchange"

def get_btc_options():
    try:
        url = f"{BASE_URL}/v2/products"
        response = requests.get(url)
        products = response.json().get("result", [])
        return [p for p in products if p["product_type"] == "options" and "BTC" in p["underlying_asset"]["symbol"]]
    except Exception as e:
        print(f"Error fetching BTC options: {e}")
        return []

def get_ticker_data(symbol):
    try:
        url = f"{BASE_URL}/v2/tickers/{symbol}"
        response = requests.get(url)
        return response.json().get("result", {})
    except Exception as e:
        print(f"Error fetching ticker data for {symbol}: {e}")
        return {}

@app.get("/options/high-vega")
def high_vega_options():
    btc_options = get_btc_options()
    calls = []
    puts = []

    for option in btc_options:
        symbol = option["symbol"]
        details = get_ticker_data(symbol)
        vega = details.get("vega")

        if vega is not None:
            entry = {
                "symbol": symbol,
                "strike_price": option["strike_price"],
                "expiry": option["expiry_date"],
                "vega": vega
            }

            if option["option_type"] == "call":
                calls.append(entry)
            elif option["option_type"] == "put":
                puts.append(entry)

    # Sort by Vega in descending order
    top_calls = sorted(calls, key=lambda x: x["vega"], reverse=True)[:10]
    top_puts = sorted(puts, key=lambda x: x["vega"], reverse=True)[:10]

    return {
        "top_10_high_vega_calls": top_calls,
        "top_10_high_vega_puts": top_puts
    }

@app.get("/")
def root():
    return {"message": "FastAPI running - Delta Options Vega fetcher"}

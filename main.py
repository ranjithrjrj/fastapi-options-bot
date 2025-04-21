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

def fetch_option_chain():
    try:
        response = requests.get(f"{BASE_URL}/v2/options/chains")
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print(f"Error fetching option chain: {e}")
        return []

@app.get("/")
def root():
    return {"message": "Delta Exchange Options API is working."}

@app.get("/options/high-vega")
def high_vega_options():
    chain = fetch_option_chain()
    if not chain:
        return {"error": "No option chain data found."}

    call_options = []
    put_options = []

    # Get top 3 expiries (T, T+1, T+2)
    expiries = sorted(list({opt["expiry_date"] for opt in chain}))[:3]

    # For debugging: show sample options that have Vega values
    sample_with_vega = [opt for opt in chain if opt.get("vega") is not None][:5]

    for option in chain:
        if option["expiry_date"] in expiries and option.get("vega") is not None:
            entry = {
                "symbol": option["contract_symbol"],
                "expiry": option["expiry_date"],
                "strike": option["strike_price"],
                "vega": option["vega"],
                "type": option["option_type"]
            }
            if option["option_type"] == "call":
                call_options.append(entry)
            elif option["option_type"] == "put":
                put_options.append(entry)

    top_calls = sorted(call_options, key=lambda x: x["vega"], reverse=True)[:10]
    top_puts = sorted(put_options, key=lambda x: x["vega"], reverse=True)[:10]

    return {
        "sample_vega_preview": sample_with_vega,
        "top_10_high_vega_calls": top_calls,
        "top_10_high_vega_puts": top_puts
        }

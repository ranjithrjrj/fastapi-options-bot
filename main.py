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

def get_instruments():
    try:
        response = requests.get(f"{BASE_URL}/v2/products")
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print(f"Error fetching instruments: {e}")
        return []

def get_option_chain():
    try:
        response = requests.get(f"{BASE_URL}/v2/options/chains")
        return response.json().get("result", [])
    except Exception as e:
        print(f"Error fetching option chain: {e}")
        return []

def get_iv(symbol="BTCUSD"):
    try:
        response = requests.get(f"{BASE_URL}/v2/underlying/index?symbol={symbol}")
        data = response.json()
        return data.get("result", {}).get("iv")
    except Exception as e:
        print(f"Error fetching IV: {e}")
        return None

@app.get("/")
def root():
    return {"message": "Delta Exchange Options API - FastAPI is working."}

@app.get("/options/instruments")
def instruments():
    instruments_data = get_instruments()
    return {"instruments": instruments_data}

@app.get("/options/chain")
def option_chain():
    chain = get_option_chain()
    return {"option_chain": chain}

@app.get("/options/iv")
def iv_rank(symbol: str = "BTCUSD"):
    rank = get_iv_rank(symbol)
    return {"symbol": symbol, "iv": iv}

@app.get("/options-alpha")
def options_alpha():
    instruments_data = get_instruments()
    chain = get_option_chain()
    iv = get_iv()

    return {
        "instruments": instruments_data[:5],  # send partial data for readability
        "option_chain": chain[:5],
        "iv": iv
    }
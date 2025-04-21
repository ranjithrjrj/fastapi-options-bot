from fastapi import FastAPI import requests import os from typing import List

app = FastAPI()

DELTA_API_KEY = os.getenv("DELTA_API_KEY") DELTA_API_SECRET = os.getenv("DELTA_API_SECRET") HEADERS = { "api-key": DELTA_API_KEY, "api-secret": DELTA_API_SECRET }

BASE_URL = "https://api.delta.exchange"

def fetch_option_chain(): try: response = requests.get(f"{BASE_URL}/v2/options/chains") return response.json().get("result", []) except Exception as e: print(f"Error fetching option chain: {e}") return []

def extract_top_vega(chain: List[dict], option_type: str, top_n=10): filtered = [item for item in chain if item.get("option_type") == option_type and item.get("vega") is not None] sorted_options = sorted(filtered, key=lambda x: x["vega"], reverse=True) return [ { "strike_price": opt["strike_price"], "expiry": opt["expiry_date"], "vega": opt["vega"] } for opt in sorted_options[:top_n] ]

@app.get("/options/high-vega") def high_vega_options(): chain = fetch_option_chain() top_calls = extract_top_vega(chain, "call") top_puts = extract_top_vega(chain, "put") return { "top_calls_by_vega": top_calls, "top_puts_by_vega": top_puts }


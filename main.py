from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import hmac
import hashlib
import time
import requests

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")
BASE_URL = "https://api.delta.exchange"

app = FastAPI(title="Delta Options Alpha API")


def generate_signature(http_method, endpoint_path, expiry, request_body=""):
    message = f"{http_method}{endpoint_path}{expiry}{request_body}"
    return hmac.new(
        API_SECRET.encode(), message.encode(), hashlib.sha256
    ).hexdigest()


def delta_authenticated_request(http_method, endpoint_path, params=""):
    url = BASE_URL + endpoint_path
    expiry = str(int(time.time()) + 30)
    signature = generate_signature(http_method, endpoint_path, expiry, params)

    headers = {
        "api-key": API_KEY,
        "signature": signature,
        "expiry": expiry,
        "Content-Type": "application/json"
    }

    if http_method == "GET":
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, data=params)

    return response.json()


@app.get("/")
def root():
    return {"status": "Delta Options Alpha API is running"}


@app.get("/option-chain/{symbol}")
def get_option_chain(symbol: str = "BTCUSD"):
    endpoint = f"/v2/options/chain?underlying={symbol}"
    try:
        response = delta_authenticated_request("GET", endpoint)
        return JSONResponse(content=response)
    except Exception as e:




    print(f"An error occurred: {e}")
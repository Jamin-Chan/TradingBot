
import requests
import alpaca_trade_api as tradeapi

from config import API_KEY
from config import SECRET_KEY


# Replace these with your own API key and secret

BASE_URL = 'https://paper-api.alpaca.markets'   # Use 'https://api.alpaca.markets' for live trading
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')



#r = requests.get(ACCOUNT_URL, headers=HEADERS)

account = api.get_account()
print(account)


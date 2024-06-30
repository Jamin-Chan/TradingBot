
import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import time, requests, datetime, json


from config import API_KEY
from config import SECRET_KEY


# Replace these with your own API key and secret

BASE_URL = 'https://paper-api.alpaca.markets'   # Use 'https://api.alpaca.markets' for live trading
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


# Initialize the Alpaca API
try:
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
except:
    print("URL error")


symbol = 'BTCUSD'
dataSymbol = 'BTC/USD'
short_ma_length = 50
long_ma_length = 200
percent_of_equity = 0.25

def getAccountInfo():
    try:
        # Initialize the Alpaca API
        api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

        # Get account information
        account = api.get_account()

        # Print account details
        print("Account ID:", account.id)
        print("Account Status:", account.status)
        print("Currency:", account.currency)
        print("Cash:", account.cash)
        print("Buying Power:", account.buying_power)
        print("Equity:", account.equity)
        print("Last Equity:", account.last_equity)
        print("Portfolio Value:", account.portfolio_value)
        print("Initial Margin:", account.initial_margin)
        print("Maintenance Margin:", account.maintenance_margin)
        print("Short Market Value:", account.short_market_value)
        print("Long Market Value:", account.long_market_value)

    except tradeapi.rest.APIError as e:
        print("API Error:", e)


def buy_stock(symbol, qty):
    try:
        # Place a market order to buy the specified quantity of the stock
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Buy order for {qty} shares of {symbol} placed successfully.")
        return order
    except tradeapi.rest.APIError as e:
        print(f"API Error: {e}")
        return None



def sell_stock(symbol, qty):
    try:
        # Place a market order to sell the specified quantity of the stock
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print(f"Sell order for {qty} shares of {symbol} placed successfully.")
        return order
    except tradeapi.rest.APIError as e:
        print(f"API Error: {e}")
        return None



def getMarketData(symbol):
    now = datetime.datetime.now(datetime.UTC)
    print(now)
    startTime = now - datetime.timedelta(hours=5)
    converted_datetime_str = startTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(converted_datetime_str)

    #url = "https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols={symbol}&start={}&end={now}&limit=1000&sort=asc"
    #url = f'https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols={symbol}'
    url = f'https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols={symbol}&start={converted_datetime_str}&timeframe=5Min&limit=1000&sort=asc'

    headers = {
        "accept": "application/json",
        #"APCA-API-KEY-ID": API_KEY,
        #"APCA-API-SECRET-KEY": SECRET_KEY
    }
    response = requests.get(url, headers=headers)
    marketData = json.loads(response.text)
    # c = closing, h = high, l = low, n = no idea, o = opening, t = time, v = volume, vw = volume weighted/vwap
    for i in marketData["bars"][symbol]:
        print(i)
    # goal, get ema and make changes based on ema
    return None


#buy_stock(symbol, 1)
#sell_stock(symbol, 1)
getMarketData(dataSymbol)
#getAccountInfo()
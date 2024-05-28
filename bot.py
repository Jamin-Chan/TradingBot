
import requests
import alpaca_trade_api as tradeapi

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
    

buy_stock("AAPL", 100)
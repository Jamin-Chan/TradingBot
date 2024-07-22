
import alpaca_trade_api as tradeapi
import pandas as pd
import pandas_ta as ta
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import time, requests, datetime, json


from config import API_KEY
from config import SECRET_KEY


# Replace these with your own API key and secret
# REMEMBER THIS IS PAPER FOR NOW
BASE_URL = 'https://paper-api.alpaca.markets'   # Use 'https://api.alpaca.markets' for live trading
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


# Initialize the Alpaca API
try:
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
except:
    print("URL error")


symbol = 'BTCUSD'  #for orders and buy and sell
dataSymbol = 'BTC/USD' #for getting the data for this symbol
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
    startTime = now - datetime.timedelta(hours=48)
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
    j=0
    for i, item in enumerate(reversed(marketData["bars"][symbol])):
        j+=1
        item['index'] = j
    # is this not the stupid candel headass data LOOK HERE LOOK HERE LOOK HERE
    #
    for i in marketData["bars"][symbol]:
        print(i)
    # goal, get ema and make changes based on ema

    #creates the graph for the data retrived
    creatCandleStickgraph(marketData["bars"][symbol])
    return marketData


def creatCandleStickgraph(data):
    df = pd.DataFrame(data)
    df.rename(columns={'t': 'Date', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'}, inplace=True)

    #ema
    df["EMA_slow"]=ta.ema(df.Close, length=20)
    df["EMA_fast"]=ta.ema(df.Close, length=10)
    

    #rsi
    df['RSI']=ta.rsi(df.Close, length=10)

    #bollinger bands
    #my_bbands = ta.bbands(df.Close, length=15, std=1.5)
    #df=df.join(my_bbands)
    df[['lower_band', 'mid', 'upper_band' ]] = ta.bbands(df.Close, length=20, std=2).iloc[:, :3]
    
    #plotting
    addplot = [
        mpf.make_addplot(df['EMA_slow'], color='blue', secondary_y=False),
        mpf.make_addplot(df['EMA_fast'], color='red', secondary_y=False),
        mpf.make_addplot(df['RSI'], panel=1, color='black', secondary_y=False),
        mpf.make_addplot(df['lower_band'], color = 'green'),
        #mpf.make_addplot(df['mid'], color = 'yellow'),
        mpf.make_addplot(df['upper_band'], color = 'orange')
    ]

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    print("this is df")
    print(df)
    mpf.plot(df, type='candle', style='charles', title=f'Candlestick Chart {symbol}', ylabel='Price', volume=False, addplot=addplot, panel_ratios=(2,1))

    plt.show()
    return(df)


def getCurrentCandle(df, symbol):
    for item in df["bars"][symbol]:
        currentCandle = item
        #print(currentCandle)
    print(f"this is what it print")
    print(currentCandle)

    return currentCandle 

def getBackCandles(df, symbol):
    backCandles = []
    for item in df["bars"][symbol]:
        backCandles.append(item)
        #print(backCandles)

        if(len(backCandles) > 21):
            backCandles.pop(0)
    
    backCandles.pop() #get rid of current candle
    print(f"this is what it print (backcandles)")
    for candles in backCandles:
        print(candles)

    return backCandles 

#checks whether the candles crosses both ema lines
def EMAIndicator(current_candle, backcandles):
    if(current_candle["EMA_slow"] > current_candle["low"] & current_candle["EMA_fast"] > current_candle["low"]):
        print("both lines are lower than the lowest point")
    

    return None


#checks whether the candles crosses or touches the bollinger bands indicating bounces
def BBIndicator(current_candle, backcandles):
    return None




def finalIndicator(current_candle, backcandles):
    if(BBIndicator(current_candle, backcandles) == 1 & EMAIndicator(df, current_candle, backcandles) == 1):
        print("buy")


#creates the stop loss and take profit after buying in 
#(past 20 candles, lowest point is stop loss)
def setSLTP():
    return None



#buy_stock(symbol, 1)
#sell_stock(symbol, 1)
df = getMarketData(dataSymbol)
#getCurrentCandle(df, dataSymbol)
getBackCandles(df, dataSymbol)
#getAccountInfo()
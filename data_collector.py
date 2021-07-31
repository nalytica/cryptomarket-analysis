# LINK TO THE ORIGINAL CREATOR:
# - https://github.com/pythonlessons/RL-Bitcoin-trading-bot/blob/main/RL-Bitcoin-trading-bot_6/Download.py

import bitfinex
import time
import datetime
import pandas as pd

# Defining the query parameters
pair = 'BTCUSD'
timeframe = '1m'# '4h' '1h' '15m' '1m'
timeframe_sec = 60 # seconds

# Defining the start date
t_start = datetime.datetime(2013, 3, 31, 0, 0) # years, month, day, hour, minute
t_start = time.mktime(t_start.timetuple()) * 1000

# Define the end date
t_stop = datetime.datetime(2021, 7, 30, 0, 0)
t_stop = time.mktime(t_stop.timetuple()) * 1000

def fetch_data(start, stop, symbol, interval, timeframe_sec):
    limit = 1000    # We want the maximum of 1000 data points
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    hour = timeframe_sec * 1000
    step = hour * limit
    data = []

    total_steps = (stop-start)/hour
    while total_steps > 0:
        if total_steps < limit: # recalculating ending steps
            step = total_steps * hour

        end = start + step
        data += api_v2.candles(symbol=symbol, interval=interval, limit=limit, start=start, end=end)
        print(pd.to_datetime(start, unit='ms'), pd.to_datetime(end, unit='ms'), "steps left:", total_steps)
        start = start + step
        total_steps -= limit
        time.sleep(1.5)
    return data

result = fetch_data(t_start, t_stop, pair, timeframe, timeframe_sec)
names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
df = pd.DataFrame(result, columns=names)
df.drop_duplicates(inplace=True)
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)
df.to_csv(f"{pair}_{timeframe}.csv") # df.to_csv(f"{pair}_training_data_{timeframe}.csv")




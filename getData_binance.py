
# -------------------- Get Date time ----------------------
import datetime
Previous_Date = datetime.datetime.today() - datetime.timedelta(days=7)
format = "%Y-%m-%dT%H:%M:%S.%fZ"
time1 = Previous_Date.strftime(format)

# -----------------------------------------------------------

# -*- coding: utf-8 -*-

import os
import sys
import csv
import sys

# -----------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

# -----------------------------------------------------------------------------

def retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    num_retries = 0
    try:
        num_retries += 1
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    now = exchange.milliseconds()
    all_ohlcv = []
    fetch_since = since
    while fetch_since < now:
        ohlcv = retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
        all_ohlcv = all_ohlcv + ohlcv
        if len(all_ohlcv):
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to', exchange.iso8601(all_ohlcv[-1][0]))
        else:
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(fetch_since))
    return exchange.filter_by_since_limit(all_ohlcv, since, None, key=0)


def write_to_csv(filename, data):
    with open(filename, mode='w') as output_file:
        # create Header
        csv_writer = csv.DictWriter(output_file, fieldnames = ["timestamp", "open", "high", "low", "close", "volume"])
        csv_writer.writeheader()

        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(data)


def scrape_candles_to_csv(filename, exchange_id, max_retries, symbol, timeframe, since, limit):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,  # required by the Manual
    })
    # convert since from string to milliseconds integer if needed
    if isinstance(since, str):
        since = exchange.parse8601(since)
    # preload all markets from the exchange
    exchange.load_markets()
    # fetch all candles
    ohlcv = scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit)

    # save them to csv file
    write_to_csv(filename, ohlcv)
    print('Saved', len(ohlcv), 'candles from', exchange.iso8601(ohlcv[0][0]), 'to', exchange.iso8601(ohlcv[-1][0]), 'to', filename)


# total arguments
n = len(sys.argv)
# print("Total arguments passed:", n)

# Arguments passed
# print("\nName of Python script:", sys.argv[0])

# symbol = 'VET/USDT'
symbol = sys.argv[1]

scrape_candles_to_csv('binance.csv', 'binance', 3, symbol, '1h', time1, 100)


# cmd = 'python binance-fetch-ohlcv-to-csv.py'

# # Using os.system() method
# os.system(cmd)
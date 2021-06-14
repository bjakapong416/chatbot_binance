import ccxt  # noqa: E402
import sys


binance = ccxt.binance()

symbol = sys.argv[1]
timeframe = '4h'

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle


def print_chart(exchange, symbol, timeframe):

    # print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

    # get a list of ohlcv candles
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    # print(len(ohlcv))
    # get the ohlCv (closing price, index == 4)
    series = [x[index] for x in ohlcv]


    # if (count%60 == 0):
        # print the chart
        # print("\n" + plot(series[-length:], {'height': height}))  # print the chart


    last = ohlcv[len(ohlcv) - 1][index]  # last closing price
    return last

last = print_chart(binance, symbol, timeframe)
print(last)
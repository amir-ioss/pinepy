from datetime import datetime
from time import sleep
from ohlcv import Ohlcv
import talib
import asyncio
import json
import calendar
import pandas as pd
import client
from log import p 
from markets import markets
import websockets
 
f = open('sample.json')
data = json.load(f)


sum = []

def pine_rma(src, length):
    alpha = 1/length

    # sum = 0.0

    # sum := na(sum[1]) ? ta.sma(src, length) : alpha * src + (1 - alpha) * nz(sum[1])

        # p("---------", item[0])
    global sum
    if not sum:
            # ta.sma(src, length)
            p("ta.sma(src, length)")
            sum = [1, 2, 3]
            pass    
    else:
            nz = sum[-1] if sum[-1] != None else 0
            f = alpha * src + (1 - alpha) * nz
            sum.append(f)
            # alpha * src + (1 - alpha) * nz(sum[1])
            pass

    return sum

# p(pine_rma(0.65, 15))
for item in data:
    # p(pine_rma(item[4], 15))
    pine_rma(item[4], 15)
    pass
p(sum)
# for item in data:
#     rsiLengthInput = 14
#     # rsiSourceInput = item[4]
#     rsiSourceInput = 20100.1
#     up = pine_rma(rsiSourceInput, rsiLengthInput)

#     p(up, rsiSourceInput)


# rsiLengthInput = input.int(14, minval=1, title="RSI Length", group="RSI Settings")
# rsiSourceInput = input.source(close, "Source", group="RSI Settings")
# maTypeInput = input.string("SMA", title="MA Type", options=["SMA", "Bollinger Bands", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group="MA Settings")
# maLengthInput = input.int(14, title="MA Length", group="MA Settings")
# bbMultInput = input.float(2.0, minval=0.001, maxval=50, title="BB StdDev", group="MA Settings")

# up = ta.rma(math.max(ta.change(rsiSourceInput), 0), rsiLengthInput)
# down = ta.rma(-math.min(ta.change(rsiSourceInput), 0), rsiLengthInput)
# rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

# //@version=5
# indicator("ta.rma")
# plot(ta.rma(close, 15))

# //the same on pine
# pine_rma(src, length) =>
# 	alpha = 1/length
# 	sum = 0.0
# 	sum := na(sum[1]) ? ta.sma(src, length) : alpha * src + (1 - alpha) * nz(sum[1])
# plot(pine_rma(close, 15))
  
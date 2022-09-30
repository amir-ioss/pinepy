import math
import numpy as np

arr= [
 0.1
,0.4291
,0.428
,0.4289
,0.4284
,0.4299
,0.4284
,0.4275
,0.4272
,0.500]

array = ["nan",0.414525
 ,0.416575 ,.408225
 ,0.4059   ,.397175 ,.390325
 ,0.390675 ]

def highest(src, length = 1):
    _flip = np.flip(src)
    result = max(_flip[:length+1])
    # print("arr for highest->", _flip[:length+1])
    return result

def lowest(src, length = 1):
    _flip = np.flip(src)
    result = min(_flip[:length+1])
    # print("arr for highest->", _flip[:length+1])
    return result

# play

# print(highet(arr, 2))
# print(lowest(arr, 2))

# longStopPrev = nz(longStop[1], longStop) 
# longStop = ["nan"]
# longStopPrev = longStop[-1] if math.isnan(float(longStop[-2])) else longStop[-2] 
# print(longStopPrev)


# print(highest(array, 20))

# for idx in range(len(arr)):
#     print(arr[:idx+1])
#     pass

# print(len(arr))

def wwma(values, n):
    """
    J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

def atr__(df, n=22):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

# pine_rma(src, length) =>
# 	alpha = 1/length
# 	sum = 0.0
# 	sum := na(sum[1]) ? ta.sma(src, length) : alpha * src + (1 - alpha) * nz(sum[1])

# //the same on pine
# pine_ema(src, length) =>
#     alpha = 2 / (length + 1)
#     sum = 0.0
#     sum := na(sum[1]) ? src : alpha * src + (1 - alpha) * nz(sum[1])
# plot(pine_ema(close,15))

def pine_rma(df, length):
    data = df.copy()
    close = np.nan_to_num(data['Close'].to_numpy())
    sum = []
    alpha = 1/length

    for idx in range(len(data)):
    # for c in data['Close']:
        sum_ = sum;
        sumPrev = sum_[idx-1] if idx > 1 else 0
        result = alpha * close[idx] + (1 - alpha) * sumPrev
        sum_.append(result)
        # print(sumPrev)
    # print(sum_)    
    # print("ok")
    # alpha = 1/length
    # sum = 0.0
    # sum = alpha * src + (1 - alpha) * sum[1]
    return sum


def ema(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    # s = array(s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema

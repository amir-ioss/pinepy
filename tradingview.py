from tradingview_ta import TA_Handler, Interval, Exchange

tesla = TA_Handler(
    symbol="LUNCBUSD",
    screener="Crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)
# print(tesla.get_analysis().summary)
print(tesla.get_analysis().indicators)
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}
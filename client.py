import sys
import ccxt  

# exchange = ccxt.binance({
#     'apiKey': 'KrtAkDbOxGxovcGDORa1TmOduII7R5SgkbfxdxVJss0OZ4o7ylUKJOqwx1Jjubgb',
#     'secret': 'TDNzfpSmfX7l8lklaO5Ydq5Yvtq293PxGTStJeecwjD766VztgaxDxTWXj17w688',
#     'enableRateLimit': True,
# })
exchange = ccxt.binance()

# exchange.options = {'defaultType': 'delivery', 'adjustForTimeDifference': True}
# exchange.setSandboxMode(True)
# exchange.verbose = True  # ←---------------- ALWAYS ADD THIS IF YOU HAVE A PROBLEM

### market
markets = exchange.fetch_markets()
# print(markets)
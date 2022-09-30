import sys
import ccxt


class order:
    def __init__(self, symbol, type, side, amount, params={}):

        # type = 'market'  # or 'limit'
        # side = 'sell'
        # params = {
        #     # 'triggerPrice': 0.04132501,  # your stop price
        # }

        self.exchange = ccxt.binance({
            'apiKey': "KrtAkDbOxGxovcGDORa1TmOduII7R5SgkbfxdxVJss0OZ4o7ylUKJOqwx1Jjubgb",
            'secret': "TDNzfpSmfX7l8lklaO5Ydq5Yvtq293PxGTStJeecwjD766VztgaxDxTWXj17w688",
            'enableRateLimit': True,
        })
        self.exchange.setSandboxMode(True)


        print(symbol, type, side, amount)
        order = self.exchange.create_order(symbol, type, side, amount)
        # print("order => ", order)


        ### check balance
        try:
            # balances = self.exchange.fetch_balance()
            # print(balances['free']) # total 
            assetbalance = (self.exchange.fetch_free_balance()["USDT"])
            print("USDT ------------------------------------------- : ", assetbalance)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
        

        pass


amount = 203.17730983
symbol = 'TRX/USDT' 
# order = order(symbol, 'market', 'buy', amount , {})
# order = order(symbol, 'market', 'sell', amount , {})

# my balance on 29
# {'BNB': 1000.0, 'BTC': 1.0, 'BUSD': 10000.0, 'ETH': 100.0, 'LTC': 500.0, 'TRX': 500000.0, 'USDT': 10000.0, 'XRP': 50000.0}

# usdt balance 9999.984385
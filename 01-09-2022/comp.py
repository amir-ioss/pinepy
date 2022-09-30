from cmath import log
import json
from exchanges import exchanges 


# gen_coins= open('coins.json')
# array_ = json.load(gen_coins)
# gen_coins.close()


def _genKey():
  keys = []
  for x in exchanges:
    keys.append(x)
  return keys


# for test
array = [
  {
    "binance": [
      { "ex": 'BTC/USDT', "close": 1.58 },
      { "ex": 'LUNA/USDT', "close": 2.01 },
    ],
  },
  {
    "wazirx": [
      { "ex": 'BTC/USDT', "close": 3.58 },
      { "ex": 'LUNA/USDT', "close": 4.016 },
    ],
  },
  {
    "kucoin": [
      { "ex": 'BTC/USDT', "close": 5.58 },
      { "ex": 'LUNA/USDT', "close": 7.03 },
    ],
  },
]

keys = _genKey()

def getCoins():
        # output
        coll = []

        for ex in exchanges:
            exchange = exchanges[ex]
            # print("--------------", ex)
            if (exchange.has['fetchTickers']):
                fetchTickers = exchange.fetchTickers()
                fetchTickers_dumps = json.dumps(fetchTickers)
                data = json.loads(fetchTickers_dumps)
                tickers = []
                for key, value in data.items():
                    # print(";;;", "/" in value['symbol'])
                    if( "/" in value['symbol']):
                        if (value['close'] == 0): continue
                        if (value['symbol'].split('/')[1] != 'USDT'): continue
                        
                        tickers.append({
                        "ex": value['symbol'],
                        "close":value['close'],
                        })
                # print("-->",tickers)
                coll.append({ex: tickers })
            else:
                print('no Tickets')

        # print('all coins--->', coll)
        return coll
# END main()

gen_all_ex_coins = getCoins()
def markets():
        # OUT
        markets = []
        output =  {}

        # Check is coin already pushed to output Dic 
        def existing(val):
            bool = False
            for coin in output:
                if (coin == val): bool = True
            return bool



        for idx, coins in enumerate(gen_all_ex_coins):
            for coin in coins[keys[idx]]:
                if(existing(coin['ex'])):
                    output[coin['ex']]  =  {**output[coin['ex']],keys[idx]: {'close': coin['close']}}
                else:
                    output[coin['ex']] = {keys[idx]: {'close': coin['close']}}

        # print(output)
        
        
        # PAHSE 2

        diff = 1
        coinMinPrice = 1
        for idx, pairs in enumerate(output):
            low = { 'exchange': '', 'price': 0 }
            high = { 'exchange': '', 'price': 0 }
            isPair = len(output[pairs]) > 1
            # print("---------------")
            if(isPair):
                for idx, exchange in enumerate(output[pairs]):
                    ex_close=output[pairs][exchange]['close']

                    if (low['price'] > ex_close):
                        low['price'] = ex_close
                        low['exchange'] = exchange
                    
                    if (idx == 0):
                        low['price'] = ex_close
                        low['exchange'] = exchange
                    
                    if (high['price'] < ex_close):
                        high['price'] = ex_close
                        high['exchange'] = exchange
            
            ex_diff =  high['price']  -  low['price'] 
            isProfitable = ex_diff > diff
            isMinPrice =  low['price'] < coinMinPrice

            # OUT
            if(isPair and isProfitable ):
              # print(pairs, '---------', low['price'], '-', low['exchange'], ' | ',high['price'],  '+',  high['exchange'], ' | <-->',ex_diff)
              markets.append({"pair": pairs, "low":low, "high": high, "diff": ex_diff })

        return markets
    

# print(markets())
# getCoins()


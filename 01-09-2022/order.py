import ccxt, asyncio, io, json
from binance.client import Client, AsyncClient



class Order:
    # exchange = ccxt.binance({
    # 'apiKey': 'Zm736zqFfeUpi2n2wRCIt0TIzIpl9rUm3gYZDndj382iSz4V9tbh5LBU1udtDdMo',
    # 'secret': '7xD8hcp2NleymDO5EQ2UCIbg3D07xBN50xfgxi9du0JYeVBEHZA1fE7kw6xkNlRC',
    # })
    api_key = 'Zm736zqFfeUpi2n2wRCIt0TIzIpl9rUm3gYZDndj382iSz4V9tbh5LBU1udtDdMo'
    api_secret = '7xD8hcp2NleymDO5EQ2UCIbg3D07xBN50xfgxi9du0JYeVBEHZA1fE7kw6xkNlRC'

    # client = Client(api_key, api_secret, testnet=True)

    symbol = 'ETH/BTC'
    type = 'market'  # or 'market'
    side = 'buy'  # or 'buy'
    amount = 1.0
    price = 0.060154  # or None

    # extra params and overrides if needed
    params = {
        'test': True,  # test if it's valid, but don't actually place it
    }

    # order = client.create_order(symbol, type, side, amount, price, params)

    # order = client.create_test_order(
    # symbol='BNBBTC',
    # side=side,
    # type=type,
    # quantity=1.0)

    # print(order)
    # print(client)


    async def main(self):
        client = await AsyncClient.create(self.api_key, self.api_secret, testnet=True)


        # fetch exchange info
        # res = await client.get_exchange_info()
        # print(json.dumps(res, indent=2))

        # bal = await client.get_asset_balance("BUSD")
        # print(bal)

        order = await client.create_order(
            symbol='BNBBUSD',
            side=self.side,
            type=self.type,
            # timeInForce='GTC',
            quantity=10.0,
            # price='0.00001'
        )

        print(order)

        # stat = await client.get_order(
        #     symbol='BNBBTC',
        #     orderId='2087364')

        # print(stat)


        await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Order().main())

from core.bitmex import BinanceAPI

cd = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT',
      'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT']

client = BinanceAPI()
# priv_client = BinanceAPI()
client.klines('BTCUSDT', interval=15)
def compare_intersect(x, y):
    return frozenset(x).intersection(y)

def ticker_data():
    j = []
    for f in client.allPrices():
        dj = [f['price'], f['symbol']]
        if len(list(compare_intersect(dj, cd))) > 0:
            j.append([f['symbol'], f['price']])
    print(j)
    return j

p = (client.klines('BTCUSDT', interval='15m')[-1],)


while True:

    x = client.allBookTickers()
    for d in ticker_data():
        print(d)


    import time
    time.sleep(0)



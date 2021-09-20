from os.path import join, dirname
from core.binance import Api
from binance import client
import telegram
from telegram import Bot

bot = Bot(token='620369180:AAF58K-FUyB1E5L-AwEdp6D7GFciRNxEYJw')

binance_api_key = 'luWhzpyWDB1IBghvGJ68HQe3Id89XJEKlj6AFYSm5TZZIaGcmqf1dFiS2mln1Lw1'
binance_api_secret = 'z5XsPQgkkL1ada18GS50wZAk1b2LHfq4IVKRYnA6afjCDJdGq8dfWAHeMRTmaUS5S'
binance = Api(key = binance_api_key , secret = binance_api_secret)

binance_conn = client.Client(api_key=binance_api_key, api_secret=binance_api_secret)
d = {
    'symbol':'BTCUSDT',
    'side':'SELL',
    'type':'LIMIT',
    'quantity':'0.0001',
    'rate':'7500'
}

print(binance_conn.order_limit_buy(timeInForce="GTC",params = d))
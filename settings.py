from os.path import join, dirname
from core.binance import Api
from binance import client
import telegram

bot = telegram.Bot(token='620369180:AAF58K-FUyB1E5L-AwEdp6D7GFciRNxEYJw')

binance_api_key = 'luWhzpyWDB1IBghvGJ68HQe3Id89XJEKlj6AFYSm5TZZIaGcmqf1dFiS2mln1Lw1'
binance_api_secret = 'z5XsPQgkkL1ada18GS50wZAk1b2LHfq4IVKRYnA6afjCDJdGq8dfWAHeMRTmaUS5S'
binance = Api(key = binance_api_key , secret = binance_api_secret)



##############################################
pairs=[
    ['BTCUSDT', 75],['ETHUSDT', 7],['EOSUSDT', 0.45],
    ['ONTUSDT', 0.22],['NEOUSDT', 0.5],#['XRDUSDT', 0.016],
    ['BCCUSDT', 30],['VETUSDT', 4.5e-4],['ETCUSDT', 0.5],
    ['TRXUSDT', 4.5e-4],['ADAUSDT', 7e-3],['LTCUSDT', 3.5],
    ['IOTAUSDT', 0.04],['ICXUSDT', 0.063],['XLMUSDT', 0.009]
]
period='15m'
limit=50

##############################################

# def create_database():
#     import sqlite3
#     conn = sqlite3.connect('trend_scalper.db')
#     c = conn.cursor()
#     c.execute(
#         "CREATE TABLE IF NOT EXISTS trend_trader (id integer primary key autoincrement, signal Text, Coin TEXT, time_date Text, price REAL, profit_pc REAL )"
#     )
#
#     conn.commit()
#     conn.close()
#
#
# project_root = join(dirname(__file__), 'trend_scalper.db')




##########################################################
#########         BUY ENTRY SETTINGS            ##########
##########################################################
buy_ema = 14
buy_entry_rsi = 50
# buy_entry_adx = 50
buy_entry_cci = 0
buy_entry_atr = 70
# buy_entry_momentum = 5


#########         BUY EXIT SETTINGS             ##########
buy_exit_cci = 50
buy_exit_momentum = -5

##########################################################
#########         SELL ENTRY SETTINGS            #########
##########################################################
sell_ema = 14
sell_entry_rsi = 50
sell_entry_cci = 0
# sell_entry_adx = 20
sell_entry_atr = 20
sell_entry_momentum = -5


#########         SELL EXIT SETTINGS            ##########

sell_exit_cci = 50
# sell_exit_momentum = 5



#########         BUY KEY LEVELS             ##########
cci_kl_ema = 14
# buy_ema = 14
# buy_entry_rsi = 50
# buy_entry_cci = 50
# buy_entry_dmi = 20
# buy_entry_momentum = 5



#########         SELL KEY LEVELS             ##########
# sell_ema = 14
# sell_entry_rsi = 50
# sell_entry_cci = 50
# sell_entry_dmi = 20
# sell_entry_momentum = -5



cci_period = 14
ema_periood = 14
rsi_period = 14
ndi_period = 14
pdi_period = 14
# adx_period = 14
moment_period = 14
atr_period = 14
atrp_period =14















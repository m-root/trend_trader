from settings import binance
class Candle(object):


    def data(self,pair, period, limit):

        candles = binance.klines(symbol=pair, interval=period, limit=limit)
        return [[float(d[1]) for d in candles], # Open = 0
                [float(d[2]) for d in candles], # High = 1
                [float(d[3]) for d in candles], # Low = 2
                [float(d[4]) for d in candles]  # Close = 3
                ]




'''
    cci.commodity_channel_index(close_data=, high_data=, low_data=, period=)
    cci.typical_price(close_data=, high_data=, low_data=)
    rsi.relative_strength_index(data=, period=)
    di.atr(close_data=, period=)
    di.average_directional_index(close_data=, high_data=, low_data=, period=)
    di.positive_directional_index(close_data=, high_data=, low_data=, period=)
    di.positive_directional_movement(high_data=, low_data=)
    di.negative_directional_index(close_data=, high_data=, low_data=, period=)
    di.negative_directional_movement(high_data=, low_data=)
    momentum.momentum(data=, period=)
    atr.average_true_range(close_data=, period=)
    
    
    
from pyti import commodity_channel_index as cci, \
    exponential_moving_average as ema, \
    relative_strength_index as rsi, \
    directional_indicators as di, \
    momentum,average_true_range as atr, \
    average_true_range_percent as atrp

import time
while True:
    d = Candle().data(pair='BTCUSDT', period='15m', limit=50)

    for j in d:
        print(j)

    #
    f = time.time()
    print('Commodity Channel Index \n{}'.format(cci.commodity_channel_index(close_data=d[3] , high_data=d[1], low_data=d[2], period=14)))
    print('exponential_moving_average \n{}'.format(ema.exponential_moving_average(data=d[3], period=14)))
    print('relative_strength_index \n{}'.format(rsi.relative_strength_index(data=d[3], period=14)))
    print('negative_directional_movement \n{}'.format(di.negative_directional_movement(high_data=d[1], low_data=d[2])))
    print('negative_directional_index \n{}'.format(di.negative_directional_index(close_data=d[3] , high_data=d[1], low_data=d[2], period=14)))
    print('positive_directional_movement \n{}'.format(di.positive_directional_movement(high_data=d[1], low_data=d[2])))
    print('positive_directional_index \n{}'.format(di.positive_directional_index(close_data=d[3] , high_data=d[1], low_data=d[2], period=14)))
    print('average_directional_index \n{}'.format(di.average_directional_index(close_data=d[3] , high_data=d[1], low_data=d[2], period=14)))
    print('momentum \n{}'.format(momentum.momentum(data=d[3] , period=14)))
    print('average_true_range \n{}'.format(atr.average_true_range(close_data=d[3] , period=14)))
    print([fd for fd in atr.average_true_range(close_data=d[3] , period=14)][13:])
    print('average_true_range_percent \n{}'.format(atrp.average_true_range_percent(close_data=d[3] , period=14)))
    print('average_true_range_percent \n{}'.format(atrp.average_true_range_percent(close_data=d[3] , period=14)))
    print(time.time()-f)
    print()
    print()
    time.sleep(2)


#
# # cd = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT',
# #       'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT']
# # '''
#
# '''
#     [
#       [
#         1499040000000,      // Open time
#         "0.01634790",       // Open
#         "0.80000000",       // High
#         "0.01575800",       // Low
#         "0.01577100",       // Close
#         "148976.11427815",  // Volume
#         1499644799999,      // Close time
#         "2434.19055334",    // Quote asset volume
#         308,                // Number of trades
#         "1756.87402397",    // Taker buy base asset volume
#         "28.46694368",      // Taker buy quote asset volume
#         "17928899.62484339" // Ignore.
#       ]
#     ]
# '''
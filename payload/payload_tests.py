from datetime import datetime
import pytz
import telegram
from settings import bot
from core.ema import exponential_moving_average as ema
from core import binance_candles as bc
import settings
from pyti import commodity_channel_index as cci, \
    exponential_moving_average as ema, \
    relative_strength_index as rsi, \
    directional_indicators as di, \
    momentum,average_true_range as atr

buy_list = []
sell_list = []


####################################
#              PAYLOAD             #
####################################

class Payload(object):



    def __init__(self, pair, period, limit, quantity):
        self.pair = pair
        self.period = period
        self.limit = limit

        self.candle = bc.Candle().data(
            pair=self.pair,
            period=self.period,
            limit=self.limit
        )
        self.cci_data = cci.commodity_channel_index(
            close_data=self.candle[3],
            high_data=self.candle[1],
            low_data=self.candle[2],
            period=settings.cci_period
        )
        self.ema_data = ema.exponential_moving_average(
            data=self.candle[3],
            period=settings.ema_periood
        )

        self.rsi_data = rsi.relative_strength_index(
            data=self.candle[3],
            period=settings.rsi_period
        )

        self.adx_data = di.average_directional_index(
            close_data=self.candle[3],
            high_data=self.candle[1],
            low_data=self.candle[2],
            period=settings.adx_period
        )

        self.moment_data = momentum.momentum(
            data=self.candle[3],
            period=settings.moment_period
        )

        self.atr_data = atr.average_true_range(
            close_data=self.candle[3],
            period=settings.atr_period
        )


    ####################################
    #          BUY ENTRY LOGIC         #
    ####################################
    def buy_entry_logic(self):


        if self.cci_data > settings.buy_entry_cci \
                and self.candle[-1][-2] > self.ema_data[-2] \
                and self.rsi_data[-2] > settings.buy_entry_rsi \
                and self.adx_data[-2] > settings.buy_entry_adx \
                and self.moment_data[-2] > settings.buy_entry_momentum \
                and self.atr_data[-2] > settings.buy_entry_atr \
                and self.pair not in buy_list:




            telegram_message = 'Buy Entry : {} Price : {} Time {} Australia/Sydney time '\
                .format(
                self.pair,[float(fg[4]) for fg in self.candle][-1],
                str(datetime.now(pytz.timezone('Australia/Sydney'))
                    )
                )
            print(telegram_message)
            status = bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
                                      )
            print(status)

            buy_list.append(self.pair)
            if self.pair in sell_list:
                sell_list.remove(self.pair)

        if self.cci_data > settings.buy_entry_cci \
                and self.candle[-1][-2] > self.ema_data[-2] \
                and self.rsi_data[-2] > settings.buy_entry_rsi \
                and self.adx_data[-2] > settings.buy_entry_adx \
                and self.moment_data[-2] > settings.buy_entry_momentum \
                and self.atr_data[-2] > settings.buy_entry_atr:

            print('We are currently long on {}'.format(self.pair))

            if self.pair not in buy_list:
                buy_list.append(self.pair)

                if self.pair in sell_list:
                    sell_list.remove(self.pair)

    ####################################
    #          BUY EXIT LOGIC          #
    ####################################
    def buy_exit_logic(self):

        if self.cci_data > settings.buy_exit_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.moment_data[-2] < settings.buy_exit_momentum \
                and self.pair in buy_list:


            telegram_message = 'Buy Exit \t: {} Price : {} Time {} Australia/Sydney time ' \
                .format(
                self.pair, [float(fg[4]) for fg in self.candle][-1],
                str(datetime.now(pytz.timezone('Australia/Sydney'))
                    )
            )

            print(telegram_message)
            status = bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
            )
            print(status)



    ####################################
    #          SELL ENTRY LOGIC        #
    ####################################
    def sell_entry_logic(self):

        if self.cci_data[-2] < settings.sell_entry_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.rsi_data[-2] < settings.sell_entry_rsi \
                and self.adx_data[-2] < settings.sell_entry_adx \
                and self.moment_data[-2] < settings.sell_entry_momentum \
                and self.atr_data[-2] < settings.sell_entry_atr \
                and self.pair not in sell_list:



            telegram_message = 'Sell : {} Price : {} Time {} Australia/Sydney time '\
                .format(self.pair,
                        [float(fg[4]) for fg in self.candle][-1],
                        str(datetime.now(pytz.timezone('Australia/Sydney'))
                    )
                )

            print(telegram_message)
            status = bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
                                      )

            print(status)
            sell_list.append(self.pair)
            if self.pair in buy_list:
                buy_list.remove(self.pair)

        if self.cci_data[-2] < settings.sell_entry_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.rsi_data[-2] < settings.sell_entry_rsi \
                and self.adx_data[-2] < settings.sell_entry_adx \
                and self.moment_data[-2] < settings.sell_entry_momentum \
                and self.atr_data[-2] < settings.sell_entry_atr:

            print('We are currently short on {}'.format(self.pair))


            if self.pair not in sell_list:
                sell_list.append(self.pair)

                if self.pair in buy_list:
                    buy_list.remove(self.pair)



    ####################################
    #          SELL EXIT LOGIC         #
    ####################################

    def sell_exit_logic(self):

        if self.cci_data[-2] < settings.sell_exit_cci \
            and self.candle[-1][-2] > self.ema_data[-2] \
            and self.moment_data[-2] < settings.sell_exit_momentum:



            telegram_message = 'Sell Exit : {} Price : {} Time {} Australia/Sydney time '\
                .format(self.pair,
                        [float(fg[4]) for fg in self.candle][-1],
                        str(datetime.now(pytz.timezone('Australia/Sydney'))
                    )
                )

            print(telegram_message)
            status = bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
                                      )
            print(status)



'''
    import sqlite3
    from sqlite3 import Error
    import settings
    average_true_range_percent as atrp
    settings.create_database()
    conn = sqlite3.connect(settings.project_root)
    c = conn.cursor()
    average_directional_index(close_data, high_data, low_data, period):
    [id,currency, time, Low, High, Open, Close]
    from datetime import datetime
    import pytz
    str(datetime.now(pytz.timezone('US/Eastern')))
    from datetime import datetime
    import pytz
    print(str(datetime.now(pytz.timezone('US/Eastern'))))
    2018-08-04 14:56:44.463205-04:00
    # ndm_data = di.negative_directional_movement(high_data=candle[1], low_data=candle[2])
    # ndi_data = di.negative_directional_index(close_data=candle[3], high_data=candle[1], low_data=candle[2], period=settings.ndi_period)
    # pdm_data = di.positive_directional_movement(high_data=candle[1], low_data=candle[2]
    # atrp_data = atrp.average_true_range_percent(close_data=candle[3], period=settings.atrp_period)

'''
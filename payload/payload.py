from datetime import datetime
import pytz
import telegram
# from core import ema.exponential_moving_average as ema
from core import binance_candles as bc
import settings
from pyti import commodity_channel_index as cci, \
    exponential_moving_average as ema, \
    relative_strength_index as rsi, \
    directional_indicators as di, \
    momentum, \
    average_true_range as atr

buy_list = []
sell_list = []


####################################
#              PAYLOAD             #
####################################

class Payload(object):

    def __init__(self, pair,set_range):
        self.pair = pair
        self.set_range = set_range
        self.period = settings.period
        self.limit = settings.limit

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

        self.pdi_data = di.positive_directional_index(
            close_data=self.candle[3],
            high_data=self.candle[1],
            low_data=self.candle[2],
            period=settings.cci_period
        )

        self.ndi_data = di.negative_directional_index(
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

        self.moment_data = momentum.momentum(
            data=self.candle[3],
            period=settings.moment_period
        )

        self.atr_data = atr.average_true_range(
            close_data=self.candle[3],
            period=settings.atr_period
        )

    def telegram_print(self):

        # print('++++++++++++++++++++++++++++++++++++++++++')
        telegram_message = 'PAIR \t: {} \n' \
                           'CCI \t: {} \n' \
                           'RSI \t: {} \n' \
                           'ATR \t: {} \n' \
                           'PDI \t: {} \n' \
                           'NDI \t: {} \n' \
                           'MOM \t: {} \n'.format(

            self.pair,
            self.cci_data[-5:],
            self.rsi_data[-5:],
            self.atr_data[-5:],
            self.pdi_data[-5:],
            self.ndi_data[-5:],
            self.moment_data[-5:],
        )
        # print('++++++++++++++++++++++++++++++++++++++++++')
        # print()
        # print()



        settings.bot.send_message(chat_id="@crypto_signals_int",
                         text=telegram_message,
                         parse_mode=telegram.ParseMode.HTML
                         )

    def on_screen_print(self):

        screen_print = 'PAIR \t: {} \n' \
                           'CCI \t: {} \n' \
                           'RSI \t: {} \n' \
                           'ATR \t: {} \n' \
                           'PDI \t: {} \n' \
                           'NDI \t: {} \n' \
                           'MOM \t: {} \n'.format(

            self.pair,
            self.cci_data[-5:],
            self.rsi_data[-5:],
            self.atr_data[-5:],
            self.pdi_data[-5:],
            self.ndi_data[-5:],
            self.moment_data[-5:],
        )
        print(screen_print)



    def buy_logic(self):

        if self.cci_data[-2] > settings.buy_entry_cci \
                and self.candle[-1][-2] > self.ema_data[-2] \
                and self.rsi_data[-2] > settings.buy_entry_rsi \
                and self.atr_data[-2] > self.set_range \
                and self.pdi_data[-2] > self.ndi_data[-2] \
                and self.pair not in buy_list:

            # settings.Api.order_execution(symbol=self.pair, side=, type='LIMIT', quantity=, rate=)
            

            telegram_message = 'BINANCE SIGNAL : ENTER BUY : {} Price : {} Time {} Australia/Sydney time ' \
                .format(
                self.pair, [float(fg[4]) for fg in self.candle][-1],
                str(datetime.now(pytz.timezone('Australia/Sydney'))
                    )
            )

            status = settings.bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
            )
            
            self.telegram_print()
            
            print(status)

            buy_list.append(self.pair)
            if self.pair in sell_list:
                sell_list.remove(self.pair)

        if self.cci_data[-2] > settings.buy_entry_cci \
                and self.candle[-1][-2] > self.ema_data[-2] \
                and self.rsi_data[-2] > settings.buy_entry_rsi \
                and self.atr_data[-2] > self.set_range \
                and self.pdi_data[-2] > self.ndi_data[-2]:

            print('We are currently long on {}'.format(self.pair))

            if self.pair not in buy_list:
                buy_list.append(self.pair)

                if self.pair in sell_list:
                    sell_list.remove(self.pair)

        self.buy_exit_logic()

    ####################################
    #          BUY EXIT LOGIC          #
    ####################################
    def buy_exit_logic(self):

        if self.cci_data[-2] < settings.buy_entry_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.pdi_data[-2] < self.ndi_data[-2]\
                and self.pair in buy_list:

            # settings.Api.order_execution(symbol=self.pair, side=, type=, quantity=, rate=)
            if self.pair in buy_list:
                buy_list.remove(self.pair)

            telegram_message = 'BINANCE SIGNAL : EXIT BUY : {} Price : {} Time {} Australia/Sydney time ' \
                .format(self.pair,
                        [float(fg[4]) for fg in self.candle][-1],
                        str(datetime.now(pytz.timezone('Australia/Sydney'))
                            )
                        )

            status = settings.bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
            )
            self.telegram_print()
            print(status)

    ####################################
    #          SELL ENTRY LOGIC        #
    ####################################
    def sell_logic(self):

        if self.cci_data[-2] < settings.sell_entry_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.rsi_data[-2] < settings.sell_entry_rsi \
                and self.atr_data[-2] < settings.sell_entry_atr \
                and self.pdi_data[-2] < self.ndi_data[-2] \
                and self.pair not in sell_list:

            # settings.Api.order_execution(symbol=self.pair, side=, type=, quantity=, rate=)

            telegram_message = 'BINANCE SIGNAL : ENTER SELL : {} Price : {} Time {} Australia/Sydney time ' \
                .format(self.pair,
                        [float(fg[4]) for fg in self.candle][-1],
                        str(datetime.now(pytz.timezone('Australia/Sydney'))
                            )
                        )

            status = settings.bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
            )
            self.telegram_print()

            print(status)
            sell_list.append(self.pair)
            if self.pair in buy_list:
                buy_list.remove(self.pair)

        if self.cci_data[-2] < settings.sell_entry_cci \
                and self.candle[-1][-2] < self.ema_data[-2] \
                and self.rsi_data[-2] < settings.sell_entry_rsi \
                and self.atr_data[-2] < settings.sell_entry_atr \
                and self.pdi_data[-2] < self.ndi_data[-2]:

            print('We are currently short on {}'.format(self.pair))

            if self.pair not in sell_list:
                sell_list.append(self.pair)

                if self.pair in buy_list:
                    buy_list.remove(self.pair)

        self.sell_exit_logic()

    ####################################
    #          SELL EXIT LOGIC         #
    ####################################


    def sell_exit_logic(self):

        if self.cci_data[-2] < settings.sell_exit_cci \
                and self.candle[-1][-2] > self.ema_data[-2] \
                and self.pdi_data[-2] > self.ndi_data[-2]\
                and self.pair in sell_list:

            # settings.Api.order_execution(symbol=self.pair, side=, type=, quantity=, rate=)

            if self.pair in sell_list:
                sell_list.remove(self.pair)

            telegram_message = 'BINANCE SIGNAL : EXIT SELL : {} Price : {} Time {} Australia/Sydney time ' \
                .format(self.pair,
                        [float(fg[4]) for fg in self.candle][-1],
                        str(datetime.now(pytz.timezone('Australia/Sydney'))
                            )
                        )

            status = settings.bot.send_message(
                chat_id="@crypto_signals_int",
                text=telegram_message,
                parse_mode=telegram.ParseMode.HTML
            )
            self.telegram_print()
            print(status)

    def logic(self):
        self.on_screen_print()
        self.buy_logic()
        self.sell_logic()

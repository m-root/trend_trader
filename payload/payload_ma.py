from datetime import datetime
import pytz
import telegram
from settings import bot
from core.ema import exponential_moving_average as ema
import sqlite3
import settings
from sqlite3 import Error

settings.create_database()
conn = sqlite3.connect(settings.project_root)
c = conn.cursor()

buy_list = []
sell_list = []


class Payload:
    #
    # def __init__(self, pair):
    #     self.pair = pair

    def logic(self, pair, data_feed, current_price):
        '''
        average_directional_index(close_data, high_data, low_data, period):
        [id,currency, time, Low, High, Open, Close]



            from datetime import datetime
            import pytz
            str(datetime.now(pytz.timezone('US/Eastern')))
            from datetime import datetime
            import pytz
            print(str(datetime.now(pytz.timezone('US/Eastern'))))
            2018-08-04 14:56:44.463205-04:00
        '''
        ####################################
        #            BUY  SIGNALS          #
        ####################################

        if ema(data=data_feed, period=3)[-2] < ema(data=data_feed, period=6)[-2] and \
                ema(data=data_feed, period=3)[-1] > ema(data=data_feed, period=6)[-1] and pair not in buy_list:
            c.execute(
                "INSERT INTO trend_trader (signal , coin , time_date , price, profit_pc )VALUES (?,?, ?, ?, ?)",
                ('Buy', pair, str(datetime.now(pytz.timezone('US/Eastern'))), current_price, '')
            )
            conn.commit()

            telegram_message = 'Buy : {} Price : {} Time {} '.format(pair, current_price,
                                                                     str(datetime.now(pytz.timezone('US/Eastern'))))
            status = bot.send_message(chat_id="@crypto_signals_int",
                                      text=telegram_message,
                                      parse_mode=telegram.ParseMode.HTML
                                      )
            print(status)
            buy_list.append(pair)
            if pair in sell_list:
                sell_list.remove(pair)

        if ema(data=data_feed, period=3)[-2] < ema(data=data_feed, period=6)[-2] and \
                ema(data=data_feed, period=3)[-1] > ema(data=data_feed, period=6)[-1]:
            print('We are currently long on {}'.format(pair))

            if pair not in buy_list:
                buy_list.append(pair)

                if pair in sell_list:
                    sell_list.remove(pair)

        ####################################
        #            SELL SIGNALS          #
        ####################################

        if ema(data=data_feed, period=3)[-2] > ema(data=data_feed, period=6)[-2] and \
                ema(data=data_feed, period=3)[-1] < ema(data=data_feed, period=6)[-1] and pair not in sell_list:


            c.execute(
                "INSERT INTO trend_trader (signal , coin , time_date , price, profit_pc )VALUES (?,?, ?, ?, ?)",
                ('sell', pair, str(datetime.now(pytz.timezone('US/Eastern'))), current_price, '')
            )
            conn.commit()

            telegram_message = 'Sell : {}  Price : {} Time {} '.format(pair, current_price,
                                                                       str(datetime.now(pytz.timezone('US/Eastern'))))
            status = bot.send_message(chat_id="@crypto_signals_int",
                                      text=telegram_message,
                                      parse_mode=telegram.ParseMode.HTML
                                      )
            print(status)
            sell_list.append(pair)
            if pair in buy_list:
                buy_list.remove(pair)

        if ema(data=data_feed, period=3)[-1] < ema(data=data_feed, period=6)[-1]:
            print('We are currently short on {}'.format(pair))

            if pair not in sell_list:
                sell_list.append(pair)

                if pair in buy_list:
                    buy_list.remove(pair)
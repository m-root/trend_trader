from __future__ import absolute_import
from pyti import catch_errors
from pyti.function_helper import fill_for_noncomputable_vals
from six.moves import range


def exponential_moving_average(data, period):
    """
    Exponential Moving Average.

    Formula:
    p0 + (1 - w) * p1 + (1 - w)^2 * p2 + (1 + w)^3 * p3 +...
                /   1 + (1 - w) + (1 - w)^2 + (1 - w)^3 +...

    where: w = 2 / (N + 1)
    """
    catch_errors.check_for_period_error(data, period)
    emas = [exponential_moving_average_helper(
            data[idx - period + 1:idx + 1], period) for idx in range(period - 1, len(data))]
    emas = fill_for_noncomputable_vals(data, emas)
    return emas


def exponential_moving_average_helper(data, period):
    w = 2 / float(period + 1)
    ema_top = data[period - 1]
    ema_bottom = 1
    for idx in range(1, period):  # idx 1 to n
        ema_top += ((1 - w)**idx) * data[period - 1 - idx]
        ema_bottom += (1 - w)**idx
    ema = ema_top / ema_bottom
    return ema

'''

There are three steps to calculate the EMA. Here is the formula for a 5 Period EMA

1. Calculate the SMA

(Period Values / Number of Periods)

2. Calculate the Multiplier

(2 / (Number of Periods + 1) therefore (2 / (5+1) = 33.333%

3. Calculate the EMA

For the first EMA, we use the SMA(previous day) instead of EMA(previous day).

EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day)
'''

# ema_data = []
#
#
# def exponential_moving_average(data, period):
#
#     multiplier = 2 / (period + 1)
#
#     if len(ema_data) == 0:
#         ema = sum(data[-period:])
#         ema = ema / period
#         ema_data.append(ema)
#
#     elif len(ema_data) > 0:
#         print(ema_data)
#         print(data[-1])
#         print((data[-1] - ema_data[-1]))
#         print((data[-1] - ema_data[-1]) * multiplier)
#         print(ema_data[-1])
#         ema = ((data[-1] - ema_data[-1]) * multiplier) + ema_data[-1]
#         ema_data.append(ema)
#
#     return ema_data
# print(exponential_moving_average([4,5,6,7,8,9,5,6,7,8,9],4))
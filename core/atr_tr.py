from collections import deque
from datetime import timedelta



###################################################

from core import binance_candles as bc



###################################################



### TrueRange and AverageTrueRange classes ###

# FIXME: I'm not sure what the implications are of illiquid stocks. If a stock
# doesn't trade some minutes, how does that interact with the granularity of
# the True Range and Average True Range?

class TrueRange(object):
    """
    Valid granularities: minute, hour, day, week
    """

    def __init__(self, granularity='minute'):
        self.period_start = None
        self.high = None
        self.low = None
        self.close = None
        self.prev_close = None
        if granularity not in ('minute', 'hour', 'day', 'week'):
            raise Exception("Invalid granularity: %s" % granularity)
        self.granularity = granularity

    def periodIsOver(self, sid_data):
        if not self.period_start:
            return False
        if self.granularity == 'minute':
            return self.period_start != sid_data.datetime
        elif self.granularity == 'hour':
            return sid_data.datetime - self.period_start >= timedelta(hours=1)
        elif self.granularity == 'day':
            return self.period_start.date() != sid_data.datetime.date()
        else:
            return sid_data.datetime.date() - self.period_start.date() >= \
                   timedelta(7)

    def update(self, sid_data):
        """
        Update the True Range for the current period. For data to be
        correct, you must invoke this every time handle_data is called with
        data for the SID in question.
        """
        if self.period_start is None:
            # First time we're being called
            self.period_start = sid_data.datetime
            try:
                self.high = sid_data.high
                self.low = sid_data.low
                self.close = sid_data.close
            except KeyError:
                # Quantopian bug: high, low, close not set when building /
                # validing algorithm.
                pass
        elif self.periodIsOver(sid_data):
            # The current minute is the beginning of a new period
            self.period_start = sid_data.datetime
            self.prev_close = self.close
            self.high = sid_data.high
            self.low = sid_data.low
            self.close = sid_data.close
        else:
            # We still within the same period
            if self.high < sid_data.high:
                self.high = sid_data.high
            if self.low > sid_data.low:
                self.low = sid_data.low
            self.close = sid_data.close

    def get(self, sid_data=None):
        """
        Get the current True Range value. Optional pass in sid_data to update
        before you get (otherwise you can call update explicitly).
        """
        if sid_data:
            self.update(sid_data)
        if not self.period_start:
            raise Exception("TrueRange.get() called before update()")
        if self.prev_close is None:
            try:
                return self.high - self.low
            except TypeError:
                # Quantopian bug (see above)
                return 0
        return max((self.high - self.low),
                   abs(self.high - self.prev_close),
                   abs(self.low - self.prev_close))


class AverageTrueRange(object):
    """
    Arbitrary defaults: minute granularity, 60-minute window for ATR.
    """

    def __init__(self, granularity='minute', periods=60):
        self.history = deque(maxlen=periods)
        self.trueRange = TrueRange(granularity)
        if periods < 2 or int(periods) != periods:
            raise Exception("Invalid periods: %s" % periods)
        self.periods = periods

    def update(self, sid_data):
        """
        You need to call this every time data is available for SID in
        handle_data.
        """
        isNewPeriod = self.trueRange.periodIsOver(sid_data)
        trueRangeValue = self.trueRange.get(sid_data)
        if len(self.history):
            if not isNewPeriod:
                self.history.popleft()
            elif len(self.history) == self.periods:
                self.history.pop()
        if len(self.history) == self.periods - 1:
            # We don't actually need to save all the history once we've
            # "filled" the array the first time, since once we do that, the
            # ATR for each day incorporates the data from prior days, but the
            # code is simpler if we just go ahead and save it.
            self.history.appendleft((trueRangeValue +
                                     self.history[0] * (self.periods - 1)) /
                                    self.periods)
        else:
            self.history.appendleft(trueRangeValue)
            avg = sum(self.history) / len(self.history)
            self.history.popleft()
            self.history.appendleft(avg)

    def get(self, sid_data=None):
        """
        Call with optional SID data to update before getting.
        """
        if sid_data:
            self.update(sid_data)
        if not len(self.history):
            raise Exception("AverageTrueRange.get() called before update()")
        return self.history[0]


### End TrueRange and AverageTrueRange classes ###
#
#
# def initialize(context):
#     context.my_sid = sid(24)
#     # There is no special significance to these periods. They're just
#     # examples.
#     context.minuteATR = AverageTrueRange(granularity='minute', periods=60)
#     context.hourATR = AverageTrueRange(granularity='hour', periods=8)
#     context.dayATR = AverageTrueRange(granularity='day', periods=14)
#     context.weekATR = AverageTrueRange(granularity='week', periods=5)
#
#
# def handle_data(data, context):
#     if data.available(context.my_sid):
#         sid_data = data[context.my_sid]
#         minute = context.minuteATR.get(sid_data)
#         hour = context.hourATR.get(sid_data)
#         day = context.dayATR.get(sid_data)
#         week = context.weekATR.get(sid_data)
#         log.info("minute=%f, hour=%f, day=%f, week=%f" % (minute, hour, day, week))




def candle( pair, period, limit):
    pair = pair
    period = period
    limit = limit

    candle = bc.Candle().data(
        pair= pair,
        period=period,
        limit=limit
    )

while True:
    atr = AverageTrueRange()
    atr = atr.get(sid_data=)
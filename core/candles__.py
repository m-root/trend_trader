import dateutil.parser as dp
import ccxt


def candles():
    bitmex = ccxt.bitmex({})
    limit = 500  # their max is 500, default is 100 candles
    since = bitmex.milliseconds() - limit * 60 * 1000
    cash = ['BTC/USD', 'ETH/BTC']



    for money in cash:
        candles = bitmex.fetch_ohlcv(money, '5m', since, limit)

        cand = []
        g = []

        for f in candles:
            if float(dp.parse(bitmex.iso8601(f[0])).strftime("%M")) % 15 != 0:
                g.append([bitmex.iso8601(f[0])] + f[1:])

            if float(dp.parse(bitmex.iso8601(f[0])).strftime("%M")) % 15 == 0:
                g.append([bitmex.iso8601(f[0])] + f[1:])
                if len(g) == 1:
                    f = [bitmex.iso8601(f[0])] + f[1:]
                    # print(f)
                    # print("hello 1")

                    cand.append(f)
                    del g[:]

                elif len(g) == 2:
                    f = [g[1][0], g[0][1], max(g[0][2], g[1][2]), min(g[0][3], g[1][3]), g[1][4], sum([g[0][-1], g[1][-1]])]
                    # print(f)
                    # print("hello 2")
                    cand.append(f)
                    del g[:]

                elif len(g) == 3:

                    f = [g[2][0],
                         g[0][1],
                         max(g[0][2], g[1][2], g[2][2]),
                         min(g[0][3], g[1][3], g[2][3]),
                         g[2][4],
                         sum([g[0][-1], g[1][-1], g[2][-1]])]
                    # print(f)
                    # print("hello 3")
                    cand.append(f)
                    # print(g)
                    del g[:]

                # print(cand)
    return cand

import ccxt
bitmex = ccxt.bitmex({})
limit = 500  # their max is 500, default is 100 candles
since = bitmex.milliseconds() - limit * 60 * 1000
cash = ['BTC/USD', 'BTC/ADA', 'BCH/BTC', 'EOS/BTC', 'ETH/BTC', 'LTC/BTC', 'TRX/BTC', 'XRP/BTC']


print(bitmex.symbols)
print(candles())
#

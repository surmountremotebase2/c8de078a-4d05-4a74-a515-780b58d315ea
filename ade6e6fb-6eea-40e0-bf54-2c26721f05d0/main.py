from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "4hour"

    def run(self, data):
        d = data["ohlcv"]
        holdings = data["holdings"]

        if len(d) < 220:
            return None

        price = d[-1]["SPY"]["close"]

        ema20 = EMA("SPY", d, 20)[-1]
        ema50 = EMA("SPY", d, 50)[-1]
        sma200 = SMA("SPY", d, 200)[-1]
        rsi = RSI("SPY", d, 14)[-1]

        current = holdings.get("SPY", 0)

        buy_signal = (
            current == 0 and
            price > ema20 and
            ema20 > ema50 and
            ema50 > sma200 and
            rsi > 35 and
            rsi < 45
        )

        sell_signal = (
            current > 0 and
            (
                price < ema20 or
                rsi > 70 or
                ema20 < ema50
            )
        )

        if buy_signal:
            return TargetAllocation({"SPY": 1})

        if sell_signal:
            return TargetAllocation({"SPY": 0})

        return None
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "30minutes"

    def run(self, data):
        d = data["ohlcv"]
        holdings = data["holdings"]

        if len(d) < 60:
            return None

        price = d[-1]["SPY"]["close"]

        ema20 = EMA("SPY", d, 20)[-1]
        ema50 = EMA("SPY", d, 50)[-1]
        rsi = RSI("SPY", d, 14)[-1]

        current = holdings.get("SPY", 0)

        buy_signal = (
            current == 0 and
            ema20 > ema50 and
            price >= ema20 and
            rsi > 40 and
            rsi < 55
        )

        sell_signal = (
            current > 0 and
            (
                price < ema20 or
                rsi > 68
            )
        )

        if buy_signal:
            return TargetAllocation({"SPY": 1})

        if sell_signal:
            return TargetAllocation({"SPY": 0})

        return None
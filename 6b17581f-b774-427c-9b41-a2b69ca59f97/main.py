from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        holdings = data["holdings"]

        if len(d) < 60:
            return None

        price = d[-1]["QQQ"]["close"]

        ema20 = EMA("QQQ", d, 20)[-1]
        ema50 = EMA("QQQ", d, 50)[-1]
        rsi = RSI("QQQ", d, 14)[-1]

        current = holdings.get("QQQ", 0)

        buy_signal = (
            current == 0 and
            ema20 > ema50 and
            price >= ema20 and
            rsi > 42 and
            rsi < 58
        )

        sell_signal = (
            current > 0 and
            (
                price < ema20 or
                rsi > 72
            )
        )

        if buy_signal:
            return TargetAllocation({"QQQ": 1})

        if sell_signal:
            return TargetAllocation({"QQQ": 0})

        return None
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "4hours"

    def run(self, data):
        d = data["ohlcv"]

        if len(d) <= 220:
            return TargetAllocation({"SPY": 0})

        rsi = RSI("SPY", data, 14)
        ema20 = EMA("SPY", data, 20)
        ema50 = EMA("SPY", data, 50)
        sma200 = SMA("SPY", data, 200)
        price = d[-1]["SPY"]["close"]

        buy_signal = (
            price > ema20 and
            ema20 > ema50 and
            ema50 > sma200 and
            rsi > 35 and
            rsi < 45
        )

        sell_signal = (
            price < ema20 or
            rsi > 70 or
            ema20 < ema50
        )

        current = self.current_allocation.get("SPY", 0)

        if current == 0 and buy_signal:
            stake = 1
        elif current > 0 and sell_signal:
            stake = 0
        else:
            stake = current

        return TargetAllocation({"SPY": stake})
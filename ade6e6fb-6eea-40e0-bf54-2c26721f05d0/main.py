from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        holdings = data["holdings"]

        if len(d) < 120:
            return None

        price = d[-1]["SPY"]["close"]
        sma100 = SMA("SPY", d, 100)[-1]
        current = holdings.get("SPY", 0)

        if current == 0 and price > sma100:
            return TargetAllocation({"SPY": 1})

        if current > 0 and price < sma100:
            return TargetAllocation({"SPY": 0})

        return None
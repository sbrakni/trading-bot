import csv
from dataclasses import dataclass
from typing import List, Dict


def read_price_data(path: str) -> List[Dict[str, float]]:
    """Read CSV price data.

    The CSV file must contain ``Date`` and ``Close`` columns.
    """
    prices = []
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prices.append({"Date": row["Date"], "Close": float(row["Close"])})
    return prices


def moving_average(values: List[float]) -> float:
    return sum(values) / len(values)


def standard_deviation(values: List[float]) -> float:
    mean = moving_average(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return variance ** 0.5


@dataclass
class Trade:
    date: str
    side: str  # "BUY" or "SELL"
    price: float


class MeanReversionBot:
    """A simple mean reversion trading bot."""

    def __init__(self, cash: float = 10000.0, window: int = 5, num_std: float = 1.0):
        self.initial_cash = cash
        self.cash = cash
        self.window = window
        self.num_std = num_std
        self.holdings = 0
        self.trades: List[Trade] = []

    def run(self, prices: List[Dict[str, float]]):
        for i in range(self.window, len(prices)):
            window_prices = [p["Close"] for p in prices[i - self.window : i]]
            ma = moving_average(window_prices)
            std = standard_deviation(window_prices)
            price = prices[i]["Close"]
            date = prices[i]["Date"]

            lower_band = ma - self.num_std * std
            upper_band = ma + self.num_std * std

            if price < lower_band:
                self._buy(date, price)
            elif price > upper_band and self.holdings > 0:
                self._sell(date, price)

        final_price = prices[-1]["Close"]
        final_value = self.cash + self.holdings * final_price
        return {
            "final_value": final_value,
            "trades": self.trades,
        }

    def _buy(self, date: str, price: float):
        self.holdings += 1
        self.cash -= price
        self.trades.append(Trade(date, "BUY", price))

    def _sell(self, date: str, price: float):
        self.holdings -= 1
        self.cash += price
        self.trades.append(Trade(date, "SELL", price))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python mean_reversion.py <csv_file>")
        sys.exit(1)

    path = sys.argv[1]
    prices = read_price_data(path)
    bot = MeanReversionBot()
    result = bot.run(prices)

    for trade in result["trades"]:
        print(f"{trade.date}: {trade.side} at {trade.price}")
    print(f"Final portfolio value: {result['final_value']:.2f}")

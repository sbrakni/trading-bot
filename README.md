# Trading Bot

This repository contains a simple Python implementation of a mean reversion trading strategy.
The bot reads historical price data from a CSV file, generates buy/sell signals when prices
deviate from their recent moving average, and simulates portfolio performance.

## Usage

```
python mean_reversion.py data/sample_prices.csv
```

The script will output executed trades and the final portfolio value.

A small sample dataset is provided in `data/sample_prices.csv`.

## Testing

Run the unit tests using:
```
python -m unittest discover -s tests
```

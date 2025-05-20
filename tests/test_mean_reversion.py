import os
import unittest
from mean_reversion import read_price_data, MeanReversionBot


class MeanReversionTest(unittest.TestCase):
    def test_bot_executes_trades(self):
        data_path = os.path.join('data', 'sample_prices.csv')
        prices = read_price_data(data_path)
        bot = MeanReversionBot(window=3, num_std=0.5)
        result = bot.run(prices)
        self.assertGreater(len(result['trades']), 0)
        self.assertGreater(result['final_value'], 0)


if __name__ == '__main__':
    unittest.main()

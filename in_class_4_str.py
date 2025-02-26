import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sb

sb.set_theme()

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(1))
DEFAULT_END = dt.date.isoformat(dt.date.today())


class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data()

    def get_data(self):
        """method that downloads data and stores in a DataFrame"""
        data = yf.download(self.symbol, start=self.start, end=self.end)
        self.calc_returns(data)
        return data

    def calc_returns(self, df):
        """method that adds change and return columns to data"""
        df['returns'] = np.log(df.Close).diff().round(4)
        df['change'] = df['Close'].diff()
        df.dropna(inplace=True)


    def plot_return_dist(self):
        """method that plots instantaneous returns as histogram"""
        if self.data is not None:
            returns = self.calc_returns(self.data)['Daily Return'].dropna()
            plt.hist(returns, bins=20)
            plt.title(f"{self.symbol} Daily Return Distribution")
            plt.show()

    def plot_performance(self):
        """method that plots stock object performance as percent"""
        if self.data is not None:
            cumulative_returns = (1 + self.calc_returns(self.data)['Daily Return']).cumprod()
            plt.plot(cumulative_returns)
            plt.title(f"{self.symbol} Cumulative Returns")
            plt.show()


def main():
    test = Stock(symbol="MSFT")
    print(test.data)
    test.plot_performance()
    test.plot_return_dist()


if __name__ == '__main__':
    main()
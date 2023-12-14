import pandas as pd
from trading_simulator.portfolio.risk_engine import RiskEngine
import warnings
from data.database.sqlite_db import LocalDatabase
import time
from trading_simulator.portfolio.portfolio import Portfolio
from trading_simulator.market.trade import Trade

warnings.filterwarnings('ignore', category=RuntimeWarning)


class TradingSimulator:

    def __init__(self, trades_df):
        self.simulation_df = self.format_simulation_df(trades_df)
        self.current_index = 0

    def format_simulation_df(self, trades_df):
        # Create a column that shows PREV_CLOSE, so we can accurately calculate TOTAL_VALUE
        trades_df = trades_df.sort_values(['ticker', 'Time'])
        trades_df['prev_vwap'] = trades_df.groupby('ticker')['vwap'].shift(1)
        trades_df['prev_vwap'].fillna(trades_df['vwap'], inplace=True)
        trades_df.fillna(0, inplace=True)

        # Sort the DataFrame by 'Time' in descending order for each date
        trades_df = trades_df.sort_values(['Time'], ascending=[True]).reset_index()

        return trades_df

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.simulation_df):
            row = self.simulation_df.iloc[self.current_index]
            self.current_index += 1
            current_trade = Trade(row['Time'], row['ticker'], row['vwap'], row['volume'], pd.DataFrame([row]))

            return current_trade
        else:
            raise StopIteration


if __name__ == "__main__":
    df = pd.read_csv('./model/testing_df.csv')

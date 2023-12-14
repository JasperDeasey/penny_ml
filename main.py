import pandas as pd
from data.historical_data import historical_trade_gatherer
from model.random_forest_classifier import RandomForestModel
from data.database import sqlite_db
from trading_simulator.portfolio.risk_engine import RiskEngine
from trading_simulator.portfolio.portfolio import Portfolio
from trading_simulator.trading_simulator import TradingSimulator


# --- DATA ---
# All data is based off of minute-trading data from Polygon.io
# historical_data_gatherer.gather_historic_data() # <-- uncomment to if need to restart and get data again
db = sqlite_db.LocalDatabase()
historic_trades_df = db.query("SELECT * FROM historical_trades WHERE ticker == 2")
historic_trades_df['Time'] = pd.to_datetime(historic_trades_df['Time'])
historic_trades_df = historic_trades_df.sort_values(['Time'], ascending=[True]).reset_index()

# --- MODEL ---
# Create model, which predicts if a stock will go up or down 10% in the next 5 days
pre_2023_trades_training_df = historic_trades_df[historic_trades_df['Time'].dt.year < 2023].copy()
ytd_2023_trades_df = historic_trades_df[historic_trades_df['Time'].dt.year == 2023].copy()
model = RandomForestModel(training_df=pre_2023_trades_training_df, testing_df=ytd_2023_trades_df)


# --- RISK ENGINE ---
# Create a risk engine, which calculates return correlations based on pre-2023 data
pre_2023_trades_training_df['Time'] = pd.to_datetime(pre_2023_trades_training_df['Time'])
pre_2023_trades_training_df['Date'] = pre_2023_trades_training_df['Time'].dt.date
pre_2023_trade_pivot = pre_2023_trades_training_df.pivot_table(index='Date', columns='ticker', values='vwap', aggfunc='last')
pre_2023_returns_df = pre_2023_trade_pivot.pct_change(fill_method=None)
risk_engine = RiskEngine(pre_2023_returns_df)


# --- PORTFOLIO ---
# Create a portfolio, with an initial cash balance
tickers_with_2022_data = pre_2023_trades_training_df['ticker'].unique().tolist()
portfolio = Portfolio(tickers=tickers_with_2022_data, cash=100000, risk_engine=risk_engine)


# --- TRADING SIMULATOR ---
# Simulates trading through 2023, receiving trade information on a minute-by-minute basis
ytd_2023_trade_simulator_df = historic_trades_df[(historic_trades_df['Time'].dt.year >= 2023) & (historic_trades_df['ticker'].isin(tickers_with_2022_data))].copy()
ytd_2023_trade_simulator_df.drop(columns=['target_fn 0=same 1=dec 2=inc 3=both'], inplace=True)
trade_simulation = TradingSimulator(ytd_2023_trade_simulator_df)

for trade in trade_simulation:
    # NOTE: I updated this code so it actually performs like it would in a real environment - running the model on each new trade.
    # This obviously takes a lot of time, so if you don't like this just use the testing_df
    prediction = model.predict(trade.convert_for_prediction())
    portfolio.update_ticker_price(trade.get_ticker(), trade.get_price())
    portfolio.redeem_sell_orders(trade, prediction)

    if portfolio.is_buy(prediction):
        portfolio.buy(prediction, trade)
    elif portfolio.is_sell(prediction):
        portfolio.sell(prediction, trade)

trade_log_df = portfolio.get_trade_log()
trade_log_df.to_csv('trade_log.csv')

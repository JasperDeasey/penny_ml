import pandas as pd
from data.historical_data import historical_trade_gatherer
from model.random_forest_classifier import RandomForestModel
from data.database import sqlite_db
from trading_simulator.portfolio.risk_engine import RiskEngine
from trading_simulator.portfolio.portfolio import Portfolio
from trading_simulator.trading_simulator import TradingSimulator
from model.random_forest_classifier import Prediction
import numpy as np

import pandas as pd
import json

# Load the CSV file
df = pd.read_csv('trading_simulator/concentration_data.csv')

# Assuming the first row of the CSV is the header with tickers
# and subsequent rows are the values
tickers = df.columns.tolist()
values = df.values.tolist()

# Initialize your JSON structure
json_data = {
    "Cash": [],
    "Top 10 Positions": [],
    "Remaining Positions": []
}

# Assuming 'Cash' is always the first column
for row in values:
    json_data["Cash"].append(row[0])  # Adding cash values

    # Sort the remaining values (excluding 'Cash') and get their indices
    sorted_indices = sorted(range(1, len(tickers)), key=lambda i: row[i], reverse=True)

    # Adding top 10 positions
    top_10_indices = sorted_indices[:10]
    json_data["Top 10 Positions"].append([tickers[i] + ": " + str(row[i]) for i in top_10_indices])

    # Adding remaining positions if they exist
    if len(tickers) > 11:
        remaining_indices = sorted_indices[10:]
        json_data["Remaining Positions"].append([tickers[i] + ": " + str(row[i]) for i in remaining_indices])

# Specify the path where you want to save the JSON file
json_file_path = 'frontend/src/data/concentration_data.json'  # Replace with your desired file path
json_str = json.dumps(json_data, indent=4)

# Write the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_str)

print(f"JSON data saved to {json_file_path}")





"""
--------- DATA ---------
All data is based off of minutely-trading data from Polygon.io
"""
print("Gathering Data")
# historical_data_gatherer.gather_historic_data() # <-- uncomment if need to restart and get data again
db = sqlite_db.LocalDatabase()
# historic_trades_df = db.query("SELECT * FROM historical_trades WHERE strftime('%Y', Time) < '2023'")
# historic_trades_df['Time'] = pd.to_datetime(historic_trades_df['Time'])
# historic_trades_df = historic_trades_df.sort_values(['Time'], ascending=[True]).reset_index()
# pre_2023_trades_training_df = historic_trades_df

"""
--------- MODEL ---------
Create model, which predicts if a stock will go up or down 10% in the next 5 days
"""
print("Creating model")
# pre_2023_trades_training_df = historic_trades_df[historic_trades_df['Time'].dt.year < 2023].copy()
# ytd_2023_trades_df = historic_trades_df[historic_trades_df['Time'].dt.year == 2023].copy()
# model = RandomForestModel()
# prediction_df = model.train(train_df=pre_2023_trades_training_df, test_df=ytd_2023_trades_df)
# db.replace_df(prediction_df, 'model_prediction')
prediction_df = db.query("""
SELECT *
FROM model_prediction
WHERE ticker IN (
    SELECT ticker
    FROM model_prediction
    WHERE MODEL_PREDICTION = 2 AND PROBABILITY > 0.7
    GROUP BY ticker
    HAVING COUNT(*) >= 10
);
""")
print(len(prediction_df['ticker'].unique()))


prediction_df['Time'] = pd.to_datetime(prediction_df['Time'])
prediction_df['ticker'] = prediction_df['ticker'].astype(str)

"""
--------- RISK ENGINE ---------
Create a risk engine, which calculates return correlations based on pre-2023 data
"""
print("Building Risk Engine")
# pre_2023_trades_training_df['Date'] = pre_2023_trades_training_df['Time'].dt.date
# pre_2023_trade_pivot = pre_2023_trades_training_df.pivot_table(index='Date', columns='ticker', values='vwap', aggfunc='last')
# pre_2023_returns_df = pre_2023_trade_pivot.pct_change(fill_method=None)
# db.replace_df(pre_2023_returns_df, 'pre_2023_returns_df')
pre_2023_returns_df = db.query("SELECT * FROM pre_2023_returns_df")
risk_engine = RiskEngine(pre_2023_returns_df)
prediction_df = prediction_df[prediction_df['ticker'].isin(pre_2023_returns_df.columns.astype(str).tolist())]

"""
--------- PORTFOLIO ---------
"""
tickers = [str(x) for x in pre_2023_returns_df.columns.tolist() if x.isdigit()]
portfolio = Portfolio(tickers=tickers, cash=100000, risk_engine=risk_engine)


"""
--------- TRADING SIMULATOR ---------
Simulates trading through 2023, receiving trade information on a minute-by-minute basis

"""
# ytd_2023_trade_simulator_df = historic_trades_df[(historic_trades_df['Time'].dt.year >= 2023) & (historic_trades_df['ticker'].isin(tickers_with_2022_data))].copy()
# ytd_2023_trade_simulator_df.drop(columns=['target_fn 0=same 1=dec 2=inc 3=both'], inplace=True)
trade_simulation = TradingSimulator(prediction_df)

for trade, prediction in trade_simulation:
    print('.', end='') # prints at each iteration, regardless of trade
    # NOTE: I updated this code so it actually performs like it would in a real environment - running the model on each new trade.
    # This obviously takes forever, so I don't use it, but to do that, create a TradeSimulator(ytd_2023_trade_simulator)
    # and remove prediction from its iterator
    portfolio.update_ticker_price(trade.get_ticker(), trade.get_price())

    # prediction = model.predict(trade.convert_for_prediction())
    portfolio.redeem_sell_orders(trade, prediction)

    if portfolio.is_buy(prediction):
        portfolio.buy(prediction, trade)
    elif portfolio.is_sell(prediction):
        portfolio.sell(prediction, trade)


"""
--------- Save Data ---------
"""
trade_log_df = portfolio.get_trade_log()
trade_log_df.to_csv('./trading_simulator/trade_log.csv', index=False)


prediction_df['Date'] = prediction_df['Time'].dt.date
equal_weighted_portfolio_return = prediction_df.pivot_table(index='Date', columns='ticker', values='vwap', aggfunc='last')
equal_weighted_portfolio_return = equal_weighted_portfolio_return.pct_change(fill_method=None).fillna(0)
equal_weighted_portfolio_return['RoR'] = equal_weighted_portfolio_return.mean(axis=1)
equal_weighted_portfolio_return = equal_weighted_portfolio_return[['RoR']]
equal_weighted_portfolio_return.to_csv('./trading_simulator/equal_weighted_ror.csv')


trade_log_df['Date'] = trade_log_df['Time'].dt.date
trade_log_df['Value'] = trade_log_df['Ticker Quantity'] * trade_log_df['vwap']
trade_log_df['Equity'] = trade_log_df['Market Value'] - trade_log_df['Cash']
all_ticker_pivot = trade_log_df.pivot_table(index='Date', columns='ticker', values='Value', aggfunc='last')
total_value_pivot = trade_log_df.pivot_table(index='Date', values=['Market Value', 'Cash', 'Equity'])
total_value_pivot = total_value_pivot.merge(all_ticker_pivot, left_index=True, right_index=True, how='inner')
total_value_pivot.to_csv('./trading_simulator/fund_daily_value.csv')

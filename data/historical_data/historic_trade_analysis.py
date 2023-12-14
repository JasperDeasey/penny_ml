import pandas as pd
import numpy as np
from data.database.sqlite_db import LocalDatabase
def analyze_historic_trades(raw_trade_history_df):
    # NOW, with the entire company's market history, work on the data to make calculations.

    # 1) Convert time to readable format, and set as the index
    raw_trade_history_df['Time'] = pd.to_datetime(raw_trade_history_df['timestamp'], unit='ms')
    raw_trade_history_df.set_index('Time', inplace=True)
    raw_trade_history_df.index = raw_trade_history_df.index.floor('T')  # Truncate to the start of the minute

    # 2) Add rolling average prices

    # Generate a date range with a specific start time
    date_range = pd.date_range(start=raw_trade_history_df.index.min().date(),
                               end=raw_trade_history_df.index.max().date(),
                               freq='D').strftime('%Y-%m-%d')
    date_range = pd.to_datetime(date_range)
    # Calculate the daily average VWAP

    daily_avg_vwap = raw_trade_history_df['vwap'].resample('D').mean()
    daily_avg_vwap = daily_avg_vwap[pd.notna(daily_avg_vwap)]

    # Shift the daily average VWAP down by one day
    daily_avg_vwap = daily_avg_vwap.shift(1)

    # Calculate the rolling averages using the daily averages
    rolling_avg_5d = daily_avg_vwap.rolling(window=5, min_periods=5).mean()
    rolling_avg_10d = daily_avg_vwap.rolling(window=10, min_periods=10).mean()
    rolling_avg_30d = daily_avg_vwap.rolling(window=30, min_periods=30).mean()

    # Fill in missing dates, and roll forward all data
    daily_avg_vwap = daily_avg_vwap.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_avg_5d = rolling_avg_5d.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_avg_10d = rolling_avg_10d.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_avg_30d = rolling_avg_30d.reindex(date_range, fill_value=np.NaN).ffill()

    # Join the rolling average prices to the original dataframe
    raw_trade_history_df = raw_trade_history_df.join(daily_avg_vwap.rename('prev_daily_avg_price_1d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_avg_5d.rename('prev_rolling_avg_price_5d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_avg_10d.rename('prev_rolling_avg_price_10d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_avg_30d.rename('prev_rolling_avg_price_30d').resample('T').ffill(), on=raw_trade_history_df.index)

    # 3) Add rolling average volatility
    # Calculate the daily volatility
    daily_volatility = raw_trade_history_df['vwap'].resample('D').std()
    daily_volatility = daily_volatility[pd.notna(daily_volatility)]
    # daily_volatility = daily_volatility.reindex(date_range, fill_value=np.NaN)
    daily_volatility = daily_volatility.shift(1)


    # Calculate daily returns from VWAP
    daily_returns = raw_trade_history_df['close'].resample('D').last()
    daily_returns = daily_returns[pd.notna(daily_returns)]
    daily_returns = daily_returns.pct_change()

    # Calculate the rolling standard deviation of daily returns (volatility)
    rolling_vol_5d = daily_returns.rolling(window=5, min_periods=5).std()
    rolling_vol_10d = daily_returns.rolling(window=10, min_periods=10).std()
    rolling_vol_30d = daily_returns.rolling(window=30, min_periods=30).std()

    daily_volatility = daily_volatility.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_vol_5d = rolling_vol_5d.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_vol_10d = rolling_vol_10d.reindex(date_range, fill_value=np.NaN).ffill()
    rolling_vol_30d = rolling_vol_30d.reindex(date_range, fill_value=np.NaN).ffill()

    # Join the rolling volatilities back to the original dataframe
    raw_trade_history_df = raw_trade_history_df.join(daily_volatility.rename('prev_rolling_vol_1d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_vol_5d.rename('prev_rolling_vol_5d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_vol_10d.rename('prev_rolling_vol_10d').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(rolling_vol_30d.rename('prev_rolling_vol_30d').resample('T').ffill(), on=raw_trade_history_df.index)

    # 4) add industry and ticker
    ticker_info_df = pd.read_excel('./data/historical_data/polygon_available_securities.xlsx', sheet_name='Company Data')
    raw_trade_history_df = raw_trade_history_df.merge(ticker_info_df, on='numeric_ticker', how='inner')
    raw_trade_history_df['industry'] = raw_trade_history_df['numeric_industry']
    raw_trade_history_df['ticker'] = raw_trade_history_df['numeric_ticker']

    # 5) Add market cap
    raw_trade_history_df['market_cap_estimate_$M'] = raw_trade_history_df['vwap'] / raw_trade_history_df['Price Close (USD)'] * raw_trade_history_df['Company Market Cap (Millions, USD)']

    # 6) Add max/min prices over 1-day/5-day rolling periods
    # Calculate the daily volatility
    daily_highs = raw_trade_history_df['high'].resample('D').max()
    daily_lows = raw_trade_history_df['low'].resample('D').min()
    daily_highs = daily_highs[pd.notna(daily_highs)]
    daily_lows = daily_lows[pd.notna(daily_lows)]

    # Shift the daily average VWAP down by one day
    daily_highs = daily_highs.shift(-1)
    daily_lows = daily_lows.shift(-1)

    # Calculate the rolling standard deviation of daily returns (volatility)
    next_5_day_high = daily_highs.rolling(window=5, min_periods=5).max().shift(-4)
    next_5_day_low = daily_lows.rolling(window=5, min_periods=5).min().shift(-4)

    # Fill in blank dates
    daily_highs = daily_highs.reindex(date_range, fill_value=np.NaN).bfill()
    daily_lows = daily_lows.reindex(date_range, fill_value=np.NaN).bfill()
    next_5_day_high = next_5_day_high.reindex(date_range, fill_value=np.NaN).bfill()
    next_5_day_low = next_5_day_low.reindex(date_range, fill_value=np.NaN).bfill()

    # Join the highs and lows to the original dataframe
    raw_trade_history_df = raw_trade_history_df.join(next_5_day_high.rename('next_5_day_high').resample('T').ffill(), on=raw_trade_history_df.index)
    raw_trade_history_df = raw_trade_history_df.join(next_5_day_low.rename('next_5_day_low').resample('T').ffill(), on=raw_trade_history_df.index)

    raw_trade_history_df['10_pct_increase'] = raw_trade_history_df['next_5_day_high'] >= (raw_trade_history_df['vwap'] * 1.1)
    raw_trade_history_df['10_pct_decrease'] = raw_trade_history_df['next_5_day_low'] <= (raw_trade_history_df['vwap'] * 0.9)

    inc_int = raw_trade_history_df['10_pct_increase'].astype(int)
    dec_int = raw_trade_history_df['10_pct_decrease'].astype(int)

    raw_trade_history_df['target_fn 0=same 1=dec 2=inc 3=both'] = dec_int + 2 * inc_int

    # 8) Drop rows that aren't filled in
    raw_trade_history_df = raw_trade_history_df[(pd.notna(raw_trade_history_df['prev_rolling_avg_price_30d'])) & (pd.notna(raw_trade_history_df['next_5_day_low']))]

    # 7) drop columns that aren't useful
    raw_trade_history_df.reset_index(inplace=True)
    raw_trade_history_df = raw_trade_history_df[
        ['Time', 'ticker', 'industry', 'market_cap_estimate_$M', 'vwap', 'volume', 'prev_daily_avg_price_1d',
         'prev_rolling_avg_price_5d', 'prev_rolling_avg_price_10d', 'prev_rolling_avg_price_30d', 'prev_rolling_vol_1d',
         'prev_rolling_vol_5d', 'prev_rolling_vol_10d', 'prev_rolling_vol_30d', 'target_fn 0=same 1=dec 2=inc 3=both']]

    # 9?) Create a few final calculations to take some of the grunt work out for the model.
    raw_trade_history_df['pct_difference_from_1d_avg'] = raw_trade_history_df['vwap'] / raw_trade_history_df['prev_daily_avg_price_1d'] - 1
    raw_trade_history_df['pct_difference_from_5d_avg'] = raw_trade_history_df['vwap'] / raw_trade_history_df['prev_rolling_avg_price_5d'] - 1
    raw_trade_history_df['pct_difference_from_10d_avg'] = raw_trade_history_df['vwap'] / raw_trade_history_df['prev_rolling_avg_price_10d'] - 1
    raw_trade_history_df['pct_difference_from_30d_avg'] = raw_trade_history_df['vwap'] / raw_trade_history_df['prev_rolling_avg_price_30d'] - 1

    raw_trade_history_df.drop(columns=['prev_daily_avg_price_1d', 'prev_rolling_avg_price_5d', 'prev_rolling_avg_price_10d',
                             'prev_rolling_avg_price_30d'], inplace=True)

    # WITH the complete dataframe, with calculations included, append to csv with all data
    db = LocalDatabase()
    lo

    raw_trade_history_df.to_csv(output_file, mode='a', index=False, header=not os.path.exists(output_file))
    print(f'Appended chunk from {ticker}')

    print('\n -- saved data here: polygon_historical_trading_data.csv -- \n')
    df = pd.read_csv(output_file)
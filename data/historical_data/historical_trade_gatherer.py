import numpy as np
from polygon import RESTClient
import pandas as pd
from datetime import datetime, timedelta
from data.database.sqlite_db import LocalDatabase

def gather_historic_data():
    client = RESTClient(api_key="6MfbROoUA4uYZz4nYMMJ2Lwp6baStpwH")
    company_df = pd.read_excel('./data/historical_data/polygon_available_securities.xlsx', sheet_name='Company Data')

    # Modified date calculations
    current_date = datetime.now() - timedelta(days=1)
    five_years_ago = current_date - timedelta(days=5*365)
    end_date = five_years_ago + timedelta(days=30)  # One month from the start date
    db = LocalDatabase()

    for ind, row in company_df.iterrows():
        start_date = five_years_ago
        company_dfs = []

        ticker = row['Ticker']
        numeric_ticker = row['numeric_ticker']

        # Gathering the data monthly, to ensure that data is a managable size
        while start_date < current_date:
            formatted_start_date = start_date.strftime("%Y-%m-%d")
            formatted_end_date = end_date.strftime("%Y-%m-%d")

            # Fetch data for the month
            try:
                aggs = []
                for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_=formatted_start_date, to=formatted_end_date, limit=50000):
                    aggs.append(a)
                date_df = pd.DataFrame(aggs)
                date_df['Ticker'] = ticker
                company_dfs.append(date_df)
            except Exception as e:
                print(f"Unable to add ticker '{ticker}'. Error=\n{e}\n\n")

            # Move to the next month
            start_date = end_date
            end_date = start_date + timedelta(days=30)

        # NOW, with the entire company's market history, work on the data to make calculations.

        # 1) Convert time to readable format, and set as the index
        company_df = pd.concat(company_dfs)
        company_df['Time'] = pd.to_datetime(company_df['timestamp'], unit='ms')
        company_df.set_index('Time', inplace=True)
        company_df.index = company_df.index.floor('T')  # Truncate to the start of the minute

        # 2) Add rolling average prices

        # Generate a date range with a specific start time
        date_range = pd.date_range(start=company_df.index.min().date(),
                            end=company_df.index.max().date(),
                            freq='D').strftime('%Y-%m-%d')
        date_range = pd.to_datetime(date_range)
        # Calculate the daily average VWAP

        daily_avg_vwap = company_df['vwap'].resample('D').mean()
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
        company_df = company_df.join(daily_avg_vwap.rename('prev_daily_avg_price_1d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_avg_5d.rename('prev_rolling_avg_price_5d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_avg_10d.rename('prev_rolling_avg_price_10d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_avg_30d.rename('prev_rolling_avg_price_30d').resample('T').ffill(), on=company_df.index)

        # 3) Add rolling average volatility
        # Calculate the daily volatility
        daily_volatility = company_df['vwap'].resample('D').std()
        daily_volatility = daily_volatility[pd.notna(daily_volatility)]
        # daily_volatility = daily_volatility.reindex(date_range, fill_value=np.NaN)
        daily_volatility = daily_volatility.shift(1)


        # Calculate daily returns from VWAP
        daily_returns = company_df['close'].resample('D').last()
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
        company_df = company_df.join(daily_volatility.rename('prev_rolling_vol_1d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_vol_5d.rename('prev_rolling_vol_5d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_vol_10d.rename('prev_rolling_vol_10d').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(rolling_vol_30d.rename('prev_rolling_vol_30d').resample('T').ffill(), on=company_df.index)

        # 4) add industry and ticker
        company_df['industry'] = row['numeric_industry']
        company_df['ticker'] = row['numeric_ticker']

        # 5) Add market cap
        company_df['market_cap_estimate_$M'] = company_df['vwap'] / row['Price Close (USD)'] * row['Company Market Cap (Millions, USD)']


        # 6) Add max/min prices over 1-day/5-day rolling periods
        # Calculate the daily volatility
        daily_highs = company_df['high'].resample('D').max()
        daily_lows = company_df['low'].resample('D').min()
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
        company_df = company_df.join(next_5_day_high.rename('next_5_day_high').resample('T').ffill(), on=company_df.index)
        company_df = company_df.join(next_5_day_low.rename('next_5_day_low').resample('T').ffill(), on=company_df.index)

        company_df['10_pct_increase'] = company_df['next_5_day_high'] >= (company_df['vwap'] * 1.1)
        company_df['10_pct_decrease'] = company_df['next_5_day_low'] <= (company_df['vwap'] * 0.9)

        inc_int = company_df['10_pct_increase'].astype(int)
        dec_int = company_df['10_pct_decrease'].astype(int)

        company_df['target_fn 0=same 1=dec 2=inc 3=both'] = dec_int + 2*inc_int

        # 8) Drop rows that aren't filled in
        company_df = company_df[(pd.notna(company_df['prev_rolling_avg_price_30d'])) & (pd.notna(company_df['next_5_day_low']))]

        # 7) drop columns that aren't useful
        company_df.reset_index(inplace=True)
        company_df = company_df[['Time', 'ticker', 'industry', 'market_cap_estimate_$M', 'vwap', 'volume', 'prev_daily_avg_price_1d', 'prev_rolling_avg_price_5d', 'prev_rolling_avg_price_10d','prev_rolling_avg_price_30d', 'prev_rolling_vol_1d','prev_rolling_vol_5d', 'prev_rolling_vol_10d', 'prev_rolling_vol_30d', 'target_fn 0=same 1=dec 2=inc 3=both']]

        # 9?) Create a few final calculations to take some of the grunt work out for the model.
        company_df['pct_difference_from_1d_avg'] = company_df['vwap'] / company_df['prev_daily_avg_price_1d'] - 1
        company_df['pct_difference_from_5d_avg'] = company_df['vwap'] / company_df['prev_rolling_avg_price_5d'] - 1
        company_df['pct_difference_from_10d_avg'] = company_df['vwap'] / company_df['prev_rolling_avg_price_10d'] - 1
        company_df['pct_difference_from_30d_avg'] = company_df['vwap'] / company_df['prev_rolling_avg_price_30d'] - 1

        company_df.drop(columns=['prev_daily_avg_price_1d', 'prev_rolling_avg_price_5d', 'prev_rolling_avg_price_10d', 'prev_rolling_avg_price_30d'], inplace=True)

        # WITH the complete dataframe, with calculations included, append to database with all data
        db.append_df(company_df, 'historical_trades')
        print(f'Appended chunk from {ticker}')

    print('\n -- saved data here to penny_ai.db[historical_trades] -- \n')


if __name__=='__main__':
    gather_historic_data()
    

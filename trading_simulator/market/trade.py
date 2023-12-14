from datetime import datetime
import pandas as pd
import math

class Trade:
    def __init__(self, time, ticker, price, volume, row_df):
        self._time = time
        self._ticker = ticker
        self._price = price
        self._volume = volume
        self._prediction_df = row_df

    def get_time(self):
        return self._time

    def get_ticker(self):
        return self._ticker

    def get_price(self):
        return self._price

    def get_volume(self):
        return self._volume

    def convert_for_prediction(self):
        self._prediction_df['Time'] = self._prediction_df['Time'].view('int64')
        self._prediction_df.drop(columns=['level_0', 'prev_vwap'], inplace=True)
        return self._prediction_df

    def __str__(self):
        return f"Trade - Time: {self._time}, Ticker: {self._ticker}, Price: {self._price}, Volume: {self._volume}"

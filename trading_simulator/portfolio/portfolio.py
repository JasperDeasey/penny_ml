from trading_simulator.market.outstanding_orders import OutstandingOrders
import math
import pandas as pd


class Portfolio:
    def __init__(self, tickers, cash, risk_engine):
        self.risk_engine = risk_engine
        self._holdings = {}
        for ticker in tickers:
            self.add_ticker_to_holdings(ticker, 0, 0, )
        self._holdings['cash'] = {'quantity': cash, 'price': 1, 'sell_orders': OutstandingOrders()}
        self._total_value = cash
        self._trade_log = []
        self._min_buy_probability = 0.5
        self._min_sell_probability = 0.5

    def redeem_sell_orders(self, trade, prediction):
        sold_df = self._holdings[trade.get_ticker()]['sell_orders'].redeem_orders(trade.get_price(), trade.get_time())

        if (sold_df is None) or (sold_df['quantity'].sum() == 0):
            return

        quantity_sold = sold_df['quantity'].sum()
        cash_transacted = sold_df['quantity'].sum() * trade.get_price()
        self._holdings[trade.get_ticker()]['quantity'] -= quantity_sold
        self._holdings['cash']['quantity'] += cash_transacted
        sold_df['weighted_price'] = sold_df['purchase_price'] * sold_df['quantity']
        avg_price = sold_df['weighted_price'].sum() / quantity_sold
        print(f'sold {quantity_sold} of {trade.get_ticker()} @ {trade.get_price()} vs. avg price of {avg_price}')
        self.update_trade_log(trade, quantity_sold, cash_transacted, prediction)

    def create_sell_order(self, ticker, strike_price, quantity, purchase_price, expiry_date):
        self._holdings[ticker]['sell_orders'].add_sell_order(strike_price, quantity, purchase_price, expiry_date)

    def get_holdings(self):
        return self._holdings

    def update_trade_log(self, trade, quantity_transacted, cash_transacted, prediction):
        self._trade_log.append([trade.get_time(), trade.get_ticker(), self.get_cash(), self.get_total_value(), self.get_ticker_quantity(trade.get_ticker()), quantity_transacted, cash_transacted, trade.get_price(), prediction.prediction, prediction.probability])

    def get_trade_log(self):
        return pd.DataFrame(self._trade_log)

    def add_ticker_to_holdings(self, ticker, quantity, price):
        """Add or update a ticker in the portfolio."""
        if ticker not in self._holdings:
            self._holdings[ticker] = {'quantity': 0, 'price': 0, 'sell_orders': OutstandingOrders()}

        self._holdings[ticker]['quantity'] += quantity
        self._holdings[ticker]['price'] = price

    def change_ticker_quantity(self, ticker, quantity):
        self._holdings[ticker]['quantity'] += quantity

    def get_ticker_quantity(self, ticker):
        return self._holdings[ticker]['quantity']

    def get_cash(self):
        return self._holdings['cash']['quantity']

    def change_cash(self, cash_value):
        self._holdings['cash']['quantity'] += cash_value

    def update_ticker_price(self, ticker, price):
        """Update the price of a specific ticker."""
        if ticker in self._holdings:
            price_0 = self._holdings[ticker]['price']
            self._holdings[ticker]['price'] = price
            if price_0 != 0:
                quantity = self._holdings[ticker]['quantity']
                self._total_value += quantity * (price - price_0)

        else:
            print(f"{ticker} not found in portfolio.")

    def get_ticker_weight(self, ticker):
        """Returns weight of ticker [1, 0]"""
        ticker_value = self._holdings[ticker]['price'] * self._holdings[ticker]['quantity']
        return ticker_value / self._total_value

    def get_total_value(self):
        """Calculate and return the total value of the portfolio."""
        return self._total_value

    def is_buy(self, prediction):
        """Determines if the trade is a buy."""
        return (prediction.prediction == 2) & (prediction.probability >= self._min_buy_probability)

    def is_sell(self, prediction):
        """Determines if the trade is a sell."""
        return (prediction.prediction == 1) & (prediction.probability >= self._min_sell_probability)

    def buy(self, prediction, trade):
        """
        Purchase the optimal amount to buy, and add it to the portfolio
        """
        ideal_value = self.risk_engine.calc_ideal_incremental_value(prediction, trade, self)

        transaction_quantity = math.floor(ideal_value / trade.get_price())
        transaction_value = transaction_quantity * trade.get_price()

        # Can't trade more volume than is available
        if transaction_quantity > trade.get_volume():
            transaction_quantity = math.floor(trade.get_volume())
            transaction_value = transaction_quantity * trade.get_price()

        # Can't trade more value than we have cash
        if transaction_value > self.get_cash():
            transaction_quantity = math.floor(self.get_cash() / trade.get_price())
            transaction_value = transaction_quantity * trade.get_price()

        self.change_ticker_quantity(trade.get_ticker(), transaction_quantity)
        self.change_cash(-1*transaction_value)

        self.update_trade_log(trade, transaction_quantity, -1*transaction_value, prediction)
        self.create_sell_order(trade.get_ticker(), trade.get_price() * 1.1, transaction_quantity, trade.get_price(), trade.get_time() + pd.Timedelta(days=10))

        if transaction_value != 0:
            print(
                f'{trade.get_time().strftime("%m-%d %H:%M")}  | '
                f'BUY : ${transaction_value:>4.0f}  |'
                f' MV: ${self.get_total_value():>7,.0f}  |'
                f' CASH: ${self.get_cash():>5,.0f}  |'
                f' VOL: {transaction_quantity:>5}='
                f'ideal_value: ${ideal_value:>4.0f} =='
                f' price(${trade.get_price():>4.1f}) -- '
                f' ticker: {trade.get_ticker():>3.0f} | {self.get_ticker_quantity(trade.get_ticker()):>4.0f} | {self.get_ticker_weight(trade.get_ticker()) * 100: 3.1f}%'
            )

    def sell(self, prediction, trade):
        """
        Purchase the optimal amount to buy, and add it to the portfolio
        """
        # just for printing reference!

        ideal_value = self.risk_engine.calc_ideal_incremental_value(prediction, trade, self)
        transaction_quantity = math.floor(ideal_value / trade.get_price())
        transaction_value = transaction_quantity * trade.get_price()

        # Can't trade more volume than is available
        if transaction_quantity > trade.get_volume():
            transaction_quantity = math.floor(trade.get_volume())
            transaction_value = transaction_quantity * trade.get_price()

        # Can't trade more units than we have in our portfolio
        if transaction_quantity > self.get_ticker_quantity(trade.get_ticker()):
            transaction_quantity = self.get_ticker_quantity(trade.get_ticker())
            transaction_value = transaction_quantity * trade.get_price()

        self.change_ticker_quantity(trade.get_ticker(), -1*transaction_quantity)
        self.change_cash(transaction_value)

        self.update_trade_log(trade, -1*transaction_quantity, transaction_value, prediction)

        if transaction_value != 0:
            print(
                f'{trade.get_time().strftime("%m-%d %H:%M")}  | '
                f'SELL: ${transaction_value:>4.0f}  |'
                f' MV: ${self.get_total_value():>7,.0f}  |'
                f' CASH: ${self.get_cash():>5,.0f}  |'
                f' VOL: {transaction_quantity:>5}='
                f'ideal_value: ${ideal_value:>4.0f} =='
                f' price(${trade.get_price():>4.1f}) -- '
                f' ticker: {trade.get_ticker():>3.0f} | {self.get_ticker_quantity(trade.get_ticker()):>4.0f} | {self.get_ticker_weight(trade.get_ticker()) * 100: 3.1f}%'
            )

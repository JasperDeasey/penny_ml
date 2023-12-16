import pandas as pd

class OutstandingOrders:
    def __init__(self):
        self.sell_orders = pd.DataFrame(columns=['quantity', 'strike_price', 'purchase_price', 'expiry_date'])
        self.min_value = 1000

    def add_sell_order(self, strike_price, quantity, purchase_price, expiry_date):
        """
        Add a new order.

        Args:
        order_type (str): 'buy' or 'sell'
        units (int): Number of units in the order
        price (float): Price per unit
        """
        if strike_price < self.min_value: self.min_value = strike_price

        new_order = pd.DataFrame({'quantity': [quantity], 'strike_price': [strike_price], 'purchase_price': purchase_price, 'expiry_date': expiry_date})

        self.sell_orders = self.sell_orders.dropna(axis=1, how='all')
        new_order = new_order.dropna(axis=1, how='all')

        # Then concatenate
        self.sell_orders = pd.concat([self.sell_orders, new_order], ignore_index=True)

    def cancel_orders(self, quantity):
        quantity_cancelled = 0
        cancelled_indices = []

        for ind, row in self.sell_orders.iterrows():
            if quantity_cancelled + row['quantity'] > quantity:
                # Adjust the quantity of the current row if adding it exceeds the target quantity
                excess = quantity_cancelled + row['quantity'] - quantity
                self.sell_orders.at[ind, 'quantity'] -= excess
                quantity_cancelled = quantity  # Set to exact target quantity
                break

            quantity_cancelled += row['quantity']
            cancelled_indices.append(ind)

            if quantity_cancelled == quantity:
                break

        self.sell_orders.drop(cancelled_indices, inplace=True)
        self.min_value = self.sell_orders['strike_price'].min() if not self.sell_orders.empty else None
        return quantity_cancelled

    def redeem_orders(self, current_price, current_date):
        """
        Redeem all orders where the price is above the current price. Assumes there is adequate liquidity for all orders

        Args:
        current_price (float): The current price of the stock
        """
        if len(self.sell_orders) == 0:
            return

        min_date = self.sell_orders.iloc[0]['expiry_date']
        if (self.min_value <= current_price) or (min_date <= current_date):
            orders_sold_df = self.sell_orders[(self.sell_orders['strike_price'] <= current_price) | (self.sell_orders['expiry_date'] <= current_date)]

            if len(orders_sold_df) > 0:
                self.sell_orders = self.sell_orders[(self.sell_orders['strike_price'] > current_price) & (self.sell_orders['expiry_date'] > current_date)]
                self.min_value = self.sell_orders['strike_price'].min()

            return orders_sold_df
        return None

    def __str__(self):
        return str(self.sell_orders)

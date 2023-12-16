import pandas as pd
from scipy.stats import norm


class RiskEngine:
    def __init__(self, underlying_returns_df):
        """
        Initialize the Risk Engine with a portfolio DataFrame.
        The DataFrame should contain daily [index] returns [value] for each ticker [columns].
        """
        underlying_returns_df['cash'] = 0
        self._underlying_returns_df = underlying_returns_df
    
    def get_portfolio_return(self, portfolio):
        # Step 1: Calculate weights
        portfolio_df = pd.DataFrame.from_dict(portfolio.get_holdings(), orient='index')
        portfolio_df.index.name = 'ticker'

        portfolio_df['Market_Value'] = portfolio_df['price'] * portfolio_df['quantity']
        total_portfolio_value = portfolio_df['Market_Value'].sum()
        portfolio_df['Weight'] = portfolio_df['Market_Value'] / total_portfolio_value

        # Step 2: Multiply daily returns by weights
        aligned_weights = portfolio_df['Weight'].reindex(self._underlying_returns_df.columns).fillna(0)
        weighted_returns = self._underlying_returns_df.multiply(aligned_weights, axis='columns')
        
        # Step 3: Sum weighted returns for each day
        portfolio_daily_returns = weighted_returns.sum(axis=1)
        return portfolio_daily_returns
    
    def calculate_correlation_to_portfolio(self, ticker, portfolio):
        """
        Returns value [-1, 1], which is the correlation of the stock to the current portfolio
        """
        portfolio_return = self.get_portfolio_return(portfolio).dropna()
        ticker_returns_df = self._underlying_returns_df[ticker]
        ticker_returns_df = ticker_returns_df.dropna()
        portfolio_return, ticker_returns_df = portfolio_return.align(ticker_returns_df, join='inner')

        # # Check for constant values
        # if portfolio_return.std() == 0 or ticker_returns_df.std() == 0:
        #     print("One of the series has constant values")

        correlation = portfolio_return.corr(ticker_returns_df)
        if pd.isna(correlation):
            correlation = 0

        return correlation

    def calculate_parametric_var(self, weights_df, confidence_level=0.95):

        # Calculate weighted portfolio returns
        portfolio_returns_df = self._underlying_returns_df[weights_df.index]
        weights_series = weights_df['weight']
        portfolio_returns = (portfolio_returns_df * weights_series).sum(axis=1)
        
        # Calculate the mean and standard deviation of the portfolio returns
        portfolio_mean = portfolio_returns.mean()
        portfolio_std = portfolio_returns.std()

        # Calculate the z-score for the confidence level
        z_score = norm.ppf(confidence_level)

        # Calculate the VaR at the specified confidence level
        var = -z_score * portfolio_std

        print(f"The {confidence_level} Parametric VaR is: {var}")
        return var

    def calc_probability_factor(self, prediction):
        """Buy more, the more confident we are it is a buy. Sell more, the more confident we are it is a sell."""
        return prediction.probability ** 2

    def calc_correlation_factor(self, trade, portfolio, prediction):
        """
        Buy more if it is a diversifying asset.
        Sell less if it is a diversifying asset.
        """
        correlation = self.calculate_correlation_to_portfolio(trade.get_ticker(), portfolio)
        correlation_factor = 0
        if portfolio.is_buy(prediction):
            #   purchase more, the more diversifying the asset is
            #       = (1 - correlation)
            #               - correlation of 1 = 0, correlation of 0 = 1, correlation of -1 = 2
            correlation_factor = (-1 * correlation) + 1

        elif portfolio.is_sell(prediction):
            #   2) sell less, the more diversifying the asset is
            #       = (correlation)
            #               - correlation of 1 = 1, correlation of 0 = 1, correlation of -1 = 2
            correlation_factor = correlation + 1

        return min(2, max(0, correlation_factor))

    def calc_weight_factor(self, trade, portfolio, prediction):
        """
        Buy less, the more we own: [0, 1], ideal ~3%.
        Sell more, the more we own: [0: +], selling much more as weight increases.
        """
        weight = portfolio.get_ticker_weight(trade.get_ticker())
        weight_scaling_factor = 20

        if portfolio.is_buy(prediction):
            weight_factor = 1 - (weight_scaling_factor * weight) ** 2

        elif portfolio.is_sell(prediction):
            weight_factor = (weight_scaling_factor * weight) ** 2

        else:
            weight_factor = 0

        return max(0, weight_factor)

    def calc_total_factor(self, portfolio, prediction):
        """
        Scale purchase/sale with the total value of the portfolio
        """
        if portfolio.is_buy(prediction):
            portfolio_weight_factor = 0.01
        else:
            portfolio_weight_factor = 0.2
        return portfolio.get_total_value() * portfolio_weight_factor

    def calc_ideal_incremental_value(self, prediction, trade, portfolio):
        probability_factor = self.calc_probability_factor(prediction)
        correlation_factor = self.calc_correlation_factor(trade, portfolio, prediction)
        weight_factor = self.calc_weight_factor(trade, portfolio, prediction)
        total_factor = self.calc_total_factor(portfolio, prediction)

        ideal_value = probability_factor * correlation_factor * weight_factor * total_factor
        return ideal_value


if __name__ == "__main__":
    df = pd.DataFrame()
    risk_engine = RiskEngine(df)

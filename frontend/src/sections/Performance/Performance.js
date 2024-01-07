import React from 'react';
import './Performance.css';
import SectionTitle from '../../components/SectionTitle';
import ReturnsChart from '../../components/ReturnsChart';
import OverviewChart from '../../components/OverviewChart';

const Performance = () => {
  return (
    <div id="performance" className="section">
      <SectionTitle title="Performance" />
      <div className="content">
        <div className="commentary">
          <p>
            This strategy experienced extremely strong returns versus all benchmarks, at 426% return with a $100,000 portfolio.
            It also had strong risk-adjusted returns, with Sharpe and Sortino ratios well above that of the benchmarks.
          </p>
          <p>
            Days with the highest return (such as August 29) had many trades that occurred on that day - both buying and selling. 
            The model was able to take advantage of multiple rises in value through the day due to the high volatility and correct predictions. 
            The weight of a single stock never overwhelmed the portfolio.
            </p>
          <p>
            The strategy performs largely unrelated to the benchmark, with a low correlation and low beta (relative to its high volatility).
          </p>
          
          <div className="performance-table">
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>Penny ML</th>
                  <th>Equal Weighted Index</th>
                  <th>Russell Micro Cap Growth</th>
                  <th>Russell 2000</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>Period Returns</td><td>426.8%</td><td>-44.2%</td><td>-6.2%</td><td>3.3%</td></tr>
                <tr><td>Std. Devation of Returns</td><td>47.9%</td><td>50.5%</td><td>16.0%</td><td>15.6%</td></tr>
                <tr><td>Downside Deviation</td><td>19.8%</td><td>37.1%</td><td>11.8%</td><td>10.2%</td></tr>
                <tr><td>Sharpe Ratio</td><td>8.8</td><td>-1.0</td><td>-0.7</td><td>-0.1</td></tr>
                <tr><td>Sortino Ratio</td><td>21.4</td><td>-1.0</td><td>-0.7</td><td>-0.1</td></tr>
                <tr><td>Beta of Penny ML vs.</td><td>1.0</td><td>0.0</td><td>0.7</td><td>0.7</td></tr>
                <tr><td>Correlation of Penny ML vs.</td><td>1.0</td><td>0.0</td><td>0.3</td><td>0.2</td></tr>
              </tbody>
            </table>
          </div>
        </div>
          <div className="chart">
            <ReturnsChart />
        </div>
      </div>
    </div>
  );
};

export default Performance;

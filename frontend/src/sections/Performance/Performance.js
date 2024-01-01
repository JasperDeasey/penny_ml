import React from 'react';
import './Performance.css'; // Make sure to create and style this CSS file
import SectionTitle from '../../components/SectionTitle';
import ReturnsChart from '../../components/ReturnsChart';

const Performance = () => {
  return (
    <div id="performance" className="section">
      <SectionTitle title="Performance" />
      <div className="performance-content">
        <div className="performance-commentary">
          <p>
            This strategy experienced strong returns versus all benchmarks, at 175% return with a $100,000 portfolio.
            It also had strong risk-adjusted returns, with Sharpe and Sortino ratios well above that of the benchmarks.
            It was able to predict a 10% rise correctly X% of the time, and a 10% drop X% of the time.
          </p>
          <p>
            The strategy (acts?) unrelated to the benchmark, with an extremely low beta and correlation.
            It would be a strong diversifier to any portfolio; however, it is bound by AUM constraints, and would recieve diminishing returns as AUM rises.
            An AUM of $1M, for example, generates returns of __%, and an AUM of $1B generates a return of __%.
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
                <tr><td>Period Returns</td><td>175.6%</td><td>-44.2%</td><td>-6.2%</td><td>3.3%</td></tr>
                <tr><td>Std. Devation of Returns</td><td>15.1%</td><td>50.5%</td><td>16.0%</td><td>15.6%</td></tr>
                <tr><td>Downside Deviation</td><td>7.4%</td><td>37.1%</td><td>11.8%</td><td>10.2%</td></tr>
                <tr><td>Sharpe Ratio</td><td>11.3</td><td>-1.0</td><td>-0.7</td><td>-0.1</td></tr>
                <tr><td>Sortino Ratio</td><td>22.9</td><td>-1.0</td><td>-0.7</td><td>-0.1</td></tr>
                <tr><td>Beta of Penny ML vs.</td><td>1.0</td><td>0.0</td><td>0.3</td><td>0.3</td></tr>
                <tr><td>Correlation of Penny ML vs.</td><td>1.0</td><td>0.1</td><td>0.3</td><td>0.3</td></tr>
              </tbody>
            </table>
          </div>
        </div>
        <div className="performance-data">
          <div className="performance-graph">
            <ReturnsChart />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Performance;

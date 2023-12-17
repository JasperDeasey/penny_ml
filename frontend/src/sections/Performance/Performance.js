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
            Here is where the performance commentary will go. It can be a detailed text 
            explaining the performance metrics, market conditions, and other relevant information.
          </p>
        </div>
        <div className="performance-data">
          <div className="performance-graph">
            <ReturnsChart />
          </div>
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
      </div>
    </div>
  );
};

export default Performance;

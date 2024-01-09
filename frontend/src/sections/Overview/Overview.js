import React from 'react';
import './Overview.css';
import SectionTitle from '../../components/SectionTitle';
import OverviewChart from '../../components/OverviewChart';

const Overview = () => {
  return (
    <div id="overview" className="section">
        <SectionTitle title="Penny ML Overview" />
      <div className="content">
        <div className="commentary">
          <p>
            In 2019, I made an investment into a micro-cap company when it went public. 
            After a meteoric rise its first month on the market, it experienced an even more dramatic fall in value, now being worth next to nothing.
            Even after its steep sell-off, I continued to watch it and was fascinated by its behavior.
          </p>
          <p>
            I noticed that the stock displayed remarkable volatility - often experiencing swings of 20% within a single day. 
            Looking into other companies of similar size yielded similar results.
            In my job as an investment analyst, I became used to 20% swings in value over a year - a swing in value that large over just a day seemed unreasonable.
          </p>
          <p>
            I wondered if there was a way to build a strategy out of this behavior -
            to analyze the extreme volatility of the micro-cap market, and develop a strategy that typical funds don't investigate due to their size.
            Creating a quantitative fund from scratch, encompassing everything from alpha indicators to portfolio construction, to gain a deeper understanding of how these funds operate.
          </p>
          <p>
            That's the purpose of this project.
          </p>
          <p>
            Using minute-by-minute transaction data and machine learning, this projects aims to predict if a stock will quickly rise or fall in value.
            Using those predictions, trades are made - within the liquidity constraints of the market, and in a risk aware way - to build a portfolio.
            That portfolio is then optimized and tracked over time, to see if this strategy is a practical method for generating strong risk-adjusted returns.
          </p>
        </div>
        <div className="chart">
          <OverviewChart />
        </div>
      </div>
    </div>
  );
};

export default Overview;

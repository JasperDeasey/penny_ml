import React from 'react';
import './Overview.css';
import SectionTitle from '../../components/SectionTitle';
import OverviewChart from '../../components/OverviewChart';

const Overview = () => {
  return (
    <div id="overview" className="section">
        <SectionTitle title="Penny ML Overview" />
      <div className="overview-content">
        <div className="overview-text">
          <p>
            In 2019, I made an investment into a micro-cap company when it went public. 
            After a meteoric rise its first month on the market, it experienced an even more dramatic fall in value, now being worth next to nothing.
            After its steep sell-off, I still watch of it, despite it now (unfortunately) being worth next to nothing.
          </p>
          <p>
            I noticed that on any given day, the stock will rise and fall dramatically - often experiencing swings of 20% within a single day. 
            Looking into other companies of similar size yielded similar results.
            In my job as an investment analyst, I became used to 20% swings in value over a year - a swing in value that large over just a day seemed unreasonable.
          </p>
          <p>
          This market is very different than where large investors traditionally allocate - it is defined by small, illiquid transaction sizes and risky companies.
          These constraints (particularily the small transactoins sizes and illiquidity) may make them impractical for large investors, but is there buying opportunitis for a smaller investor?
          </p>
          <p>
            That's what this project seeks to solve.
          </p>
          <p>
            Using minute-by-minute transaction data and machine learning, this projects aims to predict if a stock will quickly rise or fall in value.
            Using those predictions, trades are made - within the liquidity constraints of the market, and in a risk aware way - to build a portfolio.
            That portfolio is then optimized and tracked over time, to see if this strategy is a realistic strategy for securing strong risk-adjusted returns.
          </p>
        </div>
        <div className="overview-visual">
          <OverviewChart />
        </div>
      </div>
    </div>
  );
};

export default Overview;

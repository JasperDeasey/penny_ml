import React from 'react';
import './Limitations.css';
import SectionTitle from '../../components/SectionTitle';
import InvestmentThesisImage from '../../data/InvestmentThesis.jpg';
import ProcessFlowChart from '../../data/FlowChart.png';

const Limitations = () => {
  return (
    <div id="limitations" className="section">
      <SectionTitle title="Limitations" />
      <h4>Market Simulation Assumptions & Limitations</h4>
      <h6>Price/Liquidity Impact</h6>
      <p>
      Trading in micro-cap companies can have a significant impact on the market, especially given their lower liquidity compared to larger-cap stocks.
      As a result, substantial buy orders can lead to a disproportionate increase in prices due to the limited number of available shares. 
      </p>
      <p>
        As this strategy was built on the idea of "stealing" trades without impacting the market, this may ruin the efficacy of the strategy.
        The impact of "stealing" trades will likely have large affect on the market, likely making the strategy less effective than it currently is.
      </p>
      <p>
        This will need to be tested in a real environment in order to simulate real market impact.
        Starting with a few stocks would be adequate to analyze the impact, without taking too much risk.
      </p>
      
      <h4>Technical Limitations</h4>
      <h6>A poor man's laptop</h6>
      <p>
        Unsurprisingly, if trading data is gathered by-the-minute, there tends to be a <u>lot</u> of trading data.
        Building a machine-learning model on this data, then iterating through each trade how I intended would take multiple days to calculate.
        Even with as much preprocessing and optimization as I could reasonably put in, it took my computer running all night to complete.
      </p>
      <p>
        This run-time severely affected my ability to do the optimizations and analysis I really want to do. If I were blessed with a super-computer, the additional analysis I would like to look at would be:
        <li>Iterating over increasing AUMs, to determine how rapidly returns drop</li>
        <li>Optimizing calculation of ideal shares to buy/sell, rather than assumptions</li>
        <li>Running analysis on when the model made its best predictions</li>
        <li>And many, many more...</li>

      </p>

    </div>
  );
};

export default Limitations;

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
        ~~ discussion of how these trades would impact the market ~~
      </p>
      <p>
        ~~ discussion of how this may ruin the efficacy of the strategy ~~
      </p>
      <p>
        ~~ discussion sell orders and how they make some pretty big assumptions ~~
      </p>
      <p>
        ~~ discussion of how to test ~~
      </p>
      

      <h6>Trade Sizes</h6>
      <p>
        ~~ discussion of the model trades, including the average trade sizes ~~
      </p>
      <p>
        ~~ analysis of the cost of trade sizes ~~
      </p>
      <p>
        ~~ discussion of how these trades would impact the market ~~
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

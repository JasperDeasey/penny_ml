import React from 'react';
import './InvestmentStrategy.css';
import SectionTitle from '../../components/SectionTitle';
import InvestmentThesisImage from '../../data/InvestmentThesis.svg';
import ProcessFlowChart from '../../data/FlowChart.png';
import FlowchartSlideshow from '../../components/FlowchartSlideshow';

const InvestmentStrategy = () => {
  return (
    <div id="investment-strategy" className="section">
      <SectionTitle title="Strategy" />

      <div className="subsection">
      
        <div className="text-content">
        <h3>Investment Thesis</h3>
          <p>Micro-cap companies experience extreme volatility on a daily basis. Price movements of 10% within a few days is common.</p>
          <p>Despite what appears to be extreme inefficiency, investment managers may not be able to take advantage due to their high AUMs compared to the low liquidity of these assets. </p>
          <p>Our thesis stipulates that machine learning can be used identify buying opportunities, and a small fund will be able to generate superior risk-adjusted returns though smart prediction of price movements.</p>
        </div>
        <div className="visual-content">
          {/* Replace with an actual image or chart */}
          <img src={InvestmentThesisImage} alt="Investment Thesis Visual" />
        </div>
      </div>

      <div className="subsection">
        <div className="text-content">
          <h3>Implementation</h3>
          <p><b>DATA<br /></b>Data for the project is sourced through polygon.io, which has minute-by-minute trading data for US companies. Five years of data was gathered on US companies trading on NASDAQ and NYSE with market caps between $10-$50 million. Data was collected for over 600 companies.</p>
          <p><b>MODEL<br/></b>Rolling average price and volatility measures were then calculated at each trade, and the resulting data was put into a Random Forest machine learning model, which seeks to determine if a stock will move up or down 10% in the next 5 days based on those price and volatility measures. The model was trained on 4 years of data, up to the end of 2022, then 2023 data was used for the testing data.</p>
          <p><b>TRADING<br/></b>Going trade-by-trade through 2023, the program has the opportunity to "steal" each new trade, either as a buyer or a seller. Trades can only be made with the liquidity in the market (within reasonable assumptions), to not disrupt the primary advantage of this strategy - the illiquidity. The amount of each stock that is purchased is calculated to minimize risk and maximize return, further discussed in the risk section.</p>
          <p>After a stock is purchased, a sell order is created with a strike price (of 10% above the buying price) and an expiration date (of 6 days after the purchase). When each new trade arrives, the sell orders are analyzed to determine if any strike or expire. Selling can be done separately from sell orders, which reduce the oldest sell orders made. Portfolio holdings are tracked, as short selling is not permitted in this model.</p>
        </div>
        <div className="visual-content">
          <FlowchartSlideshow />
        </div>
      </div>
    </div>
  );
};

export default InvestmentStrategy;

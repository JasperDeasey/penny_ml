import React from 'react';
import './InvestmentStrategy.css';
import SectionTitle from '../../components/SectionTitle';

const InvestmentStrategy = () => {
  return (
    <div id="investment-strategy" className="section">
      <SectionTitle title="Strategy" />

      <div className="subsection">
        <div className="text-content">
          <h3>Investment Thesis</h3>
          <p>
            Our investment thesis revolves around leveraging advanced machine learning algorithms 
            to identify undervalued assets with high growth potential. We analyze vast datasets 
            encompassing market trends, economic indicators, and company performance metrics to 
            uncover hidden investment opportunities.
          </p>
        </div>
        <div className="visual-content">
          {/* Replace with an actual image or chart */}
          <img src="path-to-your-investment-thesis-visual.jpg" alt="Investment Thesis Visual" />
        </div>
      </div>

      <div className="subsection">
        <div className="text-content">
          <h3>Implementation</h3>
          <p>
            The implementation of our strategy is executed through a systematic, data-driven 
            approach. Utilizing real-time market data, our models adapt to changing market 
            conditions, dynamically adjusting asset allocations to optimize portfolio performance 
            while mitigating risk.
          </p>
        </div>
        <div className="visual-content">
          {/* Replace with an actual image or chart */}
          <img src="path-to-your-implementation-visual.jpg" alt="Implementation Visual" />
        </div>
      </div>
    </div>
  );
};

export default InvestmentStrategy;

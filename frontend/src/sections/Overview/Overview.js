import React from 'react';
import './Overview.css';
import SectionTitle from '../../components/SectionTitle';

const Overview = () => {
  return (
    <div id="overview" className="section">
        <SectionTitle title="Penny ML Overview" />
      <div className="overview-content">
        <div className="overview-text">
          <p>
            Our Quantitative Equity Fund leverages advanced machine learning algorithms 
            to analyze market trends and make data-driven investment decisions. 
            The primary goal is to maximize returns while managing risks through 
            diversified portfolios.
          </p>
          <p>
            The app's core functionality includes real-time market analysis, 
            automated trading strategies, and predictive analytics for future 
            market movements. Since its inception, the fund has achieved a 
            performance rate of 15% annual growth, with a risk factor maintained 
            at a moderate level of 2.5% volatility.
          </p>
          <p>
            This platform was built to democratize access to sophisticated 
            investment strategies, previously available only to institutions 
            and high-net-worth individuals. By harnessing the power of 
            machine learning, we offer an innovative approach to personal 
            investing.
          </p>
        </div>
        <div className="overview-visual">
          /* <img src="path-to-your-image.jpg" alt="Fund Overview Visual" /> */
        </div>
      </div>
    </div>
  );
};

export default Overview;

import React from 'react';
import './Risk.css';
import SectionTitle from '../../components/SectionTitle';
import LiquidityChart from '../../components/LiquidityChart';
import ConcentrationChart from '../../components/ConcentrationChart/ConcentrationChart';

const Risk = () => {
  return (
    <div id="risk" className="section">
      <SectionTitle title="Risk Analysis" />

      {/* Overall Risk */}
      <div className="risk-subsection">
        <p>
          Micro-cap companies are inherently riskier than large cap companies, as they typically have less predictable cash flows, higher debt, and are thinly traded.
          As a result, the largest risks in this portfolio come from too little liquidity (where we would be unable to exit a position), and single-company risk.
        </p>
      </div>

      {/* Liquidity Risk */}
      <div className="risk-subsection">
      <div className="risk-content">
        <div className="risk-commentary">
        <h3>Liquidity Risk</h3>
            <p>
              Liquidity risk refers to the ease with which assets can be converted to cash. 
              If we're unable to exit positions, we would not be able to take advantage of new positions. 
              Further, if we're expecting a large drop in value we would be unable to sell before that occurs.
            </p>
            <p>
              The liquidity risk is minimized due to the 5-day maximum holding period of each trade.
              Instead of waiting for a perfect selling opportunity to arise, we sell after 5 days if the 10% rise did not occur.
              This greatly increases liquidity.
            </p>
            <p>
              As a result, the portfolio typically has a large portion dedicated to cash.
            </p>
            <h3>Single-Company Risk</h3>
            <p>
              As these companies experience extreme price volatility, putting too much weight into any single company subjects the portfolio to risk.
              This risk is mitigated with the formula that calculates the ideal number of shares, through two mechanisms:
              <li><b>Correlation Reduction Factor:</b> There is a preference for minimizing the correlation between assets in the portfolio. If a significant portion of the portfolio is stock A, then there will be low incentive to add more of stock A, as it is correlated to the rest of the portfolio.</li>
              <li><b>Single Security Weight Reduction Factur:</b> There is a preference for buying less of a security, the more of it that is owned. In these simulations, no more of a security would be bought if it were already 5% of the portfolio. It increases exponentially the less is owned.</li>
            </p>
          </div>
        <div className='risk-data'>
              <LiquidityChart />
        </div>
      </div>
      </div>
      </div>
  );
};

export default Risk;

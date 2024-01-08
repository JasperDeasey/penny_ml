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
      <div className='content'>
      <div className="commentary">
        <p>
          The largest risks of this strategy come from the illiquidity inherent to the market, paired with the volatile nature of each holding.<br/>
          There are built-in mitigators for each of these risks, described below:
        </p>

        <h3>Liquidity Risk</h3>
            <p>
              Liquidity risk refers to the ease with which assets can be converted to cash. 
              If we're unable to exit positions, we would not be able to take advantage of new positions. 
              Further, if we're expecting a large drop in value, we would be unable to sell before that occurs.
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
              This risk is mitigated with the formula that calculates the ideal number of shares, through two mechanisms: <br/> <br/>
              <li><b>Correlation Reduction Factor:</b> There is a preference for minimizing the correlation between assets in the portfolio. If a significant portion of the portfolio is stock A, then there will be low incentive to add more of stock A, as it is correlated to the rest of the portfolio.</li><br/>
              <li><b>Single Security Weight Reduction Factor:</b> There is a preference for buying less of a security, the more of it that is owned. In these simulations, no more of a security would be bought if it were already 5% of the portfolio. It increases exponentially the less is owned.</li>
            </p>

          </div>
        <div className='chart'>
              <LiquidityChart />
        </div>
      </div>
      </div>
  );
};

export default Risk;

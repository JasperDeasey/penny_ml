import React from 'react';
import './Risk.css'; // CSS file for styling
import SectionTitle from '../../components/SectionTitle';

const Risk = () => {
  return (
    <div id="risk" className="section">
      <SectionTitle title="Risk Analysis" />

      {/* Overall Risk */}
      <div className="risk-subsection">
        <h3>Overall Risk</h3>
        <p>
          The overall risk encompasses market volatility, economic changes, and other external factors...
        </p>
        <div className="risk-visual">
          {/* Placeholder for visual - replace with actual content */}
          <img src="path-to-overall-risk-visual.jpg" alt="Overall Risk Visual" />
        </div>
      </div>

      {/* Liquidity Risk */}
      <div className="risk-subsection">
        <h3>Liquidity Risk</h3>
        <p>
          Liquidity risk refers to the ease with which assets can be converted to cash...
        </p>
        <div className="risk-visual">
          {/* Placeholder for visual - replace with actual content */}
          <img src="path-to-liquidity-risk-visual.jpg" alt="Liquidity Risk Visual" />
        </div>
      </div>

      {/* Single-Company Risk */}
      <div className="risk-subsection">
        <h3>Single-Company Risk</h3>
        <p>
          Single-company risk involves the potential for a significant impact on the fund due to...
        </p>
        <div className="risk-visual">
          {/* Placeholder for visual - replace with actual content */}
          <img src="path-to-single-company-risk-visual.jpg" alt="Single-Company Risk Visual" />
        </div>
      </div>
    </div>
  );
};

export default Risk;

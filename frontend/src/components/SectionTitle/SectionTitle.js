import React from 'react';
import './SectionTitle.css';

const SectionTitle = ({ title }) => {
  return (
    <div className="section-title">
      <h2>{title}</h2>
      <div className="title-line" />
    </div>
  );
};

export default SectionTitle;

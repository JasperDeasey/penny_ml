import React from 'react';
import { Line } from 'react-chartjs-2'; // Line is still used for area charts
import 'chart.js/auto';
import liquidity_data from '../../data/liquidity_data.json';

const LiquidityChart = () => {
  const data = {
    labels: liquidity_data['Date'],
    datasets: [
      {
        label: 'Cash',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(75, 192, 192, 0.4)',
        hoverBorderColor: 'rgba(75, 192, 192, 1)',
        pointRadius: 1.5,
        fill: true,
        data: liquidity_data['Cash'],
      },
      {
        label: 'Equity',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(153, 102, 255, 0.4)',
        hoverBorderColor: 'rgba(153, 102, 255, 1)',
        pointRadius: 1.5,
        fill: true,
        data: liquidity_data['Equity'],
      },
    ]
  };

  const options = {
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Day-End Liquidity of Portfolio'
      },
      legend: {
        position: 'bottom',
        align: 'center'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        stacked: true,
        title: {
          display: true,
          text: 'Value'
        },
      }
    },
  };

  return (
    <div style={{ height: '500px', width: '600px' }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default LiquidityChart;

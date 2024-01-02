import React from 'react';
import { Line } from 'react-chartjs-2'; // Line is still used for area charts
import 'chart.js/auto';
import concentration_data from '../../data/concentration_data.json';

const ConcentrationChart = () => {
  const data = {
    labels: concentration_data['Date'],
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
        data: concentration_data['Cash'],
      },
      {
        label: 'Top 10 Positions',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(153, 102, 255, 0.4)',
        hoverBorderColor: 'rgba(153, 102, 255, 1)',
        pointRadius: 1.5,
        fill: true,
        data: concentration_data['Top 10 Positions'],
      },
      {
        label: 'Remaining Positions',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(153, 102, 255, 0.4)',
        hoverBorderColor: 'rgba(153, 102, 255, 1)',
        pointRadius: 1.5,
        fill: true,
        data: concentration_data['Remaining Positions'],
      },
    ]
  };

  const options = {
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Position Concentration'
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
          text: '% of Portfolio'
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

export default ConcentrationChart;

import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import returnsData from '../../data/returns.json';

const ReturnsChart = () => {
  const data = {
    labels: returnsData['Date'],
    datasets: [
      {
        label: 'Penny ML',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(75, 192, 192, 0.4)',
        hoverBorderColor: 'rgba(75, 192, 192, 1)',
        pointRadius: 1.5,
        data: returnsData['Penny ML'],
      },
      {
        label: 'Equal Weighted Universe',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(153, 102, 255, 0.4)',
        hoverBorderColor: 'rgba(153, 102, 255, 1)',
        pointRadius: 1.5,
        data: returnsData['Equal Weighted Universe'],
      },
      {
        label: 'Russell Micro Cap Growth',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(255, 159, 64, 0.4)',
        hoverBorderColor: 'rgba(255, 159, 64, 1)',
        pointRadius: 1.5,
        data: returnsData['Russell Micro Cap Growth'],
      },
      {
        label: 'Russell 2000',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(54, 162, 235, 0.4)',
        hoverBorderColor: 'rgba(54, 162, 235, 1)',
        pointRadius: 1.5,
        data: returnsData['Russell 2000'],
      },
    ],
  };

  const options = {
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: true,
            text: 'Growth of a $100,000 Portfolio'
        },
        legend: {
            position: 'bottom',
            align: 'center'
            }
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div style={{ height: '300px', width: '600px' }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default ReturnsChart;

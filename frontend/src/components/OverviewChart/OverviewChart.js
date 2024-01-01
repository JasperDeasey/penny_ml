import React from 'react';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import overview_data from '../../data/overview_chart.json';

const OverviewChart = () => {
    const chartData = {
        labels: overview_data.date,
        datasets: [
            {
                type: 'line',
                label: 'Price',
                data: overview_data.price,
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.5)',
                yAxisID: 'y',
            },
            {
                type: 'bar',
                label: 'Confidence of 10% rise in value over next 5 days',
                data: overview_data.buy_prob,
                backgroundColor: 'rgba(0, 128, 0, 0.5)',
                yAxisID: 'y1',
                stack: 'prob'
            },
            {
                type: 'bar',
                label: 'Confidence of 10% drop in value over next 5 days',
                data: overview_data.sell_prob,
                backgroundColor: 'rgba(255, 0, 0, 0.5)',
                yAxisID: 'y1',
                stack: 'prob'
            }
        ],
    };

    const options = {
        scales: {
            x: { // Add x-axis configuration
                ticks: {
                    autoSkip: false, // Prevents automatic skipping of labels
                    // maxRotation: 90, // Optional: Adjusts the rotation of labels to fit them all
                    // minRotation: 90, // Optional: Sets a minimum rotation for consistency
                }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Price'
                },
                min: 1.6

            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                stacked: true,
                title: {
                    display: true,
                    text: 'Probability'
                },
                grid: {
                    drawOnChartArea: false,
                },
                min: 'auto'
            },
        },
        plugins: {
            title: {
                display: true,
                text: 'Actual Model Predictions for Micro-Cap stock', // Replace 'TITLE' with your actual title
                font: {
                    size: 18 // You can adjust the font size here
                },
                padding: {
                    top: 10,
                    bottom: 30
                }
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        responsive: true,
        maintainAspectRatio: false
    };

    return <div style={{ height: '400px' }}><Bar data={chartData} options={options} /></div>;
};

export default OverviewChart;

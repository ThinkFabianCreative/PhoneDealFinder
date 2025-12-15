import React, { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { Paper, Typography, Box } from '@mui/material';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PriceChart = ({ prices, model }) => {
  const chartData = useMemo(() => {
    // Filter prices for this model and sort by timestamp
    const modelPrices = prices
      .filter(p => p.model === model)
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    if (modelPrices.length === 0) {
      return null;
    }

    const labels = modelPrices.map(p => {
      const date = new Date(p.timestamp);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    const data = modelPrices.map(p => p.price);

    return {
      labels,
      datasets: [
        {
          label: `${model} Price`,
          data,
          borderColor: 'rgb(25, 118, 210)',
          backgroundColor: 'rgba(25, 118, 210, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    };
  }, [prices, model]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `$${context.parsed.y.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return '$' + value.toLocaleString('en-US');
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  };

  if (!chartData) {
    return (
      <Paper sx={{ p: 3, height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography color="text.secondary">No price data available for {model}</Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 3, height: '300px' }}>
      <Typography variant="h6" gutterBottom>
        {model} Price History
      </Typography>
      <Box sx={{ height: '250px', mt: 2 }}>
        <Line data={chartData} options={options} />
      </Box>
    </Paper>
  );
};

export default PriceChart;


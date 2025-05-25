import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function PriceChart({ history }) {
  if (!history || history.length === 0) return <p>No data yet.</p>;

 
  const labels = history.map(pt => {
   const iso = pt.timestamp.replace(' ', 'T');
   const d = new Date(iso);
   return d.toLocaleString();
 });
  const data = history.map(pt => pt.price);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Price over time (₹)',
        data,
        fill: false,
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
      title: { display: true, text: 'Price History' },
    },
    scales: {
      y: { beginAtZero: false },
    },
  };

  return <Line data={chartData} options={options} />;
}

import React from 'react';

export default function PricePreview({ history }) {
  if (!history || history.length === 0) return null;

  
  const { name, price, timestamp } = history[history.length - 1];
  const iso = timestamp.replace(' ', 'T');
  const date = new Date(iso);

  return (
    <div style={{ marginBottom: '1rem' }}>
      <h2>{name}</h2>
      <p>
        Current price: ₹{price.toLocaleString()}<br/>
        as of {date.toLocaleString()}
      </p>
    </div>
  );
}

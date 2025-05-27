import React from 'react';

export default function PricePreview({ history }) {
  if (!history || history.length === 0) return null;

  const { name, price, timestamp } = history[history.length - 1];
  const iso = timestamp.replace(' ', 'T');
  const date = new Date(iso);
  
  // Calculate price change
  let priceChange = null;
  let percentChange = null;
  if (history.length > 1) {
    const oldPrice = history[0].price;
    priceChange = price - oldPrice;
    percentChange = (priceChange / oldPrice) * 100;
  }

  return (
    <div className="price-preview">
      <h2 className="product-name">{name}</h2>
      <div className="price-container">
        <div className="current-price">
          <span className="price-label">Current Price</span>
          <span className="price-value">₹{price.toLocaleString()}</span>
        </div>
        
        {priceChange !== null && (
          <div className={`price-change ${priceChange < 0 ? 'decrease' : 'increase'}`}>
            <span className="change-value">
              {priceChange < 0 ? '↓' : '↑'} ₹{Math.abs(priceChange).toLocaleString()}
            </span>
            <span className="change-percent">
              ({percentChange.toFixed(1)}%)
            </span>
          </div>
        )}
      </div>
      
      <div className="timestamp">
        Last updated: {date.toLocaleString()}
      </div>
      
      <style jsx>{`
        .price-preview {
          background: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .product-name {
          margin: 0 0 1rem;
          font-size: 1.25rem;
          color: var(--text-color);
        }
        
        .price-container {
          margin-bottom: 1rem;
        }
        
        .current-price {
          display: flex;
          flex-direction: column;
          margin-bottom: 0.5rem;
        }
        
        .price-label {
          font-size: 0.875rem;
          color: #64748b;
        }
        
        .price-value {
          font-size: 2rem;
          font-weight: 700;
          color: var(--text-color);
        }
        
        .price-change {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
        }
        
        .price-change.decrease {
          color: var(--error-color);
        }
        
        .price-change.increase {
          color: var(--success-color);
        }
        
        .change-value {
          font-weight: 600;
        }
        
        .change-percent {
          color: #64748b;
        }
        
        .timestamp {
          font-size: 0.875rem;
          color: #64748b;
        }
      `}</style>
    </div>
  );
}
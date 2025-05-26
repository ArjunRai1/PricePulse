import React, { useState } from 'react';

export default function TrackForm({ onTracked }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState('');
  const [email, setEmail] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    if (!url) return;
    setLoading(true);
    setError('');
   
    try {
      
      await fetch('/api/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      
      
      const res = await fetch(`/api/history?url=${encodeURIComponent(url)}`);
      const data = await res.json();
      onTracked(data.history, url);

      
      if (email && targetPrice) {
        const alertRes = await fetch('/api/alerts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url,
            email,
            target_price: parseFloat(targetPrice)
          }),
        });
        
        if (!alertRes.ok) {
          const alertData = await alertRes.json();
          throw new Error(alertData.error || 'Failed to set price alert');
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
        <div style={{ marginBottom: '1rem' }}>
          <input 
            type="url" 
            placeholder="Enter Amazon product URL" 
            value={url} 
            onChange={e => setUrl(e.target.value)} 
            style={{ width: '100%', padding: '0.5rem' }} 
            required
          />
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <input
            type="email"
            placeholder="Email for price alerts (optional)"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{ flex: 1, padding: '0.5rem' }}
          />
          <input
            type="number"
            placeholder="Target price (optional)"
            value={targetPrice}
            onChange={e => setTargetPrice(e.target.value)}
            style={{ width: '150px', padding: '0.5rem' }}
            min="0"
            step="0.01"
          />
        </div>
        
        <button 
          type="submit" 
          disabled={loading}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Loading…' : 'Track Price'}
        </button>
      </form>
      
      {error && (
        <div style={{ color: 'red', marginBottom: '1rem' }}>
          {error}
        </div>
      )}
    </div>
  );
}

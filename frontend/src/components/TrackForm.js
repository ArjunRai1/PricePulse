import React, { useState } from 'react';

export default function TrackForm({ onTracked }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!url) return;
    setLoading(true);
   
    await fetch('/api/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    
    const res = await fetch(`/api/history?url=${encodeURIComponent(url)}`);
    const data = await res.json();
    onTracked(data.history, url);
    setLoading(false);
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
      <input
        type="url"
        placeholder="Enter Amazon product URL"
        value={url}
        onChange={e => setUrl(e.target.value)}
        style={{ width: '70%' }}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Loading…' : 'Track'}
      </button>
    </form>
  );
}

import React, { useState, useEffect, useRef } from 'react';
import PricePreview from './components/PricePreview';
import PriceChart from './components/PriceChart';
import TrackForm from './components/TrackForm';


function App() {
  const [history, setHistory] = useState([]);
  const [currentUrl, setCurrentUrl] = useState('');
  const intervalId = useRef(null);

  function handleTracked(newHistory, url) {
    setHistory(newHistory);
    setCurrentUrl(url);
    if (intervalId.current) clearInterval(intervalId.current);
    intervalId.current = setInterval(() => {
      fetchHistory(url);
    }, 1_800_000);
  }

  useEffect(() => {
    return () => clearInterval(intervalId.current);
  }, []);

  async function fetchHistory(url) {
  const res = await fetch(`/api/history?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  setHistory(data.history);
}

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>PricePulse Dashboard</h1>
      <TrackForm onTracked={handleTracked} />

      {currentUrl && (
        <>
          <PricePreview history={history} />
          <PriceChart history={history} />
        </>
      )}
    </div>
  );
}

export default App;

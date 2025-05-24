import React, { useState } from 'react';
import PricePreview from './components/PricePreview';
import PriceChart from './components/PriceChart';
import TrackForm from './components/TrackForm';

function App() {
  const [history, setHistory] = useState([]);
  const [currentUrl, setCurrentUrl] = useState('');

  function handleTracked(newHistory, url) {
    setHistory(newHistory);
    setCurrentUrl(url);
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

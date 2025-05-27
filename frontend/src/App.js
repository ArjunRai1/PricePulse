import React, { useState, useEffect, useRef } from 'react';
import PricePreview from './components/PricePreview';
import PriceChart from './components/PriceChart';
import TrackForm from './components/TrackForm';
import './App.css';

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
    const res = await fetch(`${API_BASE}/api/history?url=${encodeURIComponent(url)}`);
    const data = await res.json();
    setHistory(data.history);
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>PricePulse</h1>
          <p className="subtitle">Track Amazon prices effortlessly</p>
        </div>
      </header>
      
      <main className="main-content">
        <div className="track-section">
          <TrackForm onTracked={handleTracked} />
        </div>

        {currentUrl && (
          <div className="data-section">
            <PricePreview history={history} />
            <div className="chart-container">
              <PriceChart history={history} />
            </div>
          </div>
        )}
      </main>
      
      <footer className="app-footer">
        <p>© 2024 PricePulse. All rights reserved.</p>
      </footer>
    </div>
  );
}
export default App;
import React from 'react';

function App() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>PricePulse</h1>
      <form>
        <input type="text" placeholder="Amazon product URL" style={{ width: 300 }} />
        <button type="submit">Track Price</button>
      </form>
    </div>
  );
}

export default App;

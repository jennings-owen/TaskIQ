import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACK_END_URL}/status`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStatus(data);
      } catch (err) {
        setError("Failed to fetch status from the backend.");
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Capstone Project - Synapse Squad Team 4
        </p>
      </header>
      
      <footer className="App-footer">
        {loading && <div>Loading status...</div>}
        {error && <div className="status-error">Status Error: {error}</div>}
        {status && (
          <div>
            API Status: <span className={status.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}>
              {status.status}
            </span> | {status.message} | Version: {status.version}
          </div>
        )}
      </footer>
    </div>
  );
}

export default App;

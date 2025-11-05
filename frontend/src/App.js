import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';

function App() {
  const [selectedView, setSelectedView] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
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

  const handleMenuToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  const renderMainContent = () => {
    switch (selectedView) {
      case 'dashboard':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">Dashboard</h2>
              <p className="text-gray-500 mb-8">Welcome to Agile TaskIQ Dashboard</p>
              
              {/* Status information */}
              <div className="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
                <h3 className="text-lg font-medium text-gray-800 mb-4">System Status</h3>
                {loading && <div className="text-blue-600">Loading status...</div>}
                {error && <div className="text-red-600">Status Error: {error}</div>}
                {status && (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">API Status:</span>
                      <span className={status.status === 'healthy' ? 'text-green-600 font-medium' : 'text-red-600 font-medium'}>
                        {status.status}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Message:</span>
                      <span className="text-gray-800">{status.message}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Version:</span>
                      <span className="text-gray-800">{status.version}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      case 'tasks':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">Tasks</h2>
              <p className="text-gray-500">Task management features coming soon</p>
            </div>
          </div>
        );
      case 'ai-tools':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">AI Tools</h2>
              <p className="text-gray-500">AI-powered task management tools coming soon</p>
            </div>
          </div>
        );
      case 'settings':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">Settings</h2>
              <p className="text-gray-500">Application settings coming soon</p>
            </div>
          </div>
        );
      default:
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600">Welcome</h2>
              <p className="text-gray-500 mt-2">Select a view from the sidebar</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col lg:flex-row">
      {/* Top Bar - Mobile only */}
      <TopBar onMenuToggle={handleMenuToggle} />
      
      {/* Sidebar */}
      <Sidebar 
        selectedView={selectedView}
        onSelectView={setSelectedView}
        isOpen={isSidebarOpen}
        onClose={handleSidebarClose}
      />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <main className="flex-1 p-6 overflow-auto">
          <div className="container">
            {renderMainContent()}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;

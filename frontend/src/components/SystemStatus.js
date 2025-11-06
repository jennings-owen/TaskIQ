import React from 'react';
import { Activity } from 'lucide-react';

const SystemStatus = ({ status, loading, error, user }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">System Status</h3>
          <p className="text-sm text-gray-500">Current system and user information</p>
        </div>
      </div>
      
      {loading && <div className="text-blue-600">Loading status...</div>}
      {error && <div className="text-red-600">Status Error: {error}</div>}
      {status && (
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <span className="text-gray-600 font-medium">API Status:</span>
            <span className={status.status === 'healthy' ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'}>
              {status.status}
            </span>
          </div>
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <span className="text-gray-600 font-medium">Message:</span>
            <span className="text-gray-800">{status.message}</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <span className="text-gray-600 font-medium">Version:</span>
            <span className="text-gray-800">{status.version}</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-gray-600 font-medium">Logged in as:</span>
            <span className="text-gray-800 font-medium">{user?.name}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default SystemStatus;
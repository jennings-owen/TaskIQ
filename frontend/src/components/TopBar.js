import React from 'react';
import { Menu, User, Sparkles } from 'lucide-react';

const TopBar = ({ onMenuToggle }) => {
  return (
    <div className="lg:hidden bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
      {/* Left side - Menu button and brand */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="btn btn-outline"
        >
          <Menu className="icon w-6 h-6 text-gray-600" />
        </button>
        
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-blue-500 rounded flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="text-gray-900 font-semibold">Agile TaskIQ</span>
        </div>
      </div>

      {/* Right side - User profile */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
          <User className="w-4 h-4 text-gray-600" />
        </div>
      </div>
    </div>
  );
};

export default TopBar;
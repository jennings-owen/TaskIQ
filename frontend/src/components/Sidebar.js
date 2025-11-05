import React from 'react';
import { 
  LayoutDashboard, 
  CheckSquare, 
  Sparkles, 
  Settings, 
  LogOut, 
  User,
  X
} from 'lucide-react';
import clsx from 'clsx';

const Sidebar = ({ selectedView, onSelectView, isOpen, onClose }) => {
  const navItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
    },
    {
      id: 'tasks',
      label: 'Tasks',
      icon: CheckSquare,
    },
    {
      id: 'ai-tools',
      label: 'AI Tools',
      icon: Sparkles,
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: Settings,
    },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={clsx(
        "fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200 flex flex-col z-50 sidebar-transition",
        "lg:relative lg:translate-x-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {/* Header */}
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-gray-900 font-semibold">Agile TaskIQ</span>
          </div>
          
          {/* Close button for mobile */}
          <button
            onClick={onClose}
            className="lg:hidden p-1 rounded hover:bg-gray-100"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
          
          {/* User Avatar for desktop */}
          <div className="hidden lg:flex w-9 h-9 bg-gray-200 rounded-full items-center justify-center">
            <User className="w-5 h-5 text-gray-600" />
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <div className="text-gray-500 text-xs mb-2 px-3 uppercase tracking-wider">
            Menu
          </div>
          <div className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onSelectView(item.id);
                    onClose(); // Close sidebar on mobile when item is selected
                  }}
                  className={clsx(
                    "nav-item transition-colors",
                    selectedView === item.id
                      ? "active"
                      : "text-gray-600 hover:bg-gray-50"
                  )}
                >
                  <span className="icon"><Icon className="w-5 h-5" /></span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200">
          <button className="nav-item w-full flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
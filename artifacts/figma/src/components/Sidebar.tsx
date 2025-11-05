import { LayoutDashboard, CheckSquare, Sparkles, Settings, LogOut, User } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Button } from './ui/button';

interface SidebarProps {
  selectedView: 'dashboard' | 'tasks' | 'ai-tools' | 'settings';
  onSelectView: (view: 'dashboard' | 'tasks' | 'ai-tools' | 'settings') => void;
}

export function Sidebar({ selectedView, onSelectView }: SidebarProps) {
  return (
    <div className="w-64 bg-white border-r border-slate-200 flex flex-col">
      <div className="p-6 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-slate-900">Agile TaskIQ</span>
        </div>
        <Avatar className="w-9 h-9">
          <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=user" />
          <AvatarFallback>U</AvatarFallback>
        </Avatar>
      </div>

      <nav className="flex-1 p-4">
        <div className="text-slate-500 text-xs mb-2 px-3">Menu</div>
        <div className="space-y-1">
          <button
            onClick={() => onSelectView('dashboard')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              selectedView === 'dashboard'
                ? 'bg-blue-50 text-blue-600'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <LayoutDashboard className="w-5 h-5" />
            <span>Dashboard</span>
          </button>

          <button
            onClick={() => onSelectView('tasks')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              selectedView === 'tasks'
                ? 'bg-blue-50 text-blue-600'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <CheckSquare className="w-5 h-5" />
            <span>Tasks</span>
          </button>

          <button
            onClick={() => onSelectView('ai-tools')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              selectedView === 'ai-tools'
                ? 'bg-blue-50 text-blue-600'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <Sparkles className="w-5 h-5" />
            <span>AI Tools</span>
          </button>

          <button
            onClick={() => onSelectView('settings')}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
              selectedView === 'settings'
                ? 'bg-blue-50 text-blue-600'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <Settings className="w-5 h-5" />
            <span>Settings</span>
          </button>
        </div>
      </nav>

      <div className="p-4 border-t border-slate-200">
        <Button variant="ghost" className="w-full justify-start gap-3 text-slate-600">
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </Button>
      </div>
    </div>
  );
}

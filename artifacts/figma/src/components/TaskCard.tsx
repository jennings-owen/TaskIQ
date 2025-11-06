import { Task } from '../App';
import { Badge } from './ui/badge';
import { Circle, CheckCircle2 } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  isSelected: boolean;
  onSelect: () => void;
}

export function TaskCard({ task, isSelected, onSelect }: TaskCardProps) {
  const getPriorityLevel = (score: number): { label: string; variant: 'default' | 'secondary' | 'destructive' } => {
    if (score >= 70) return { label: 'High', variant: 'destructive' };
    if (score >= 40) return { label: 'Medium', variant: 'default' };
    return { label: 'Low', variant: 'secondary' };
  };

  const calculateDaysUntilDeadline = (deadline: string): number => {
    const deadlineDate = new Date(deadline);
    const today = new Date();
    
    deadlineDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    
    return Math.floor((deadlineDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
  };

  const priority = getPriorityLevel(task.priority_score);
  const daysUntil = calculateDaysUntilDeadline(task.deadline);

  return (
    <button
      onClick={onSelect}
      className={`w-full text-left p-4 rounded-lg border transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50'
          : 'border-slate-200 bg-white hover:border-slate-300'
      }`}
    >
      <div className="flex items-start gap-3">
        {task.status === 'completed' ? (
          <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
        ) : (
          <Circle className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
        )}
        <div className="flex-1 min-w-0">
          <h3 className="text-slate-900 mb-1">{task.title}</h3>
          <p className="text-slate-500 text-sm mb-3">{task.description}</p>
          
          <div className="flex items-center gap-2 flex-wrap">
            <div className="flex items-center gap-1">
              <span className="text-slate-500 text-xs">Due:</span>
              <span className={`text-xs font-medium ${
                daysUntil < 0 ? 'text-red-600' : 
                daysUntil === 0 ? 'text-orange-600' : 
                daysUntil <= 3 ? 'text-yellow-600' : 'text-slate-700'
              }`}>
                {new Date(task.deadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                {daysUntil === 0 ? ' (Today!)' : 
                 daysUntil < 0 ? ` (${Math.abs(daysUntil)}d overdue)` :
                 daysUntil <= 7 ? ` (${daysUntil}d)` : ''}
              </span>
            </div>
            <Badge variant={priority.variant} className="text-xs">
              {priority.label}
            </Badge>
            <Badge variant="outline" className="text-xs">
              {task.priority_score}
            </Badge>
            {task.tshirt_size && (
              <Badge variant="secondary" className="text-xs">
                {task.tshirt_size}
              </Badge>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

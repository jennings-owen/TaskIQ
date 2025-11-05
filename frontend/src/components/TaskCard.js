import { Badge } from './ui/badge';
import { Circle, CheckCircle2 } from 'lucide-react';

export function TaskCard({ task, isSelected, onSelect }) {
  const getPriorityLevel = (score) => {
    if (score >= 70) return { label: 'High', variant: 'destructive' };
    if (score >= 40) return { label: 'Medium', variant: 'default' };
    return { label: 'Low', variant: 'secondary' };
  };

  const priority = getPriorityLevel(task.priority_score);

  return (
    <button
      onClick={onSelect}
      className={`w-full text-left p-3 lg:p-4 rounded-lg border transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50'
          : 'border-slate-200 bg-white hover:border-slate-300'
      }`}
    >
      <div className="flex items-start gap-2 lg:gap-3">
        {task.status === 'completed' ? (
          <CheckCircle2 className="w-4 h-4 lg:w-5 lg:h-5 text-green-500 flex-shrink-0 mt-0.5" />
        ) : (
          <Circle className="w-4 h-4 lg:w-5 lg:h-5 text-slate-400 flex-shrink-0 mt-0.5" />
        )}
        <div className="flex-1 min-w-0">
          <h3 className="text-slate-900 mb-1 text-sm lg:text-base font-medium">{task.title}</h3>
          <p className="text-slate-500 text-xs lg:text-sm mb-2 lg:mb-3 line-clamp-2 lg:line-clamp-none">
            {task.description}
          </p>
          
          <div className="flex items-center gap-1 lg:gap-2 flex-wrap">
            <span className="text-slate-500 text-xs">
              Due: {new Date(task.deadline).toLocaleDateString()}
            </span>
            <Badge variant={priority.variant} className="text-xs">
              {priority.label}
            </Badge>
            <Badge variant="outline" className="text-xs">
              {task.priority_score}
            </Badge>
            {task.tshirt_size && (
              <Badge variant="secondary" className="text-xs hidden lg:inline-flex">
                {task.tshirt_size}
              </Badge>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}
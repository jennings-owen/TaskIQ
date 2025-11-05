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

  const priority = getPriorityLevel(task.priority_score);

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

import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Task } from '../App';
import { TaskCard } from './TaskCard';
import { CreateTaskDialog } from './CreateTaskDialog';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';

interface TaskListProps {
  tasks: Task[];
  selectedTask: Task | null;
  onSelectTask: (task: Task) => void;
  onCreateTask: (task: Omit<Task, 'id' | 'priority_score'>) => void;
  compact?: boolean;
}

export function TaskList({ tasks, selectedTask, onSelectTask, onCreateTask, compact = false }: TaskListProps) {
  const [filterPriority, setFilterPriority] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const [showHighPriorityOnly, setShowHighPriorityOnly] = useState(false);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const filteredTasks = tasks.filter(task => {
    if (showHighPriorityOnly && task.priority_score < 70) return false;
    
    if (filterPriority === 'all') return true;
    if (filterPriority === 'high') return task.priority_score >= 70;
    if (filterPriority === 'medium') return task.priority_score >= 40 && task.priority_score < 70;
    if (filterPriority === 'low') return task.priority_score < 40;
    return true;
  }).sort((a, b) => b.priority_score - a.priority_score);

  return (
    <div className={`${compact ? 'w-full' : 'w-[400px]'} bg-white rounded-lg border border-slate-200 flex flex-col`}>
      <div className={`${compact ? 'p-4' : 'p-6'} border-b border-slate-200`}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-slate-900">{compact ? 'Select Task' : 'Task List'}</h2>
          {compact && (
            <Badge variant="secondary">{filteredTasks.length} tasks</Badge>
          )}
        </div>
        
        {!compact && (
          <div className="flex items-center gap-2 flex-wrap">
            <Button
              variant={filterPriority === 'all' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilterPriority('all')}
            >
              All Statuses
            </Button>
            <Button
              variant={filterPriority === 'high' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilterPriority('high')}
            >
              High Priority
            </Button>
            <Button
              variant={filterPriority === 'medium' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilterPriority('medium')}
            >
              Medium
            </Button>
            <div className="flex items-center gap-2 ml-auto">
              <Switch
                checked={showHighPriorityOnly}
                onCheckedChange={setShowHighPriorityOnly}
              />
            </div>
          </div>
        )}
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-3">
        {filteredTasks.map(task => (
          <TaskCard
            key={task.id}
            task={task}
            isSelected={selectedTask?.id === task.id}
            onSelect={() => onSelectTask(task)}
          />
        ))}
        {filteredTasks.length === 0 && (
          <div className="text-center py-8 text-slate-400">
            No tasks found
          </div>
        )}
      </div>

      {!compact && (
        <div className="p-4 border-t border-slate-200">
          <Button 
            className="w-full" 
            onClick={() => setIsCreateDialogOpen(true)}
          >
            <Plus className="w-4 h-4 mr-2" />
            New Task
          </Button>
        </div>
      )}

      <CreateTaskDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onCreateTask={onCreateTask}
      />
    </div>
  );
}

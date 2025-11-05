import { useState } from 'react';
import { Plus } from 'lucide-react';
import { TaskCard } from './TaskCard';
import { CreateTaskDialog } from './CreateTaskDialog';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';

export function TaskList({ tasks, selectedTask, onSelectTask, onCreateTask }) {
  const [filterPriority, setFilterPriority] = useState('all');
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
    <div className="w-full bg-white rounded-lg border border-slate-200 flex flex-col lg:max-h-none max-h-80">
      <div className="p-4 lg:p-6 border-b border-slate-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg lg:text-xl text-slate-900">Task List</h2>
          <Badge variant="secondary" className="lg:hidden">{filteredTasks.length} tasks</Badge>
        </div>
        
        <div className="flex items-center gap-2 flex-wrap">
          <Button
            variant={filterPriority === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterPriority('all')}
            className="text-xs lg:text-sm"
          >
            All Statuses
          </Button>
          <Button
            variant={filterPriority === 'high' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterPriority('high')}
            className="text-xs lg:text-sm"
          >
            High Priority
          </Button>
          <Button
            variant={filterPriority === 'medium' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterPriority('medium')}
            className="text-xs lg:text-sm hidden lg:inline-flex"
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

      <div className="p-4 border-t border-slate-200">
        <Button 
          className="w-full" 
          onClick={() => setIsCreateDialogOpen(true)}
        >
          <Plus className="w-4 h-4 mr-2" />
          New Task
        </Button>
      </div>

      <CreateTaskDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onCreateTask={onCreateTask}
      />
    </div>
  );
}
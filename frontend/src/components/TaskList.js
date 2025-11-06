import { useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { TaskCard } from './TaskCard';
import { CreateTaskDialog } from './CreateTaskDialog';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';

export function TaskList({ tasks, selectedTask, onSelectTask, onCreateTask }) {
  const [selectedPriorities, setSelectedPriorities] = useState(['all']);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const handlePriorityToggle = (priority) => {
    if (priority === 'all') {
      setSelectedPriorities(['all']);
    } else {
      setSelectedPriorities(prev => {
        const filtered = prev.filter(p => p !== 'all');
        if (filtered.includes(priority)) {
          const newSelection = filtered.filter(p => p !== priority);
          return newSelection.length === 0 ? ['all'] : newSelection;
        } else {
          return [...filtered, priority];
        }
      });
    }
  };

  const filteredTasks = tasks.filter(task => {
    // Priority filter - support multiple selections
    const passesPriorityFilter = (() => {
      if (selectedPriorities.includes('all')) return true;
      
      const taskPriorityLevel = (() => {
        if (task.priority_score >= 70) return 'high';
        if (task.priority_score >= 40) return 'medium';
        return 'low';
      })();
      
      return selectedPriorities.includes(taskPriorityLevel);
    })();

    // Search filter
    const passesSearchFilter = searchTerm === '' || 
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(searchTerm.toLowerCase());

    return passesPriorityFilter && passesSearchFilter;
  }).sort((a, b) => b.priority_score - a.priority_score);

  return (
    <div className="w-full bg-white rounded-lg border border-slate-200 flex flex-col lg:max-h-none max-h-80">
      <div className="p-4 lg:p-6 border-b border-slate-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg lg:text-xl text-slate-900">My Tasks</h2>
          <Badge variant="secondary" className="lg:hidden">{filteredTasks.length} tasks</Badge>
        </div>
        
        <div className="mb-4">
          <Button 
            className="w-full" 
            onClick={() => setIsCreateDialogOpen(true)}
          >
            <Plus className="w-4 h-4 mr-2" />
            New Task
          </Button>
        </div>

        <div className="mb-4">
          <div className="flex items-center gap-2">
            Search:
            <Input
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9"
            />
          </div>
        </div>
        
        <div className="flex items-center gap-2 flex-wrap">
          <h4>Priority:</h4>
          <Button
            variant={selectedPriorities.includes('all') ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePriorityToggle('all')}
            className="text-xs lg:text-sm"
          >
            All
          </Button>
          <Button
            variant={selectedPriorities.includes('high') ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePriorityToggle('high')}
            className="text-xs lg:text-sm"
          >
            High
          </Button>
          <Button
            variant={selectedPriorities.includes('medium') ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePriorityToggle('medium')}
            className="text-xs lg:text-sm hidden lg:inline-flex"
          >
            Medium
          </Button>
          <Button
            variant={selectedPriorities.includes('low') ? 'default' : 'outline'}
            size="sm"
            onClick={() => handlePriorityToggle('low')}
            className="text-xs lg:text-sm"
          >
            Low
          </Button>
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

      <CreateTaskDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onCreateTask={onCreateTask}
      />
    </div>
  );
}
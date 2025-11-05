import { useState, useEffect } from 'react';
import { Search, Trash2, Sparkles } from 'lucide-react';
import { Task } from '../App';
import { toast } from 'sonner@2.0.3';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Slider } from './ui/slider';
import { Badge } from './ui/badge';

interface TaskDetailsPanelProps {
  task: Task | null;
  onUpdateTask: (task: Task) => void;
  onDeleteTask: (id: number) => void;
}

export function TaskDetailsPanel({ task, onUpdateTask, onDeleteTask }: TaskDetailsPanelProps) {
  const [editedTask, setEditedTask] = useState<Task | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (task) {
      setEditedTask(task);
    }
  }, [task]);

  if (!task || !editedTask) {
    return (
      <div className="flex-1 bg-white rounded-lg border border-slate-200 flex items-center justify-center">
        <div className="text-center text-slate-400">
          <p>Select a task to view details</p>
        </div>
      </div>
    );
  }

  const handleSave = () => {
    onUpdateTask(editedTask);
    toast.success('Task updated!', {
      description: 'AI priority score has been recalculated',
      icon: <Sparkles className="w-4 h-4" />,
    });
  };

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this task?')) {
      onDeleteTask(task.id);
    }
  };

  const getPriorityLevel = (score: number) => {
    if (score >= 70) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  return (
    <div className="flex-1 bg-white rounded-lg border border-slate-200 flex flex-col">
      <div className="p-6 border-b border-slate-200">
        <h2 className="text-slate-900 mb-4">Task Details & Actions</h2>
        
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6 space-y-6">
        <div className="space-y-2">
          <Label>Title</Label>
          <Input
            value={editedTask.title}
            onChange={(e) => setEditedTask({ ...editedTask, title: e.target.value })}
          />
        </div>

        <div className="space-y-2">
          <Label>Description</Label>
          <Textarea
            value={editedTask.description}
            onChange={(e) => setEditedTask({ ...editedTask, description: e.target.value })}
            rows={4}
          />
        </div>

        <div className="space-y-2">
          <Label>Status</Label>
          <Select
            value={editedTask.status}
            onValueChange={(value: Task['status']) => 
              setEditedTask({ ...editedTask, status: value })
            }
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="in-progress">In Progress</SelectItem>
              <SelectItem value="completed">Completed</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Deadline</Label>
          <Input
            type="date"
            value={editedTask.deadline}
            onChange={(e) => setEditedTask({ ...editedTask, deadline: e.target.value })}
          />
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label>Priority Score</Label>
            <Badge variant={editedTask.priority_score >= 70 ? 'destructive' : 'default'}>
              {getPriorityLevel(editedTask.priority_score)}
            </Badge>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-slate-900">{editedTask.priority_score}</span>
            <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${
                  editedTask.priority_score >= 70
                    ? 'bg-red-500'
                    : editedTask.priority_score >= 40
                    ? 'bg-yellow-500'
                    : 'bg-green-500'
                }`}
                style={{ width: `${editedTask.priority_score}%` }}
              />
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <Label>T-Shirt Size (Complexity)</Label>
          <div className="flex gap-2">
            {(['XS', 'S', 'M', 'L', 'XL'] as const).map((size) => (
              <Button
                key={size}
                type="button"
                variant={editedTask.tshirt_size === size ? 'default' : 'outline'}
                size="sm"
                className="flex-1"
                onClick={() => setEditedTask({ ...editedTask, tshirt_size: size })}
              >
                {size}
              </Button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <Label>Estimated Duration</Label>
          <Slider
            value={[editedTask.estimated_duration]}
            onValueChange={([value]) => 
              setEditedTask({ ...editedTask, estimated_duration: value })
            }
            min={1}
            max={24}
            step={1}
          />
          <p className="text-slate-500 text-sm">{editedTask.estimated_duration} hours</p>
        </div>

        {/* AI Priority Score Info */}
        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-blue-600" />
            <Label className="text-blue-900">AI Priority Score</Label>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="text-lg px-3 py-1">
              {editedTask.priority_score}
            </Badge>
            <span className="text-sm text-blue-700">
              {getPriorityLevel(editedTask.priority_score)} Priority
            </span>
          </div>
          <p className="text-xs text-blue-600 mt-2">
            Score will be recalculated on save based on deadline and duration
          </p>
        </div>
      </div>

      <div className="p-6 border-t border-slate-200 flex gap-3">
        <Button onClick={handleSave} className="flex-1">
          <Sparkles className="w-4 h-4 mr-2" />
          Save Changes
        </Button>
        <Button onClick={handleDelete} variant="destructive" size="icon">
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}

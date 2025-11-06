import { useState, useEffect } from 'react';
import { Trash2, Edit, X } from 'lucide-react';
import { toast } from 'sonner';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Slider } from './ui/slider';
import { Badge } from './ui/badge';

export function TaskDetailsPanel({ task, onUpdateTask, onDeleteTask }) {
  const [editedTask, setEditedTask] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (task) {
      // Ensure priority_score has a valid value
      const taskWithDefaults = {
        ...task,
        priority_score: task.priority_score || 50, // Default to 50 if not set
        tshirt_size: task.tshirt_size || 'M' // Default to M if not set
      };
      setEditedTask(taskWithDefaults);
      setIsEditing(false); // Reset to view mode when task changes
    }
  }, [task]);

  // Helper function to format date for input[type="date"]
  const formatDateForInput = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      // Return in YYYY-MM-DD format
      return date.toISOString().split('T')[0];
    } catch (error) {
      console.error('Error formatting date:', error);
      return '';
    }
  };

  // Helper function to format date for display
  const formatDateForDisplay = (dateString) => {
    if (!dateString) return 'Not set';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch (error) {
      console.error('Error formatting date:', error);
      return 'Invalid date';
    }
  };

  if (!task || !editedTask) {
    return (
      <div className="bg-white rounded-lg border border-slate-200 flex items-center justify-center min-h-64 h-full">
        <div className="text-center text-slate-400">
          <p>Select a task to view details</p>
        </div>
      </div>
    );
  }

  const handleSave = () => {
    onUpdateTask(editedTask);
    setIsEditing(false);
    toast.success('Task updated!');
  };

  const handleCancel = () => {
    setEditedTask(task); // Reset to original task data
    setIsEditing(false);
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onDeleteTask(task.id);
    }
  };

  const getPriorityLevel = (score) => {
    if (score >= 70) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 flex flex-col h-full">
      <div className="p-4 lg:p-6 border-b border-slate-200 flex-shrink-0">
        <h2 className="text-lg lg:text-xl text-slate-900">
          {isEditing ? 'Edit Task' : task.title}
        </h2>
      </div>

      <div className="flex-1 overflow-auto p-4 lg:p-6 space-y-4 lg:space-y-6">
        {isEditing ? (
          // Edit Mode - Form
          <>
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
                rows={3}
                className="resize-none lg:min-h-24"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Status</Label>
                <Select
                  value={editedTask.status}
                  onValueChange={(value) => 
                    setEditedTask({ ...editedTask, status: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="blocked">Blocked</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Deadline</Label>
                <Input
                  type="date"
                  value={formatDateForInput(editedTask.deadline)}
                  onChange={(e) => setEditedTask({ ...editedTask, deadline: e.target.value })}
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Priority Score</Label>
                <Badge variant={(editedTask.priority_score || 50) >= 70 ? 'destructive' : (editedTask.priority_score || 50) >= 40 ? 'default' : 'secondary'}>
                  {getPriorityLevel(editedTask.priority_score || 50)}
                </Badge>
              </div>
              <Slider
                value={[editedTask.priority_score || 50]}
                onValueChange={([value]) => 
                  setEditedTask({ ...editedTask, priority_score: value })
                }
                min={1}
                max={100}
                step={1}
              />
              <div className="flex items-center justify-between text-sm text-slate-500">
                <span>Low (1)</span>
                <span className="text-slate-900 font-medium">{editedTask.priority_score || 50}</span>
                <span>High (100)</span>
              </div>
            </div>

            <div className="space-y-2">
              <Label>T-Shirt Size (Complexity)</Label>
              <div className="grid grid-cols-5 gap-2">
                {(['XS', 'S', 'M', 'L', 'XL']).map((size) => (
                  <Button
                    key={size}
                    type="button"
                    variant={editedTask.tshirt_size === size ? 'default' : 'outline'}
                    size="sm"
                    className="text-xs lg:text-sm"
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
          </>
        ) : (
          // View Mode - Pretty Display
          <>
            <div className="space-y-6">
              <div>
                <p className="text-slate-600 leading-relaxed">
                  {task.description || 'No description provided'}
                </p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium text-slate-700">Status</Label>
                    <div className="mt-1">
                      <Badge 
                        variant={
                          task.status === 'completed' ? 'default' :
                          task.status === 'in_progress' ? 'secondary' :
                          task.status === 'blocked' ? 'destructive' : 'outline'
                        }
                        className="capitalize"
                      >
                        {task.status?.replace('_', ' ')}
                      </Badge>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-slate-700">Deadline</Label>
                    <p className="mt-1 text-slate-900">{formatDateForDisplay(task.deadline)}</p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-slate-700">T-Shirt Size</Label>
                    <div className="mt-1">
                      <Badge variant="outline" className="font-mono">
                        {task.tshirt_size || 'Not set'}
                      </Badge>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium text-slate-700">Priority</Label>
                    <div className="mt-1 flex items-center gap-2">
                      <Badge variant={task.priority_score >= 70 ? 'destructive' : task.priority_score >= 40 ? 'default' : 'secondary'}>
                        {getPriorityLevel(task.priority_score)}
                      </Badge>
                      <span className="text-slate-600">({task.priority_score}/100)</span>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-slate-700">Estimated Duration</Label>
                    <p className="mt-1 text-slate-900">{task.estimated_duration} hours</p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-slate-700">Created</Label>
                    <p className="mt-1 text-slate-600 text-sm">
                      {formatDateForDisplay(task.created_at)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      <div className="p-4 lg:p-6 border-t border-slate-200 flex flex-col lg:flex-row gap-3 flex-shrink-0">
        {isEditing ? (
          <>
            <Button onClick={handleSave} className="lg:w-auto">
              Save Changes
            </Button>
            <Button onClick={handleCancel} variant="outline" className="lg:w-auto">
              <X className="w-4 h-4 lg:mr-2" />
              <span className="lg:inline hidden">Cancel</span>
            </Button>
          </>
        ) : (
          <>
            <Button onClick={handleEdit} variant="outline" className="lg:w-auto">
              <Edit className="w-4 h-4 lg:mr-2" />
              <span className="lg:inline hidden">Edit</span>
            </Button>
            <Button onClick={handleDelete} variant="destructive" className="lg:w-auto">
              <Trash2 className="w-4 h-4 lg:mr-2" />
              <span className="lg:inline hidden">Delete</span>
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
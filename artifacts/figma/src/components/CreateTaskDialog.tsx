import { useState, useEffect } from 'react';
import { AlertCircle, Sparkles, TrendingUp } from 'lucide-react';
import { Task } from '../App';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from './ui/dialog';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Alert, AlertDescription } from './ui/alert';
import { Badge } from './ui/badge';
import { Slider } from './ui/slider';

interface CreateTaskDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreateTask: (task: Omit<Task, 'id' | 'priority_score'>) => void;
}

export function CreateTaskDialog({ open, onOpenChange, onCreateTask }: CreateTaskDialogProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [deadline, setDeadline] = useState('');
  const [status, setStatus] = useState<Task['status']>('pending');
  const [estimatedDuration, setEstimatedDuration] = useState(4);
  const [tshirtSize, setTshirtSize] = useState<Task['tshirt_size']>('M');
  const [error, setError] = useState('');
  const [calculatedPriority, setCalculatedPriority] = useState<number | null>(null);

  // Calculate priority score in real-time
  useEffect(() => {
    if (deadline) {
      const daysUntilDeadline = Math.floor((new Date(deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
      const score = 100 - (daysUntilDeadline * 5) - (estimatedDuration * 3);
      const clampedScore = Math.max(1, Math.min(100, score));
      setCalculatedPriority(clampedScore);
    } else {
      setCalculatedPriority(null);
    }
  }, [deadline, estimatedDuration]);

  // Update estimated duration when t-shirt size changes
  const handleTshirtSizeChange = (size: Task['tshirt_size']) => {
    setTshirtSize(size);
    
    // AI-suggested duration based on t-shirt size
    const durationMap: Record<string, number> = {
      'XS': 2,
      'S': 4,
      'M': 8,
      'L': 16,
      'XL': 24,
    };
    
    if (size) {
      setEstimatedDuration(durationMap[size]);
    }
  };

  const handleSubmit = () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    if (!description.trim()) {
      setError('Description cannot be empty');
      return;
    }
    if (!deadline) {
      setError('Deadline is required');
      return;
    }

    onCreateTask({
      title,
      description,
      deadline,
      status,
      estimated_duration: estimatedDuration,
      tshirt_size: tshirtSize,
    });

    // Reset form
    setTitle('');
    setDescription('');
    setDeadline('');
    setStatus('pending');
    setEstimatedDuration(4);
    setTshirtSize('M');
    setError('');
    setCalculatedPriority(null);
    onOpenChange(false);
  };

  const handleCancel = () => {
    setTitle('');
    setDescription('');
    setDeadline('');
    setStatus('pending');
    setEstimatedDuration(4);
    setTshirtSize('M');
    setError('');
    setCalculatedPriority(null);
    onOpenChange(false);
  };

  const getPriorityLevel = (score: number): { label: string; color: string; variant: 'default' | 'secondary' | 'destructive' } => {
    if (score >= 70) return { label: 'High Priority', color: 'text-red-600', variant: 'destructive' };
    if (score >= 40) return { label: 'Medium Priority', color: 'text-yellow-600', variant: 'default' };
    return { label: 'Low Priority', color: 'text-green-600', variant: 'secondary' };
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[550px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-blue-500" />
            Create New Task
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label>Title</Label>
            <Input
              placeholder="Enter task title..."
              value={title}
              onChange={(e) => {
                setTitle(e.target.value);
                setError('');
              }}
            />
          </div>

          <div className="space-y-2">
            <Label>Description</Label>
            <Textarea
              placeholder="Enter task description..."
              value={description}
              onChange={(e) => {
                setDescription(e.target.value);
                setError('');
              }}
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Status</Label>
              <Select value={status} onValueChange={(value: Task['status']) => setStatus(value)}>
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
                value={deadline}
                onChange={(e) => {
                  setDeadline(e.target.value);
                  setError('');
                }}
              />
            </div>
          </div>

          {/* AI T-Shirt Size Selector */}
          <div className="space-y-2 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-blue-600" />
              <Label className="text-blue-900">AI T-Shirt Size (Task Complexity)</Label>
            </div>
            <div className="flex gap-2">
              {(['XS', 'S', 'M', 'L', 'XL'] as const).map((size) => (
                <Button
                  key={size}
                  type="button"
                  variant={tshirtSize === size ? 'default' : 'outline'}
                  className="flex-1"
                  onClick={() => handleTshirtSizeChange(size)}
                >
                  {size}
                </Button>
              ))}
            </div>
            <p className="text-xs text-blue-700 mt-2">
              AI will auto-adjust estimated duration based on size
            </p>
          </div>

          {/* Estimated Duration with Slider */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Estimated Duration</Label>
              <span className="text-sm text-slate-600">{estimatedDuration} hours</span>
            </div>
            <Slider
              value={[estimatedDuration]}
              onValueChange={([value]) => setEstimatedDuration(value)}
              min={1}
              max={24}
              step={1}
              className="py-4"
            />
            <div className="flex justify-between text-xs text-slate-500">
              <span>1 hour</span>
              <span>24 hours</span>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={handleCancel}>
            Cancel
          </Button>
          <Button onClick={handleSubmit}>
            <Sparkles className="w-4 h-4 mr-2" />
            Create Task
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

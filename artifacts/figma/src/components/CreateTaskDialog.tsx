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

          {/* AI Priority Score Preview */}
          {calculatedPriority !== null && (
            <div className="space-y-3 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-blue-600" />
                  <Label className="text-blue-900">AI-Generated Priority Score</Label>
                </div>
                <Badge variant="outline" className="bg-white text-xs">
                  Auto-calculated
                </Badge>
              </div>
              
              <div className="flex items-center gap-3">
                <div className="flex-1">
                  <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all ${
                        calculatedPriority >= 70
                          ? 'bg-red-500'
                          : calculatedPriority >= 40
                          ? 'bg-yellow-500'
                          : 'bg-green-500'
                      }`}
                      style={{ width: `${calculatedPriority}%` }}
                    />
                  </div>
                </div>
                <Badge variant={getPriorityLevel(calculatedPriority).variant} className="min-w-[80px] justify-center">
                  {calculatedPriority}
                </Badge>
              </div>
              
              <div className="flex items-center justify-between">
                <p className="text-sm text-slate-700">
                  {getPriorityLevel(calculatedPriority).label}
                </p>
                <p className="text-xs text-slate-500 italic">
                  This score will be saved
                </p>
              </div>
              
              {calculatedPriority >= 70 && (
                <Alert className="bg-red-50 border-red-200">
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <AlertDescription className="text-red-800 text-sm">
                    This task will be high priority. Consider addressing it soon.
                  </AlertDescription>
                </Alert>
              )}
              
              <div className="pt-2 border-t border-blue-200">
                <p className="text-xs text-blue-700">
                  <strong>AI Formula:</strong> Score = 100 - (days_until_deadline × 5) - (estimated_duration × 3)
                </p>
              </div>
            </div>
          )}

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

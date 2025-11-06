import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { TaskList } from './components/TaskList';
import { TaskDetailsPanel } from './components/TaskDetailsPanel';
import { AIToolsPanel } from './components/AIToolsPanel';
import { toast } from 'sonner';
import { Toaster } from './components/ui/sonner';

export interface Task {
  id: number;
  title: string;
  description: string;
  deadline: string;
  status: 'pending' | 'in-progress' | 'completed';
  estimated_duration: number;
  priority_score: number;
  tshirt_size?: 'XS' | 'S' | 'M' | 'L' | 'XL';
}

export default function App() {
  const [selectedView, setSelectedView] = useState<'dashboard' | 'tasks' | 'ai-tools' | 'settings'>('tasks');
  const [targetDate, setTargetDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const handleCreateTask = (task: Omit<Task, 'id' | 'priority_score'>) => {
    const aiGeneratedScore = calculatePriorityScore(task.deadline, task.estimated_duration);
    const newTask: Task = {
      ...task,
      id: tasks.length + 1,
      priority_score: aiGeneratedScore
    };
    setTasks([...tasks, newTask]);
    
    // Show AI confirmation toast
    const priorityLevel = aiGeneratedScore >= 70 ? 'High' : aiGeneratedScore >= 40 ? 'Medium' : 'Low';
    toast.success('Task created successfully!', {
      description: `AI Priority Score: ${aiGeneratedScore} (${priorityLevel} Priority)`,
    });
  };

  const handleUpdateTask = (updatedTask: Task) => {
    const taskWithScore = {
      ...updatedTask,
      priority_score: calculatePriorityScore(updatedTask.deadline, updatedTask.estimated_duration)
    };
    setTasks(tasks.map(t => t.id === taskWithScore.id ? taskWithScore : t));
    setSelectedTask(taskWithScore);
  };

  const handleDeleteTask = (id: number) => {
    setTasks(tasks.filter(t => t.id !== id));
    if (selectedTask?.id === id) {
      setSelectedTask(null);
    }
  };

  const calculatePriorityScore = (deadline: string, estimatedDuration: number): number => {
    const daysUntilDeadline = Math.floor((new Date(deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
    const score = 100 - (daysUntilDeadline * 5) - (estimatedDuration * 3);
    return Math.max(1, Math.min(100, score));
  };

  const filterTasksByDateRange = (tasks: Task[], targetDate: string, dayRange: number = 7): Task[] => {
    const target = new Date(targetDate);
    target.setHours(0, 0, 0, 0);
    
    return tasks.filter(task => {
      const taskDeadline = new Date(task.deadline);
      taskDeadline.setHours(0, 0, 0, 0);
      
      const daysDifference = Math.floor((taskDeadline.getTime() - target.getTime()) / (1000 * 60 * 60 * 24));
      return daysDifference >= -dayRange && daysDifference <= dayRange;
    });
  };

  // Filter tasks within 7 days of the target date
  const filteredTasks = filterTasksByDateRange(tasks, targetDate);

  return (
    <div className="flex h-screen bg-slate-100">
      <Toaster />
      <Sidebar selectedView={selectedView} onSelectView={setSelectedView} />
      
      <div className="flex flex-1 gap-6 p-6 overflow-hidden">
        {selectedView === 'tasks' && (
          <>
            <div className="flex flex-col gap-4">
              {/* Date Range Selector */}
              <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm w-[400px]">
                <div className="flex items-center gap-2">
                  <label htmlFor="target-date" className="text-sm text-slate-600 font-medium">Filter by Date Range:</label>
                  <input
                    id="target-date"
                    type="date"
                    value={targetDate}
                    onChange={(e) => setTargetDate(e.target.value)}
                    className="text-sm border border-slate-300 rounded px-2 py-1"
                  />
                  <span className="text-xs text-slate-500">±7 days</span>
                </div>
              </div>
              <TaskList 
                tasks={filteredTasks} 
                selectedTask={selectedTask}
                onSelectTask={setSelectedTask}
                onCreateTask={handleCreateTask}
                targetDate={targetDate}
                totalTasks={tasks.length}
              />
            </div>
            <TaskDetailsPanel 
              task={selectedTask}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
            />
          </>
        )}
        
        {selectedView === 'ai-tools' && (
          <>
            <div className="w-80 flex-shrink-0 flex flex-col gap-4">
              {/* Date Range Selector for AI Tools */}
              <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm">
                <div className="flex flex-col gap-2">
                  <label htmlFor="target-date-ai" className="text-xs text-slate-600 font-medium">Date Range Filter:</label>
                  <div className="flex items-center gap-2">
                    <input
                      id="target-date-ai"
                      type="date"
                      value={targetDate}
                      onChange={(e) => setTargetDate(e.target.value)}
                      className="text-sm border border-slate-300 rounded px-2 py-1 flex-1"
                    />
                    <span className="text-xs text-slate-500">±7d</span>
                  </div>
                </div>
              </div>
              <TaskList 
                tasks={filteredTasks} 
                selectedTask={selectedTask}
                onSelectTask={setSelectedTask}
                onCreateTask={handleCreateTask}
                targetDate={targetDate}
                totalTasks={tasks.length}
                compact
              />
            </div>
            <AIToolsPanel 
              selectedTask={selectedTask}
              allTasks={filteredTasks}
              targetDate={targetDate}
            />
          </>
        )}

        {selectedView === 'dashboard' && (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-slate-500">Dashboard View</h2>
              <p className="text-slate-400 mt-2">Coming soon</p>
            </div>
          </div>
        )}

        {selectedView === 'settings' && (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-slate-500">Settings View</h2>
              <p className="text-slate-400 mt-2">Coming soon</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

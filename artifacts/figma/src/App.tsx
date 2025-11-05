import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { TaskList } from './components/TaskList';
import { TaskDetailsPanel } from './components/TaskDetailsPanel';
import { AIToolsPanel } from './components/AIToolsPanel';
import { toast } from 'sonner@2.0.3';
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
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: 1,
      title: "Project Alpha Kickoff",
      description: "Initial planning and team alignment",
      deadline: "2024-03-15",
      status: "in-progress",
      estimated_duration: 4,
      priority_score: 92
    },
    {
      id: 2,
      title: "Develop Feature X",
      description: "Implement core functionality",
      deadline: "2024-03-20",
      status: "pending",
      estimated_duration: 8,
      priority_score: 78
    },
    {
      id: 3,
      title: "Research Market Trends",
      description: "Analyze competitor strategies",
      deadline: "2024-03-25",
      status: "pending",
      estimated_duration: 3,
      priority_score: 65
    },
    {
      id: 4,
      title: "Submit project report",
      description: "Send final report to manager",
      deadline: "2025-11-06",
      status: "pending",
      estimated_duration: 4,
      priority_score: 85
    }
  ]);
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

  return (
    <div className="flex h-screen bg-slate-100">
      <Toaster />
      <Sidebar selectedView={selectedView} onSelectView={setSelectedView} />
      
      <div className="flex flex-1 gap-6 p-6 overflow-hidden">
        {selectedView === 'tasks' && (
          <>
            <TaskList 
              tasks={tasks} 
              selectedTask={selectedTask}
              onSelectTask={setSelectedTask}
              onCreateTask={handleCreateTask}
            />
            <TaskDetailsPanel 
              task={selectedTask}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
            />
          </>
        )}
        
        {selectedView === 'ai-tools' && (
          <>
            <div className="w-80 flex-shrink-0">
              <TaskList 
                tasks={tasks} 
                selectedTask={selectedTask}
                onSelectTask={setSelectedTask}
                onCreateTask={handleCreateTask}
                compact
              />
            </div>
            <AIToolsPanel 
              selectedTask={selectedTask}
              allTasks={tasks}
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

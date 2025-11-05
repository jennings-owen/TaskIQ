import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import { TaskList } from './components/TaskList';
import { TaskDetailsPanel } from './components/TaskDetailsPanel';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';

function App() {
  const [selectedView, setSelectedView] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Task management state
  const [tasks, setTasks] = useState([
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
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACK_END_URL}/status`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStatus(data);
      } catch (err) {
        setError("Failed to fetch status from the backend.");
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, []);

  const handleMenuToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // Task management functions
  const calculatePriorityScore = (deadline, estimatedDuration) => {
    const daysUntilDeadline = Math.floor((new Date(deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
    const score = 100 - (daysUntilDeadline * 5) - (estimatedDuration * 3);
    return Math.max(1, Math.min(100, score));
  };

  const handleCreateTask = (task) => {
    const aiGeneratedScore = calculatePriorityScore(task.deadline, task.estimated_duration);
    const newTask = {
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

  const handleUpdateTask = (updatedTask) => {
    const taskWithScore = {
      ...updatedTask,
      priority_score: calculatePriorityScore(updatedTask.deadline, updatedTask.estimated_duration)
    };
    setTasks(tasks.map(t => t.id === taskWithScore.id ? taskWithScore : t));
    setSelectedTask(taskWithScore);
  };

  const handleDeleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id));
    if (selectedTask?.id === id) {
      setSelectedTask(null);
    }
  };

  const renderMainContent = () => {
    switch (selectedView) {
      case 'dashboard':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">Dashboard</h2>
              <p className="text-gray-500 mb-8">Welcome to Agile TaskIQ Dashboard</p>
              
              {/* Status information */}
              <div className="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
                <h3 className="text-lg font-medium text-gray-800 mb-4">System Status</h3>
                {loading && <div className="text-blue-600">Loading status...</div>}
                {error && <div className="text-red-600">Status Error: {error}</div>}
                {status && (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">API Status:</span>
                      <span className={status.status === 'healthy' ? 'text-green-600 font-medium' : 'text-red-600 font-medium'}>
                        {status.status}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Message:</span>
                      <span className="text-gray-800">{status.message}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Version:</span>
                      <span className="text-gray-800">{status.version}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      case 'tasks':
        return (
          <div className="flex flex-col lg:flex-row gap-6 h-full overflow-hidden">
            <div className="lg:w-[400px] w-full">
              <TaskList 
                tasks={tasks} 
                selectedTask={selectedTask}
                onSelectTask={setSelectedTask}
                onCreateTask={handleCreateTask}
              />
            </div>
            <div className="flex-1">
              <TaskDetailsPanel 
                task={selectedTask}
                onUpdateTask={handleUpdateTask}
                onDeleteTask={handleDeleteTask}
              />
            </div>
          </div>
        );
      case 'ai-tools':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">AI Tools</h2>
              <p className="text-gray-500">AI-powered task management tools coming soon</p>
            </div>
          </div>
        );
      case 'settings':
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600 mb-4">Settings</h2>
              <p className="text-gray-500">Application settings coming soon</p>
            </div>
          </div>
        );
      default:
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-600">Welcome</h2>
              <p className="text-gray-500 mt-2">Select a view from the sidebar</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col lg:flex-row">
      <Toaster />
      {/* Top Bar - Mobile only */}
      <TopBar onMenuToggle={handleMenuToggle} />
      
      {/* Sidebar */}
      <Sidebar 
        selectedView={selectedView}
        onSelectView={setSelectedView}
        isOpen={isSidebarOpen}
        onClose={handleSidebarClose}
      />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <main className="flex-1 p-3 lg:p-6 overflow-auto">
          <div className="container">
            {renderMainContent()}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;

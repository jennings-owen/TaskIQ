import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import { TaskList } from './components/TaskList';
import { TaskDetailsPanel } from './components/TaskDetailsPanel';
import UserProfileSettings from './components/UserProfileSettings';
import SystemStatus from './components/SystemStatus';
import DailyPlan from './components/DailyPlan';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';

function MainApp() {
  const { user, logout, apiCall } = useAuth();
  const [selectedView, setSelectedView] = useState('tasks');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Task management state
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [tasksError, setTasksError] = useState(null);

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

    const fetchTasks = async () => {
      try {
        setTasksLoading(true);
        const response = await apiCall('/tasks');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setTasks(data);
      } catch (err) {
        setTasksError("Failed to fetch tasks from the backend.");
        console.error("Error fetching tasks:", err);
      } finally {
        setTasksLoading(false);
      }
    };

    fetchStatus();
    fetchTasks();
  }, [apiCall]);

  const handleMenuToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  // Task management functions
  const handleCreateTask = async (task) => {
    try {
      const response = await apiCall('/tasks', {
        method: 'POST',
        body: JSON.stringify(task),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.detail || errorData?.message || `HTTP ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
      }

      const newTask = await response.json();
      setTasks([...tasks, newTask]);
      
      toast.success('Task created successfully!');
    } catch (err) {
      console.error("Error creating task:", err);
      const isNetworkError = err.name === 'TypeError' || err.message.includes('fetch');
      const errorMessage = isNetworkError 
        ? 'Unable to connect to the server. Please check your connection and try again.'
        : err.message || 'An unexpected error occurred while creating the task.';
      
      toast.error('Failed to create task', {
        description: errorMessage,
      });
    }
  };

  const handleUpdateTask = async (updatedTask) => {
    try {
      const response = await apiCall(`/tasks/${updatedTask.id}`, {
        method: 'PUT',
        body: JSON.stringify(updatedTask),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.detail || errorData?.message || `HTTP ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
      }

      const taskFromServer = await response.json();
      setTasks(tasks.map(t => t.id === taskFromServer.id ? taskFromServer : t));
      setSelectedTask(taskFromServer);
      
      toast.success('Task updated successfully!');
    } catch (err) {
      console.error("Error updating task:", err);
      const isNetworkError = err.name === 'TypeError' || err.message.includes('fetch');
      const errorMessage = isNetworkError 
        ? 'Unable to connect to the server. Please check your connection and try again.'
        : err.message || 'An unexpected error occurred while updating the task.';
      
      toast.error('Failed to update task', {
        description: errorMessage,
      });
    }
  };

  const handleDeleteTask = async (id) => {
    try {
      const response = await apiCall(`/tasks/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.detail || errorData?.message || `HTTP ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
      }

      setTasks(tasks.filter(t => t.id !== id));
      if (selectedTask?.id === id) {
        setSelectedTask(null);
      }
      
      toast.success('Task deleted successfully!');
    } catch (err) {
      console.error("Error deleting task:", err);
      const isNetworkError = err.name === 'TypeError' || err.message.includes('fetch');
      const errorMessage = isNetworkError 
        ? 'Unable to connect to the server. Please check your connection and try again.'
        : err.message || 'An unexpected error occurred while deleting the task.';
      
      toast.error('Failed to delete task', {
        description: errorMessage,
      });
    }
  };

  const renderMainContent = () => {
    switch (selectedView) {
      case 'tasks':
        return (
          <div className="flex flex-col lg:flex-row gap-6 h-full overflow-hidden">
            <div className="lg:w-[400px] w-full lg:overflow-auto">
              {tasksLoading ? (
                <div className="flex items-center justify-center h-64">
                  <div className="text-blue-600">Loading tasks...</div>
                </div>
              ) : tasksError ? (
                <div className="flex items-center justify-center h-64">
                  <div className="text-red-600">Error: {tasksError}</div>
                </div>
              ) : (
                <TaskList 
                  tasks={tasks} 
                  selectedTask={selectedTask}
                  onSelectTask={setSelectedTask}
                  onCreateTask={handleCreateTask}
                />
              )}
            </div>
            <div className="flex-1 lg:sticky lg:top-0 lg:self-start lg:h-[calc(100vh-8rem)]">
              <TaskDetailsPanel 
                task={selectedTask}
                allTasks={tasks}
                onUpdateTask={handleUpdateTask}
                onDeleteTask={handleDeleteTask}
                onSelectTask={setSelectedTask}
              />
            </div>
          </div>
        );
      case 'ai-tools':
        return <DailyPlan />;
      case 'settings':
        return (
          <div className="space-y-6">
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Settings</h2>
              <p className="text-gray-600">Manage your account settings and view system status</p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <UserProfileSettings />
              </div>
              <div>
                <SystemStatus 
                  status={status}
                  loading={loading}
                  error={error}
                  user={user}
                />
              </div>
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
        user={user}
        onLogout={logout}
      />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <main className="flex-1 p-3 lg:p-6 lg:overflow-visible overflow-auto">
          <div className="container h-full">
            {renderMainContent()}
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    </AuthProvider>
  );
}

export default App;

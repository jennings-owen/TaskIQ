import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'sonner';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const DailyPlan = () => {
  const { apiCall } = useAuth();
  const [planData, setPlanData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [targetDate, setTargetDate] = useState(new Date().toISOString().split('T')[0]);
  const [previewMode, setPreviewMode] = useState(false);
  const [previewData, setPreviewData] = useState(null);

  const generateDailyPlan = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiCall('/daily-plan', {
        method: 'POST',
        body: JSON.stringify({
          target_date: targetDate
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setPlanData(data);
      toast.success('Daily plan generated successfully!');
    } catch (err) {
      console.error("Error generating daily plan:", err);
      const errorMessage = err.message || 'An unexpected error occurred while generating the daily plan.';
      setError(errorMessage);
      toast.error('Failed to generate daily plan', {
        description: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  const previewPlanData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiCall(`/daily-plan/preview?target_date=${targetDate}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setPreviewData(data);
      setPreviewMode(true);
      toast.success('Daily plan data preview loaded!');
    } catch (err) {
      console.error("Error previewing daily plan data:", err);
      const errorMessage = err.message || 'An unexpected error occurred while previewing the daily plan data.';
      setError(errorMessage);
      toast.error('Failed to preview daily plan data', {
        description: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Daily Plan Generator</h2>
        <p className="text-gray-600 mb-6">
          Generate AI-powered daily plans based on your tasks and dependencies. 
          The system analyzes your workload and creates optimized schedules.
        </p>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 items-end">
          <div className="flex-1">
            <label htmlFor="target-date" className="block text-sm font-medium text-gray-700 mb-2">
              Target Date
            </label>
            <input
              id="target-date"
              type="date"
              value={targetDate}
              onChange={(e) => setTargetDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={previewPlanData}
              disabled={loading}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Loading...' : 'Preview Data'}
            </button>
            
            <button
              onClick={generateDailyPlan}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Generating...' : 'Generate Plan'}
            </button>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="text-red-800">
              <h3 className="text-sm font-medium">Error</h3>
              <p className="mt-1 text-sm">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Preview Mode */}
      {previewMode && previewData && (
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Data Preview</h3>
              <button
                onClick={() => setPreviewMode(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕ Close
              </button>
            </div>
            <p className="text-sm text-gray-600 mt-1">
              Preview of data that would be used for plan generation
            </p>
          </div>
          
          <div className="p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{previewData.tasks_count}</div>
                <div className="text-sm text-blue-800">Total Tasks</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{previewData.dependencies_count}</div>
                <div className="text-sm text-green-800">Dependencies</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{formatDate(previewData.target_date)}</div>
                <div className="text-sm text-purple-800">Target Date</div>
              </div>
            </div>

            {previewData.tasks && previewData.tasks.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Tasks to be planned:</h4>
                <div className="max-h-60 overflow-y-auto space-y-2">
                  {previewData.tasks.map((task, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded border text-sm">
                      <div className="font-medium">{task.title}</div>
                      <div className="text-gray-600">Priority: {task.priority} | T-shirt: {task.tshirt_size}</div>
                      {task.description && (
                        <div className="text-gray-500 mt-1">{task.description}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Generated Plan Display */}
      {planData && !previewMode && (
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
              Daily Plan for {formatDate(planData.target_date)}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Generated on {new Date(planData.generated_at).toLocaleString()}
            </p>
          </div>
          
          <div className="p-6">
            <div className="prose prose-sm max-w-none max-h-96 overflow-y-auto">
              <div className="markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                  h1: ({node, ...props}) => <h1 className="text-2xl font-bold mb-4 text-gray-900" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-xl font-semibold mb-3 mt-6 text-gray-800" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-lg font-medium mb-2 mt-4 text-gray-700" {...props} />,
                  h4: ({node, ...props}) => <h4 className="text-base font-medium mb-2 mt-3 text-gray-700" {...props} />,
                  p: ({node, ...props}) => <p className="mb-3 text-gray-600 leading-relaxed" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1" {...props} />,
                  li: ({node, ...props}) => <li className="text-gray-600" {...props} />,
                  strong: ({node, ...props}) => <strong className="font-semibold text-gray-800" {...props} />,
                  em: ({node, ...props}) => <em className="italic text-gray-700" {...props} />,
                  code: ({node, ...props}) => <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono" {...props} />,
                  pre: ({node, ...props}) => <pre className="bg-gray-100 p-3 rounded overflow-x-auto mb-3" {...props} />,
                  blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-blue-200 pl-4 italic text-gray-600 mb-3" {...props} />,
                  table: ({node, ...props}) => <table className="min-w-full border-collapse border border-gray-200 mb-3" {...props} />,
                  th: ({node, ...props}) => <th className="border border-gray-200 bg-gray-50 px-3 py-2 text-left font-medium" {...props} />,
                  td: ({node, ...props}) => <td className="border border-gray-200 px-3 py-2" {...props} />,
                }}
              >
                {planData.plan_content}
              </ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-lg shadow-sm p-12">
          <div className="flex flex-col items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600">
              {previewMode ? 'Loading preview data...' : 'Generating your daily plan...'}
            </p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!planData && !loading && !error && !previewMode && (
        <div className="bg-white rounded-lg shadow-sm p-12">
          <div className="text-center">
            <div className="text-gray-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Plan Generated Yet</h3>
            <p className="text-gray-600 mb-4">
              Select a target date and click "Generate Plan" to create your AI-powered daily schedule.
            </p>
            <button
              onClick={generateDailyPlan}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Generate Your First Plan
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DailyPlan;
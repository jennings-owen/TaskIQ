import { Sparkles, TrendingUp, Clock, AlertTriangle, CheckCircle2, Target, Zap } from 'lucide-react';
import { Task } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Separator } from './ui/separator';
import { Alert, AlertDescription } from './ui/alert';

interface AIToolsPanelProps {
  selectedTask: Task | null;
  allTasks: Task[];
}

export function AIToolsPanel({ selectedTask, allTasks }: AIToolsPanelProps) {
  if (!selectedTask) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-md space-y-4">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-4">
            <Sparkles className="w-10 h-10 text-blue-600" />
          </div>
          <h2 className="text-slate-900">AI-Powered Task Analysis</h2>
          <p className="text-slate-500 mb-4">
            Select a task from the list on the left to view:
          </p>
          <div className="text-left space-y-2 max-w-sm mx-auto">
            <div className="flex items-start gap-2">
              <span className="text-blue-600">🎯</span>
              <p className="text-sm text-slate-600">Agile T-shirt size recommendations with confidence scores</p>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-600">📊</span>
              <p className="text-sm text-slate-600">AI-calculated priority scores with urgency analysis</p>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-600">💡</span>
              <p className="text-sm text-slate-600">Strategic action items and productivity insights</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const calculateDaysUntilDeadline = (deadline: string): number => {
    return Math.floor((new Date(deadline).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
  };

  const getTshirtSizeRecommendation = (task: Task): {
    recommended: 'XS' | 'S' | 'M' | 'L' | 'XL';
    reasoning: string;
    confidence: number;
  } => {
    const duration = task.estimated_duration;
    
    // AI logic for t-shirt size recommendation
    let recommended: 'XS' | 'S' | 'M' | 'L' | 'XL';
    let reasoning: string;
    let confidence: number;

    if (duration <= 2) {
      recommended = 'XS';
      reasoning = 'Very quick task requiring minimal time and effort. Can be completed in a single sitting.';
      confidence = 95;
    } else if (duration <= 4) {
      recommended = 'S';
      reasoning = 'Small task with clear scope. Should be straightforward to complete within a few hours.';
      confidence = 90;
    } else if (duration <= 8) {
      recommended = 'M';
      reasoning = 'Medium complexity task requiring sustained focus. May span across multiple work sessions.';
      confidence = 85;
    } else if (duration <= 16) {
      recommended = 'L';
      reasoning = 'Large task with significant scope. Requires careful planning and may involve multiple dependencies.';
      confidence = 80;
    } else {
      recommended = 'XL';
      reasoning = 'Extra large task with substantial complexity. Consider breaking this down into smaller subtasks.';
      confidence = 75;
    }

    return { recommended, reasoning, confidence };
  };

  const getPriorityInsights = (task: Task): {
    level: 'Critical' | 'High' | 'Medium' | 'Low';
    urgencyScore: number;
    complexityScore: number;
    recommendations: string[];
  } => {
    const score = task.priority_score;
    const daysUntil = calculateDaysUntilDeadline(task.deadline);
    
    let level: 'Critical' | 'High' | 'Medium' | 'Low';
    const recommendations: string[] = [];

    if (score >= 85) {
      level = 'Critical';
      recommendations.push('⚡ Immediate action required');
      recommendations.push('📅 Very close to deadline');
      recommendations.push('👥 Consider escalating to team lead');
    } else if (score >= 70) {
      level = 'High';
      recommendations.push('🎯 Schedule this week');
      recommendations.push('⏰ Block dedicated time on calendar');
      recommendations.push('🔔 Set up progress reminders');
    } else if (score >= 40) {
      level = 'Medium';
      recommendations.push('📋 Add to this sprint');
      recommendations.push('🔄 Review regularly for priority changes');
      recommendations.push('📊 Monitor for dependency updates');
    } else {
      level = 'Low';
      recommendations.push('📅 Plan for next sprint');
      recommendations.push('💡 Consider as backlog item');
      recommendations.push('🔍 Re-evaluate priority monthly');
    }

    // Calculate urgency (based on deadline)
    const urgencyScore = Math.max(0, Math.min(100, 100 - daysUntil * 3));
    
    // Calculate complexity (based on duration)
    const complexityScore = Math.min(100, (task.estimated_duration / 24) * 100);

    return { level, urgencyScore, complexityScore, recommendations };
  };

  const getAIStrategies = (task: Task): string[] => {
    const strategies: string[] = [];
    const daysUntil = calculateDaysUntilDeadline(task.deadline);
    
    if (task.estimated_duration > 12) {
      strategies.push('🔨 Break down into smaller, manageable subtasks');
    }
    
    if (daysUntil < 3 && task.status === 'pending') {
      strategies.push('🚀 Start immediately - deadline approaching');
    }
    
    if (task.status === 'in-progress') {
      strategies.push('✅ Focus on completion to maintain momentum');
    }
    
    if (task.estimated_duration < 2 && task.status === 'pending') {
      strategies.push('⚡ Quick win - prioritize for immediate completion');
    }
    
    if (daysUntil > 14) {
      strategies.push('📅 Use extra time for thorough planning and research');
    }

    return strategies;
  };

  const tshirtRec = getTshirtSizeRecommendation(selectedTask);
  const priorityInsights = getPriorityInsights(selectedTask);
  const strategies = getAIStrategies(selectedTask);
  const daysUntil = calculateDaysUntilDeadline(selectedTask.deadline);

  return (
    <div className="flex-1 overflow-auto p-6 space-y-6 bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-6 h-6" />
          <h1>AI Task Analysis</h1>
        </div>
        <p className="text-blue-100">
          Intelligent insights powered by Agile TaskIQ AI
        </p>
      </div>

      {/* Selected Task Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle>{selectedTask.title}</CardTitle>
              <CardDescription className="mt-2">{selectedTask.description}</CardDescription>
            </div>
            <Badge 
              variant={selectedTask.status === 'completed' ? 'secondary' : selectedTask.status === 'in-progress' ? 'default' : 'outline'}
            >
              {selectedTask.status}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="space-y-1">
              <p className="text-xs text-slate-500">Deadline</p>
              <p className="text-slate-900">
                {new Date(selectedTask.deadline).toLocaleDateString()}
              </p>
              <p className="text-xs text-slate-600">
                {daysUntil > 0 ? `${daysUntil} days away` : daysUntil === 0 ? 'Today!' : `${Math.abs(daysUntil)} days overdue`}
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-slate-500">Duration</p>
              <p className="text-slate-900">{selectedTask.estimated_duration} hours</p>
              <p className="text-xs text-slate-600">
                {(selectedTask.estimated_duration / 8).toFixed(1)} days
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-slate-500">Current Size</p>
              <Badge variant="secondary" className="text-base px-3 py-1">
                {selectedTask.tshirt_size || 'Not set'}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI Priority Score Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            AI Priority Score Analysis
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600">Priority Score</span>
                <span className="text-slate-900">{selectedTask.priority_score}/100</span>
              </div>
              <Progress value={selectedTask.priority_score} className="h-3" />
            </div>
            <Badge 
              variant={
                priorityInsights.level === 'Critical' || priorityInsights.level === 'High' 
                  ? 'destructive' 
                  : priorityInsights.level === 'Medium' 
                  ? 'default' 
                  : 'secondary'
              }
              className="text-base px-4 py-2"
            >
              {priorityInsights.level}
            </Badge>
          </div>

          <Separator />

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Clock className="w-4 h-4" />
                Urgency Factor
              </div>
              <Progress value={priorityInsights.urgencyScore} className="h-2" />
              <p className="text-xs text-slate-500">{priorityInsights.urgencyScore.toFixed(0)}% - Based on deadline proximity</p>
            </div>
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Target className="w-4 h-4" />
                Complexity Factor
              </div>
              <Progress value={priorityInsights.complexityScore} className="h-2" />
              <p className="text-xs text-slate-500">{priorityInsights.complexityScore.toFixed(0)}% - Based on estimated duration</p>
            </div>
          </div>

          <div className="bg-slate-50 rounded-lg p-4 space-y-2">
            <h4 className="text-sm text-slate-700 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-600" />
              AI Recommendations
            </h4>
            {priorityInsights.recommendations.map((rec, idx) => (
              <p key={idx} className="text-sm text-slate-600">
                {rec}
              </p>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* T-Shirt Size Recommendation */}
      <Card className="border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-600" />
            Agile T-Shirt Size Recommendation
          </CardTitle>
          <CardDescription>
            AI-powered complexity estimation for Agile planning
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-4">
                <div className="inline-flex items-center justify-center w-24 h-24 bg-white rounded-full border-4 border-blue-500 shadow-lg">
                  <span className="text-4xl text-blue-600">{tshirtRec.recommended}</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-slate-900 mb-1">Recommended Size: {tshirtRec.recommended}</h3>
                  <p className="text-sm text-slate-600">{tshirtRec.reasoning}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-600">AI Confidence Level</span>
              <span className="text-slate-900">{tshirtRec.confidence}%</span>
            </div>
            <Progress value={tshirtRec.confidence} className="h-2" />
          </div>

          {selectedTask.tshirt_size && selectedTask.tshirt_size !== tshirtRec.recommended && (
            <Alert className="bg-yellow-50 border-yellow-200">
              <AlertTriangle className="h-4 w-4 text-yellow-600" />
              <AlertDescription className="text-yellow-800 text-sm">
                Current size ({selectedTask.tshirt_size}) differs from AI recommendation ({tshirtRec.recommended}). 
                Consider updating for better sprint planning.
              </AlertDescription>
            </Alert>
          )}

          {selectedTask.tshirt_size === tshirtRec.recommended && (
            <Alert className="bg-green-50 border-green-200">
              <CheckCircle2 className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800 text-sm">
                Current size matches AI recommendation. Task is properly sized for Agile planning.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* AI Strategic Recommendations */}
      {strategies.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-600" />
              Strategic Action Items
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {strategies.map((strategy, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-xs text-blue-700">{idx + 1}</span>
                  </div>
                  <p className="text-sm text-slate-700 flex-1">{strategy}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Task Context */}
      <Card className="bg-slate-50">
        <CardHeader>
          <CardTitle className="text-base">Context & Insights</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-slate-600 space-y-3">
          <div className="flex items-start gap-2">
            <span className="text-blue-600">📊</span>
            <div>
              <p className="text-slate-700">Workload Analysis</p>
              <p className="text-xs text-slate-500 mt-1">
                You have {allTasks.filter(t => t.status !== 'completed').length} active tasks. 
                This task ranks #{allTasks.filter(t => t.status !== 'completed').sort((a, b) => b.priority_score - a.priority_score).findIndex(t => t.id === selectedTask.id) + 1} in priority.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-blue-600">🎯</span>
            <div>
              <p className="text-slate-700">Agile Best Practice</p>
              <p className="text-xs text-slate-500 mt-1">
                T-shirt sizing helps teams quickly estimate relative complexity without detailed time tracking. 
                Use these sizes in sprint planning and backlog refinement sessions.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

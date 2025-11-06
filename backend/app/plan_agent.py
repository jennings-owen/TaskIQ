"""
Daily Plan Generation Agent using CrewAI

This module contains a CrewAI agent system that takes user tasks and their dependencies
as input and generates a comprehensive daily plan formatted as a markdown file.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.models import Task as TaskModel, TaskDependency, TaskPriorityScore, TaskTShirtScore
from app.database import get_db

import dotenv

root_dir = Path(__file__).parent.parent.parent
dotenv.load_dotenv(dotenv_path=root_dir / ".env")


class DailyPlanGenerator:
    """CrewAI-based daily plan generator for task scheduling and organization."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the daily plan generator with OpenAI configuration."""
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            api_key=self.openai_api_key,
            temperature=0.3
        )
        
        # Load template
        self.template_path = Path(__file__).parent.parent / "templates" / "daily_plan_template.md"
        self.template_content = self._load_template()
        
    def _load_template(self) -> str:
        """Load the daily plan template from file."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found at {self.template_path}")
    
    @tool
    @staticmethod
    def format_task_dependencies(dependencies_data: str) -> str:
        """
        Format task dependencies into a readable structure.
        
        Args:
            dependencies_data: JSON string containing task dependencies
            
        Returns:
            Formatted dependency information
        """
        try:
            dependencies = json.loads(dependencies_data)
            formatted = []
            
            for dep in dependencies:
                task_title = dep.get('task_title', 'Unknown Task')
                depends_on = dep.get('depends_on_title', 'Unknown Dependency')
                formatted.append(f"- **{task_title}** depends on **{depends_on}**")
            
            return "\n".join(formatted) if formatted else "No task dependencies found."
        except (json.JSONDecodeError, KeyError):
            return "Error parsing dependency data."
    

    
    def _create_planning_agents(self) -> tuple:
        """Create the specialized CrewAI agents for daily planning."""
        
        # Task Analysis Agent
        task_analyzer = Agent(
            role="Task Analysis Specialist",
            goal="Analyze and categorize user tasks based on priority, duration, and dependencies",
            backstory="""You are an expert in productivity and task management. You excel at 
            understanding task complexity, estimating realistic time requirements, and identifying 
            critical dependencies that affect task scheduling.""",
            llm=self.llm,
            tools=[DailyPlanGenerator.format_task_dependencies],
            verbose=True
        )
        
        # Schedule Optimization Agent
        schedule_optimizer = Agent(
            role="Schedule Optimization Expert",
            goal="Create optimal daily schedules that maximize productivity and respect dependencies",
            backstory="""You are a scheduling optimization expert who understands human 
            productivity patterns, energy levels throughout the day, and how to sequence 
            tasks for maximum efficiency.""",
            llm=self.llm,
            verbose=True
        )
        
        # Daily Plan Formatter Agent
        plan_formatter = Agent(
            role="Daily Plan Documentation Specialist",
            goal="Format the optimized schedule into a comprehensive, actionable daily plan document",
            backstory="""You are a documentation specialist who creates clear, actionable 
            daily plans. You excel at presenting complex scheduling information in an 
            easy-to-follow format that helps users stay organized and productive.""",
            llm=self.llm,
            verbose=True
        )
        
        return task_analyzer, schedule_optimizer, plan_formatter
    
    def _create_planning_tasks(self, user_tasks: List[Dict], dependencies: List[Dict], 
                             task_analyzer: Agent, schedule_optimizer: Agent, 
                             plan_formatter: Agent) -> tuple:
        """Create the CrewAI tasks for the planning process."""
        
        # Task Analysis Task
        analysis_task = Task(
            description=f"""
            Analyze the following user tasks and dependencies to understand:
            1. Task priorities and complexity
            2. Estimated durations and effort required
            3. Dependencies between tasks
            4. Optimal sequencing requirements
            
            User Tasks: {json.dumps(user_tasks, indent=2)}
            Dependencies: {json.dumps(dependencies, indent=2)}
            
            Provide a comprehensive analysis including:
            - Priority categorization (High/Medium/Low)
            - Time estimates validation
            - Dependency chain analysis
            - Recommendations for task grouping
            """,
            agent=task_analyzer,
            expected_output="Detailed task analysis with priority levels, time estimates, and dependency insights"
        )
        
        # Schedule Optimization Task
        optimization_task = Task(
            description=f"""
            Based on the task analysis, create an optimized daily schedule that:
            1. Respects task dependencies
            2. Balances workload across time blocks
            3. Considers human productivity patterns
            4. Maximizes efficiency and focus
            
            Schedule constraints:
            - Morning block: 9:00 AM - 12:00 PM (3 hours)
            - Afternoon block: 1:00 PM - 5:00 PM (4 hours)
            - Evening block: 6:00 PM - 8:00 PM (2 hours)
            
            Create an optimized task allocation for these time blocks.
            """,
            agent=schedule_optimizer,
            expected_output="Optimized daily schedule with tasks allocated to appropriate time blocks"
        )
        
        # Plan Formatting Task
        formatting_task = Task(
            description=f"""
            Create a comprehensive daily plan document using this template:
            
            {self.template_content}
            
            Format the schedule and analysis into a professional, actionable daily plan.
            Include:
            - Daily overview with key metrics
            - Time-blocked schedule
            - Priority-based task breakdown
            - Dependency information
            - Productivity tips relevant to the task mix
            
            Ensure the output is properly formatted markdown that follows the template structure.
            """,
            agent=plan_formatter,
            expected_output="Complete daily plan document in markdown format following the provided template"
        )
        
        return analysis_task, optimization_task, formatting_task
    
    def generate_daily_plan(self, user_id: int, target_date: datetime = None) -> str:
        """
        Generate a daily plan for a user's tasks.
        
        Args:
            user_id: ID of the user for whom to generate the plan
            target_date: Date for the plan (defaults to today)
            
        Returns:
            Generated daily plan as markdown string
        """
        target_date = target_date or datetime.now()
        
        # Get user tasks and dependencies from database
        user_tasks, dependencies = self._fetch_user_tasks_and_dependencies(user_id, target_date)
        
        if not user_tasks:
            return self._generate_empty_plan(target_date)
        
        # Create agents and tasks
        task_analyzer, schedule_optimizer, plan_formatter = self._create_planning_agents()
        analysis_task, optimization_task, formatting_task = self._create_planning_tasks(
            user_tasks, dependencies, task_analyzer, schedule_optimizer, plan_formatter
        )
        
        # Create and execute the crew
        crew = Crew(
            agents=[task_analyzer, schedule_optimizer, plan_formatter],
            tasks=[analysis_task, optimization_task, formatting_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew and return the result
        try:
            result = crew.kickoff()
            # Extract the string content from CrewOutput object
            if hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
        except Exception as e:
            return f"Error generating daily plan: {str(e)}"
    
    def _fetch_user_tasks_and_dependencies(self, user_id: int, target_date: datetime = None) -> tuple:
        """
        Fetch user tasks and dependencies from the database, filtering for tasks due within the next week.
        
        Args:
            user_id: ID of the user
            target_date: Reference date for filtering (defaults to today)
            
        Returns:
            Tuple of (tasks_list, dependencies_list)
        """
        # This would typically use dependency injection, but for now we'll create a session
        # In production, this should be properly injected
        from app.database import SessionLocal
        
        if target_date is None:
            target_date = datetime.now()
        
        # Calculate the date range: from target_date to 7 days later
        end_date = target_date + timedelta(days=7)
        
        db = SessionLocal()
        try:
            # Fetch user tasks with related data, filtering by deadline within the next week
            # Include tasks with no deadline or deadline within the next week
            tasks = db.query(TaskModel).filter(
                TaskModel.user_id == user_id,
                (TaskModel.deadline.is_(None) | 
                 ((TaskModel.deadline >= target_date.date()) & 
                  (TaskModel.deadline <= end_date.date())))
            ).all()
            
            user_tasks = []
            task_ids = []
            for task in tasks:
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'deadline': task.deadline.isoformat() if task.deadline else None,
                    'estimated_duration': task.estimated_duration or 60,
                    'status': task.status,
                    'priority_score': task.priority_score.score if task.priority_score else 3,
                    'tshirt_size': task.tshirt_score.tshirt_size if task.tshirt_score else 'M'
                }
                user_tasks.append(task_dict)
                task_ids.append(task.id)
            
            # Fetch dependencies only for the filtered tasks
            dependencies = db.query(TaskDependency).filter(
                TaskDependency.task_id.in_(task_ids)
            ).all()
            
            dep_list = []
            for dep in dependencies:
                # Only include dependencies where both tasks are in our filtered set
                if dep.depends_on_task_id in task_ids:
                    dep_dict = {
                        'task_id': dep.task_id,
                        'task_title': dep.task.title,
                        'depends_on_id': dep.depends_on_task_id,
                        'depends_on_title': dep.depends_on_task.title
                    }
                    dep_list.append(dep_dict)
            
            return user_tasks, dep_list
        finally:
            db.close()
    
    def _generate_empty_plan(self, target_date: datetime) -> str:
        """Generate a plan for when no tasks are available."""
        formatted_date = target_date.strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""# Daily Task Plan

## Daily Overview 
**Total Tasks:** 0  
**Estimated Duration:** 0 hours  
**Priority Distribution:** High: 0, Medium: 0, Low: 0

## Daily Goals
No tasks scheduled for today. Consider this a perfect opportunity for:
- Planning upcoming projects
- Learning new skills
- Taking a well-deserved break
- Reflecting on recent accomplishments

## Task Schedule

### Morning Block (9:00 AM - 12:00 PM)
No tasks scheduled - Free time available

### Afternoon Block (1:00 PM - 5:00 PM)
No tasks scheduled - Free time available

### Evening Block (6:00 PM - 8:00 PM) 
No tasks scheduled - Free time available

## Task Breakdown by Priority

### 🔴 High Priority Tasks
No high priority tasks scheduled

### 🟡 Medium Priority Tasks
No medium priority tasks scheduled

### 🟢 Low Priority Tasks
No low priority tasks scheduled

## 🔗 Task Dependencies
No task dependencies to consider"""


# Factory function for easy instantiation
def create_daily_plan_generator(openai_api_key: str = None) -> DailyPlanGenerator:
    """Create a new daily plan generator instance."""
    return DailyPlanGenerator(openai_api_key)


# Convenience function for direct usage
def generate_user_daily_plan(user_id: int, target_date: datetime = None, 
                           openai_api_key: str = None) -> str:
    """
    Generate a daily plan for a specific user.
    
    Args:
        user_id: ID of the user
        target_date: Date for the plan (defaults to today)
        openai_api_key: OpenAI API key (uses environment variable if not provided)
        
    Returns:
        Generated daily plan as markdown string
    """
    generator = create_daily_plan_generator(openai_api_key)
    return generator.generate_daily_plan(user_id, target_date)

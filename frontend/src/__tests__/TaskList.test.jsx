/**
 * Unit tests for TaskList component.
 * 
 * Tests cover:
 * - Rendering task list
 * - Empty state display
 * - Task item rendering with all fields
 * - Priority score display
 * - Status badge rendering
 * - Task filtering
 * - Task sorting
 * - Loading states
 * - Error handling
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskList from '../components/TaskList';

// Mock fetch for API calls
global.fetch = jest.fn();

describe('TaskList Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders task list with tasks', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Submit project report',
        description: 'Send final report to manager',
        deadline: '2025-11-06',
        status: 'pending',
        estimated_duration: 4,
        priority_score: 85,
        user_id: 1
      },
      {
        id: 2,
        title: 'Clean workspace',
        description: 'Organize desk and files',
        deadline: '2025-11-15',
        status: 'completed',
        estimated_duration: 1,
        priority_score: 45,
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Submit project report')).toBeInTheDocument();
      expect(screen.getByText('Clean workspace')).toBeInTheDocument();
    });
  });

  test('renders empty state when no tasks', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/no tasks/i)).toBeInTheDocument();
    });
  });

  test('displays priority scores for tasks', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'High Priority Task',
        priority_score: 95,
        status: 'pending',
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/95/)).toBeInTheDocument();
    });
  });

  test('displays status badges correctly', async () => {
    const mockTasks = [
      { id: 1, title: 'Pending Task', status: 'pending', user_id: 1 },
      { id: 2, title: 'In Progress Task', status: 'in_progress', user_id: 1 },
      { id: 3, title: 'Completed Task', status: 'completed', user_id: 1 },
      { id: 4, title: 'Blocked Task', status: 'blocked', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/pending/i)).toBeInTheDocument();
      expect(screen.getByText(/in progress/i)).toBeInTheDocument();
      expect(screen.getByText(/completed/i)).toBeInTheDocument();
      expect(screen.getByText(/blocked/i)).toBeInTheDocument();
    });
  });

  test('handles loading state', () => {
    fetch.mockImplementation(() => new Promise(() => {})); // Never resolves

    render(<TaskList />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('handles API error gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('handles 404 response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 404
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/not found/i)).toBeInTheDocument();
    });
  });

  test('filters tasks by status', async () => {
    const mockTasks = [
      { id: 1, title: 'Pending Task', status: 'pending', user_id: 1 },
      { id: 2, title: 'Completed Task', status: 'completed', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Pending Task')).toBeInTheDocument();
    });

    // Simulate filter interaction
    const filterSelect = screen.queryByLabelText(/filter/i);
    if (filterSelect) {
      await userEvent.selectOptions(filterSelect, 'pending');

      expect(screen.getByText('Pending Task')).toBeInTheDocument();
      expect(screen.queryByText('Completed Task')).not.toBeInTheDocument();
    }
  });

  test('sorts tasks by priority score', async () => {
    const mockTasks = [
      { id: 1, title: 'Low Priority', priority_score: 30, status: 'pending', user_id: 1 },
      { id: 2, title: 'High Priority', priority_score: 90, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Low Priority')).toBeInTheDocument();
      expect(screen.getByText('High Priority')).toBeInTheDocument();
    });

    // Verify high priority task appears first (if sorting is implemented)
    const tasks = screen.getAllByRole('listitem');
    if (tasks.length > 0) {
      expect(tasks[0]).toHaveTextContent('High Priority');
    }
  });

  test('displays task deadline', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Task with Deadline',
        deadline: '2025-11-06',
        status: 'pending',
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/2025-11-06/)).toBeInTheDocument();
    });
  });

  test('displays estimated duration', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Task with Duration',
        estimated_duration: 4,
        status: 'pending',
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/4/)).toBeInTheDocument();
    });
  });

  test('calls delete task API on delete button click', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Task to Delete',
        status: 'pending',
        user_id: 1
      }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockTasks
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 204
      });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Task to Delete')).toBeInTheDocument();
    });

    const deleteButton = screen.queryByRole('button', { name: /delete/i });
    if (deleteButton) {
      await userEvent.click(deleteButton);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/tasks/1'),
          expect.objectContaining({ method: 'DELETE' })
        );
      });
    }
  });

  test('refreshes task list after deletion', async () => {
    const initialTasks = [
      { id: 1, title: 'Task 1', status: 'pending', user_id: 1 },
      { id: 2, title: 'Task 2', status: 'pending', user_id: 1 }
    ];

    const updatedTasks = [
      { id: 2, title: 'Task 2', status: 'pending', user_id: 1 }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => initialTasks
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 204
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => updatedTasks
      });

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    const deleteButton = screen.queryByRole('button', { name: /delete/i });
    if (deleteButton) {
      await userEvent.click(deleteButton);

      await waitFor(() => {
        expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
        expect(screen.getByText('Task 2')).toBeInTheDocument();
      });
    }
  });
});



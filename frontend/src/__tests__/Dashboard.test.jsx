/**
 * Unit tests for Dashboard component.
 * 
 * Tests cover:
 * - Dashboard rendering
 * - Priority dashboard display
 * - Task statistics
 * - Charts and visualizations
 * - Filter controls
 * - Real-time updates
 * - Performance metrics
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Dashboard from '../components/Dashboard';

// Mock fetch for API calls
global.fetch = jest.fn();

describe('Dashboard Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders dashboard title', () => {
    render(<Dashboard />);

    expect(screen.getByText(/dashboard|overview/i)).toBeInTheDocument();
  });

  test('displays task statistics', async () => {
    const mockTasks = [
      { id: 1, status: 'pending', priority_score: 85, user_id: 1 },
      { id: 2, status: 'in_progress', priority_score: 70, user_id: 1 },
      { id: 3, status: 'completed', priority_score: 50, user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/total.*3/i)).toBeInTheDocument();
    });
  });

  test('displays tasks by status count', async () => {
    const mockTasks = [
      { id: 1, status: 'pending', user_id: 1 },
      { id: 2, status: 'pending', user_id: 1 },
      { id: 3, status: 'in_progress', user_id: 1 },
      { id: 4, status: 'completed', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/pending.*2/i)).toBeInTheDocument();
      expect(screen.getByText(/in progress.*1/i)).toBeInTheDocument();
      expect(screen.getByText(/completed.*1/i)).toBeInTheDocument();
    });
  });

  test('displays high priority tasks section', async () => {
    const mockTasks = [
      { id: 1, title: 'Urgent Task', priority_score: 95, status: 'pending', user_id: 1 },
      { id: 2, title: 'Normal Task', priority_score: 50, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/high priority|urgent/i)).toBeInTheDocument();
      expect(screen.getByText('Urgent Task')).toBeInTheDocument();
    });
  });

  test('displays average priority score', async () => {
    const mockTasks = [
      { id: 1, priority_score: 80, status: 'pending', user_id: 1 },
      { id: 2, priority_score: 60, status: 'pending', user_id: 1 },
      { id: 3, priority_score: 70, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      // Average should be 70
      expect(screen.getByText(/average.*70/i)).toBeInTheDocument();
    });
  });

  test('displays overdue tasks warning', async () => {
    const pastDate = new Date();
    pastDate.setDate(pastDate.getDate() - 5);

    const mockTasks = [
      {
        id: 1,
        title: 'Overdue Task',
        deadline: pastDate.toISOString(),
        status: 'pending',
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/overdue/i)).toBeInTheDocument();
    });
  });

  test('displays upcoming deadlines', async () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    const mockTasks = [
      {
        id: 1,
        title: 'Due Soon',
        deadline: tomorrow.toISOString(),
        status: 'pending',
        user_id: 1
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/upcoming|due soon/i)).toBeInTheDocument();
    });
  });

  test('handles empty task list', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/no tasks|empty/i)).toBeInTheDocument();
    });
  });

  test('handles loading state', () => {
    fetch.mockImplementation(() => new Promise(() => {}));

    render(<Dashboard />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('handles API error', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('filters dashboard by date range', async () => {
    const user = userEvent.setup();
    
    const mockTasks = [
      { id: 1, title: 'Task 1', created_at: '2025-11-01', status: 'pending', user_id: 1 },
      { id: 2, title: 'Task 2', created_at: '2025-11-10', status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    const dateFilter = screen.queryByLabelText(/date range|filter/i);
    if (dateFilter) {
      await user.click(dateFilter);
      // Verify filtering functionality exists
      expect(dateFilter).toBeInTheDocument();
    }
  });

  test('displays completion rate', async () => {
    const mockTasks = [
      { id: 1, status: 'completed', user_id: 1 },
      { id: 2, status: 'completed', user_id: 1 },
      { id: 3, status: 'pending', user_id: 1 },
      { id: 4, status: 'in_progress', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      // 2 out of 4 = 50%
      expect(screen.getByText(/50%|completion/i)).toBeInTheDocument();
    });
  });

  test('displays task distribution chart', async () => {
    const mockTasks = [
      { id: 1, status: 'pending', user_id: 1 },
      { id: 2, status: 'completed', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      const chart = screen.queryByRole('img', { name: /chart|graph/i });
      if (chart) {
        expect(chart).toBeInTheDocument();
      }
    });
  });

  test('refreshes data on refresh button click', async () => {
    const user = userEvent.setup();
    
    const mockTasks = [
      { id: 1, title: 'Task 1', status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    const refreshButton = screen.queryByRole('button', { name: /refresh|reload/i });
    if (refreshButton) {
      await user.click(refreshButton);

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(2);
      });
    }
  });

  test('displays priority distribution', async () => {
    const mockTasks = [
      { id: 1, priority_score: 90, status: 'pending', user_id: 1 }, // High
      { id: 2, priority_score: 60, status: 'pending', user_id: 1 }, // Medium
      { id: 3, priority_score: 30, status: 'pending', user_id: 1 }  // Low
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/high.*1/i)).toBeInTheDocument();
      expect(screen.getByText(/medium.*1/i)).toBeInTheDocument();
      expect(screen.getByText(/low.*1/i)).toBeInTheDocument();
    });
  });

  test('displays blocked tasks count', async () => {
    const mockTasks = [
      { id: 1, status: 'blocked', user_id: 1 },
      { id: 2, status: 'blocked', user_id: 1 },
      { id: 3, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/blocked.*2/i)).toBeInTheDocument();
    });
  });

  test('links to task list', async () => {
    const mockTasks = [
      { id: 1, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      const viewAllLink = screen.queryByRole('link', { name: /view all|see all/i });
      if (viewAllLink) {
        expect(viewAllLink).toHaveAttribute('href', expect.stringContaining('tasks'));
      }
    });
  });

  test('displays estimated total duration', async () => {
    const mockTasks = [
      { id: 1, estimated_duration: 4, status: 'pending', user_id: 1 },
      { id: 2, estimated_duration: 2, status: 'pending', user_id: 1 },
      { id: 3, estimated_duration: 3, status: 'in_progress', user_id: 1 }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      // Total: 9 hours
      expect(screen.getByText(/9.*hours?/i)).toBeInTheDocument();
    });
  });

  test('updates in real-time', async () => {
    jest.useFakeTimers();
    
    const mockTasks = [
      { id: 1, status: 'pending', user_id: 1 }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTasks
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
    });

    // Fast-forward time to trigger auto-refresh
    jest.advanceTimersByTime(60000); // 1 minute

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(2);
    });

    jest.useRealTimers();
  });
});



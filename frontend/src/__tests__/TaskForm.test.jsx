/**
 * Unit tests for TaskForm component.
 * 
 * Tests cover:
 * - Form rendering
 * - Input validation
 * - Form submission
 * - API integration
 * - Error handling
 * - Success feedback
 * - Field requirements
 * - Date picker functionality
 * - Status selection
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskForm from '../components/TaskForm';

// Mock fetch for API calls
global.fetch = jest.fn();

describe('TaskForm Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders task form with all fields', () => {
    render(<TaskForm />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/deadline/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/estimated duration/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
  });

  test('renders submit button', () => {
    render(<TaskForm />);

    expect(screen.getByRole('button', { name: /submit|create/i })).toBeInTheDocument();
  });

  test('validates required title field', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  test('validates empty title', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const titleInput = screen.getByLabelText(/title/i);
    await user.type(titleInput, '   ');
    await user.clear(titleInput);

    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });
  });

  test('accepts valid task data', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({
        id: 1,
        title: 'New Task',
        description: 'Task description',
        status: 'pending',
        user_id: 1
      })
    });

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    await user.type(screen.getByLabelText(/description/i), 'Task description');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tasks'),
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          }),
          body: expect.stringContaining('New Task')
        })
      );
    });
  });

  test('displays success message after submission', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: 1, title: 'New Task', status: 'pending', user_id: 1 })
    });

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/success|created/i)).toBeInTheDocument();
    });
  });

  test('handles API error during submission', async () => {
    const user = userEvent.setup();
    
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/error|failed/i)).toBeInTheDocument();
    });
  });

  test('handles 422 validation error from API', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: 'Invalid data' })
    });

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid|validation/i)).toBeInTheDocument();
    });
  });

  test('clears form after successful submission', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: 1, title: 'New Task', status: 'pending', user_id: 1 })
    });

    render(<TaskForm />);

    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    await user.type(titleInput, 'New Task');
    await user.type(descriptionInput, 'Description');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(titleInput).toHaveValue('');
      expect(descriptionInput).toHaveValue('');
    });
  });

  test('allows selecting status', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const statusSelect = screen.getByLabelText(/status/i);
    await user.selectOptions(statusSelect, 'in_progress');

    expect(statusSelect).toHaveValue('in_progress');
  });

  test('displays all valid status options', () => {
    render(<TaskForm />);

    const statusSelect = screen.getByLabelText(/status/i);
    const options = Array.from(statusSelect.options).map(opt => opt.value);

    expect(options).toContain('pending');
    expect(options).toContain('in_progress');
    expect(options).toContain('completed');
    expect(options).toContain('blocked');
  });

  test('validates estimated duration is positive', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const durationInput = screen.getByLabelText(/estimated duration/i);
    await user.type(durationInput, '-5');

    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/positive|greater than/i)).toBeInTheDocument();
    });
  });

  test('accepts zero estimated duration', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: 1, title: 'Quick Task', estimated_duration: 0, status: 'pending', user_id: 1 })
    });

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'Quick Task');
    await user.type(screen.getByLabelText(/estimated duration/i), '0');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
    });
  });

  test('allows setting future deadline', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const deadlineInput = screen.getByLabelText(/deadline/i);
    const futureDate = '2025-12-31';
    
    await user.type(deadlineInput, futureDate);

    expect(deadlineInput).toHaveValue(futureDate);
  });

  test('allows setting past deadline', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const deadlineInput = screen.getByLabelText(/deadline/i);
    const pastDate = '2020-01-01';
    
    await user.type(deadlineInput, pastDate);

    expect(deadlineInput).toHaveValue(pastDate);
  });

  test('disables submit button during submission', async () => {
    const user = userEvent.setup();
    
    fetch.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)));

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();
  });

  test('handles very long title', async () => {
    const user = userEvent.setup();
    render(<TaskForm />);

    const longTitle = 'A'.repeat(500);
    const titleInput = screen.getByLabelText(/title/i);
    
    await user.type(titleInput, longTitle);

    expect(titleInput).toHaveValue(longTitle);
  });

  test('handles special characters in title', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: 1, title: 'Task with émojis 🚀', status: 'pending', user_id: 1 })
    });

    render(<TaskForm />);

    await user.type(screen.getByLabelText(/title/i), 'Task with émojis 🚀');
    
    const submitButton = screen.getByRole('button', { name: /submit|create/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
    });
  });

  test('renders in edit mode with existing task data', () => {
    const existingTask = {
      id: 1,
      title: 'Existing Task',
      description: 'Existing description',
      deadline: '2025-11-10',
      estimated_duration: 3,
      status: 'in_progress'
    };

    render(<TaskForm task={existingTask} mode="edit" />);

    expect(screen.getByLabelText(/title/i)).toHaveValue('Existing Task');
    expect(screen.getByLabelText(/description/i)).toHaveValue('Existing description');
    expect(screen.getByLabelText(/status/i)).toHaveValue('in_progress');
  });

  test('calls update API in edit mode', async () => {
    const user = userEvent.setup();
    const existingTask = {
      id: 1,
      title: 'Existing Task',
      status: 'pending',
      user_id: 1
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ ...existingTask, title: 'Updated Task' })
    });

    render(<TaskForm task={existingTask} mode="edit" />);

    const titleInput = screen.getByLabelText(/title/i);
    await user.clear(titleInput);
    await user.type(titleInput, 'Updated Task');
    
    const submitButton = screen.getByRole('button', { name: /update|save/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tasks/1'),
        expect.objectContaining({
          method: 'PUT'
        })
      );
    });
  });
});



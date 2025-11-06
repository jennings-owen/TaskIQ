import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Agile TaskIQ application', () => {
  render(<App />);
  const titleElement = screen.getByText(/Agile TaskIQ/i);
  expect(titleElement).toBeInTheDocument();
});

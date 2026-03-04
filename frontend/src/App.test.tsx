import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock API calls
jest.mock('./services/api', () => ({
  fetchAPIInfo: jest.fn(() => Promise.resolve({
    api_name: 'Stock Analysis Platform',
    version: '0.1.0',
    environment: 'development',
    features: ['股票行情数据获取', '技术面分析'],
    documentation: '/docs',
    timestamp: '2024-01-01T00:00:00',
  })),
  fetchHealthCheck: jest.fn(() => Promise.resolve({
    status: 'healthy',
    database: 'connected',
    redis: 'connected',
    timestamp: '2024-01-01T00:00:00',
  })),
}));

describe('App Component', () => {
  test('renders app without crashing', () => {
    render(<App />);
    // Just verify the app renders without errors
    expect(true).toBe(true);
  });
});

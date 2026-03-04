/**
 * API Service - Frontend API calls
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API Base URL from environment variable or default
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add authorization token if exists
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle errors
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Fetch API information
 */
export const fetchAPIInfo = async () => {
  try {
    const response = await apiClient.get('/api/info');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch API info:', error);
    throw error;
  }
};

/**
 * Fetch health check status
 */
export const fetchHealthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch health check:', error);
    throw error;
  }
};

/**
 * Generic GET request
 */
export const get = async <T = any>(url: string, params?: any): Promise<T> => {
  const response = await apiClient.get<T>(url, { params });
  return response.data;
};

/**
 * Generic POST request
 */
export const post = async <T = any>(url: string, data?: any): Promise<T> => {
  const response = await apiClient.post<T>(url, data);
  return response.data;
};

/**
 * Generic PUT request
 */
export const put = async <T = any>(url: string, data?: any): Promise<T> => {
  const response = await apiClient.put<T>(url, data);
  return response.data;
};

/**
 * Generic DELETE request
 */
export const del = async <T = any>(url: string): Promise<T> => {
  const response = await apiClient.delete<T>(url);
  return response.data;
};

// ---- News API ----

export interface NewsArticle {
  id: number;
  title: string;
  description: string;
  content?: string;
  source: string;
  author: string;
  url: string;
  image_url: string;
  category: string;
  sentiment: string;
  keywords: string[];
  importance_score: number;
  published_at: string;
  collected_at?: string;
}

export interface NewsListResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  data: NewsArticle[];
}

export interface NewsCategory {
  name: string;
  count: number;
}

export const fetchNewsList = async (params: {
  category?: string;
  keyword?: string;
  page?: number;
  page_size?: number;
  sort_by?: string;
}): Promise<NewsListResponse> => {
  const response = await apiClient.get('/api/news', { params });
  return response.data;
};

export const fetchNewsDetail = async (newsId: number): Promise<NewsArticle> => {
  const response = await apiClient.get(`/api/news/${newsId}`);
  return response.data;
};

export const fetchNewsCategories = async (): Promise<{ data: NewsCategory[] }> => {
  const response = await apiClient.get('/api/news/categories');
  return response.data;
};

export const triggerNewsCollection = async (): Promise<{ status: string; collected: number }> => {
  const response = await apiClient.post('/api/news/collect');
  return response.data;
};

export default apiClient;

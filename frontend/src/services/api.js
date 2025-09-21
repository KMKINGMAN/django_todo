import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token is invalid or expired
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      
      // Only redirect if we're not already on the login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const login = (username, password) => {
  return api.post('/api/auth/login/', { username, password });
};

export const validateToken = () => {
  return api.get('/api/auth/validate/');
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
};

export const getTasks = () => {
  return api.get('/api/tasks/');
};

export const addTask = (task) => {
  return api.post('/api/tasks/', task);
};

export const getTodos = () => {
  return api.get('/api/todos/');
};

export const addTodo = (todo) => {
  return api.post('/api/todos/', todo);
};

export const updateTodo = (todoId, updates) => {
  return api.patch(`/api/todos/${todoId}/`, updates);
};

export const removeTodo = (todoId) => {
  return api.delete(`/api/todos/${todoId}/`);
};

export const removeTask = (taskId) => {
  return api.delete(`/api/tasks/${taskId}/`);
};

export default api;

import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  // Vite proxy handles /api in dev, VITE_API_URL handles production
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 10000,
});

// Add a request interceptor to attach the JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // If 401 Unauthorized, token might be expired.
      localStorage.removeItem('token');
      // Only alert if we are not already on the login page
      if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
        alert('세션이 만료되었습니다. 다시 로그인해주세요.');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

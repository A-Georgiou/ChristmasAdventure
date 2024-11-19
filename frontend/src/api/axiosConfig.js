import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
});

api.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
);

export default api;
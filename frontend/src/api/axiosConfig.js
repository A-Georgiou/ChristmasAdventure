import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 30000,
  headers: {'Content-Type': 'application/json'}
});

api.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
);

export default api;
import axios from 'axios';
import { useAuthStore } from './stores/authStore';
import router from './router'

axios.defaults.withCredentials = true

const api = axios.create({
    baseURL: 'http://localhost:8000/', // REST API base URL
baseURL: 'https://vatrochat-backend.onrender.com/', // REST API base URL
});

api.interceptors.response.use(resp => {
  return resp;
},
  (error) => {
    if (error.response && error.response.status === 401) {
      useAuthStore().clearUser();

      router.push({ path: '/login' })
    }
    return Promise.reject(error);
  }
);

api.interceptors.request.use(
  config => {
    const token = useAuthStore().getToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default api;
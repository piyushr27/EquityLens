import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const capTableAPI = {
  loadSampleData: () => api.post('/load-sample-data'),
  uploadCapTable: (data) => api.post('/upload-cap-table-json', data),
  getCapTable: () => api.get('/cap-table'),
  query: (question) => api.post('/query', { question }),
  analyze: () => api.post('/analyze'),
  getTools: () => api.get('/tools'),
  getHistory: (limit = 10) => api.get(`/history?limit=${limit}`),
  calculateDilution: (newShares) => api.get(`/dilution-calculator?new_shares=${newShares}`),
  health: () => api.get('/health'),
};

export default api;

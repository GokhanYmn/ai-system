import axios from 'axios';

const API_BASE_URL = 'http://localhost:8003';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Sistem durumu
  getSystemStatus: () => api.get('/system/agents/status'),
  getSystemHealth: () => api.get('/system/health'),
  getSystemSummary: () => api.get('/reports/summary'),

  // Analiz servisleri
  comprehensiveAnalysis: (symbol) => api.post(`/analysis/comprehensive/${symbol}`),
  quickAnalysis: (symbol) => api.get(`/analysis/quick/${symbol}`),

  // Agent servisleri
  getAgentStatus: (agentName) => api.get(`/agents/${agentName}/status`),
  executeAgentTask: (agentName, taskData) => api.post(`/agents/${agentName}/task`, taskData),

  // Trading servisleri
  executeTrade: (tradeParams) => api.post('/trading/execute', tradeParams),
  getLearningPerformance: () => api.get('/learning/performance'),
  
  // Report servisleri
  generateReport: (symbol) => api.post(`/reports/generate?symbol=${symbol}`),
};

export default api;
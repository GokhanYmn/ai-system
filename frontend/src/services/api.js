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

    // Notification servisleri
  sendEmailNotification: (emailData) => api.post('/notifications/email', emailData),
  sendTelegramNotification: (telegramData) => api.post('/notifications/telegram', telegramData),
  subscribeUser: (userData) => api.post('/notifications/subscribe', userData),
  scheduleNotification: (scheduleConfig) => api.post('/notifications/schedule', scheduleConfig),
  broadcastAnalysis: (symbol) => api.post(`/notifications/broadcast/${symbol}`),
  getNotificationStats: () => api.get('/notifications/stats'),
  comprehensiveAnalysisWithNotification: (symbol, notifySubscribers = true) => 
    api.post(`/analysis/comprehensive/${symbol}/notify?notify_subscribers=${notifySubscribers}`),

    // Portfolio Management servisleri
  optimizePortfolio: (userProfile, marketData) => 
    api.post('/portfolio/optimize', { user_profile: userProfile, market_data: marketData }),
  calculateAssetAllocation: (riskTolerance, investmentAmount) =>
    api.post('/portfolio/allocate', { risk_tolerance: riskTolerance, investment_amount: investmentAmount }),
  rebalancePortfolio: (currentPortfolio, targetAllocation) =>
    api.post('/portfolio/rebalance', { current_portfolio: currentPortfolio, target_allocation: targetAllocation }),

  // Personal Portfolio servisleri  
  addPortfolioPosition: (userId, positionData) =>
    api.post('/personal-portfolio/add-position', { user_id: userId, position_data: positionData }),
  updatePortfolioPrices: (userId, currentPrices) =>
    api.post('/personal-portfolio/update-prices', { user_id: userId, current_prices: currentPrices }),
  getPortfolioPerformance: (userId) =>
    api.get(`/personal-portfolio/performance/${userId}`),
  analyzePersonalPortfolio: (userId, marketData) =>
    api.post('/personal-portfolio/analyze', { user_id: userId, market_data: marketData }),
  getPersonalRecommendations: (userId, marketAnalysis) =>
    api.post('/personal-portfolio/recommendations', { user_id: userId, market_analysis: marketAnalysis }),

  // Sentiment Analysis servisleri
  analyzeSocialSentiment: (symbol, platform = 'twitter') =>
    api.post(`/sentiment/social/${symbol}?platform=${platform}`),
  analyzeNewsSentiment: (newsData) =>
    api.post('/sentiment/news', { news_data: newsData }),
  getFearGreedIndex: () =>
    api.get('/sentiment/fear-greed'),
  getMarketSentiment: () =>
    api.get('/sentiment/market'),
  getSentimentSignals: (symbol) =>
    api.post(`/sentiment/signals/${symbol}`),
  getSentimentTrends: (symbol, timeframe = '7d') =>
    api.get(`/sentiment/trends/${symbol}?timeframe=${timeframe}`),

  // Performance servisleri
  getPerformanceDashboard: () => api.get('/performance/dashboard'),
  startPerformanceMonitoring: () => api.post('/performance/start'),
  stopPerformanceMonitoring: () => api.post('/performance/stop'),
  optimizeSystemPerformance: () => api.post('/performance/optimize'),
  getPerformanceMetrics: () => api.get('/performance/metrics'),
  getSystemHealth: () => api.get('/performance/health'),
  analyzeAgentPerformance: (agentName = null) => 
    api.post('/performance/analyze', { agent_name: agentName }),
  detectBottlenecks: () => api.get('/performance/bottlenecks'),
  generatePerformanceReport: (period = 'daily') => 
    api.post('/performance/report', { period }),

 
  comprehensiveAnalysisPlus: (symbol) => api.post(`/analysis/comprehensive-plus/${symbol}`),


};




export default api;
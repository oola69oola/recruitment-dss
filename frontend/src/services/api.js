import axios from 'axios';

const rawBaseUrl = (import.meta.env.VITE_API_URL || '').trim();
const cleanBaseUrl = rawBaseUrl.replace(/\/+$/, '');
const baseURL = cleanBaseUrl ? `${cleanBaseUrl}/api` : '/api';

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach JWT token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('recruitiq_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor to handle expired tokens gracefully
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('recruitiq_token');
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (data) => api.post('/auth/register/', data),
  getCurrentUser: () => api.get('/auth/me/'),
};

export const jobService = {
  list: () => api.get('/jobs/'),
  get: (id) => api.get(`/jobs/${id}/`),
  create: (data) => api.post('/jobs/', data),
  update: (id, data) => api.put(`/jobs/${id}/`, data),
  patch: (id, data) => api.patch(`/jobs/${id}/`, data),
  delete: (id) => api.delete(`/jobs/${id}/`),
  getCanonicalRoles: () => api.get('/jobs/canonical-roles/'),
  selectCanonicalRole: (data) => api.post('/jobs/select-canonical-role/', data),
  loadBenchmarkData: (jobId, count = 100, replace = false) =>
    api.post(`/jobs/${jobId}/load-benchmark-data/`, { count, replace }),
  extractCriteria: (data) => api.post('/jobs/extract-criteria/', data),
};

export const candidateService = {
  list: (jobId) => api.get('/candidates/', { params: { job_id: jobId } }),
  get: (id) => api.get(`/candidates/${id}/`),
  bulkUpload: (formData) => api.post('/candidates/bulk-upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

export const evaluationService = {
  list: (jobId) => api.get('/evaluations/', { params: { job_id: jobId } }),
  evaluateJob: (jobId) => api.post('/evaluations/evaluate-job/', { job_id: jobId }),
  fairnessAudit: (jobId, threshold = 70.0) => 
    api.get('/evaluations/fairness-audit/', { params: { job_id: jobId, threshold } }),
  rerankCohort: (data) => api.post('/evaluations/rerank-cohort/', data),
  getActivityLogs: () => api.get('/evaluations/activity-logs/'),
  logActivity: (data) => api.post('/evaluations/log-activity/', data),
};

export default api;

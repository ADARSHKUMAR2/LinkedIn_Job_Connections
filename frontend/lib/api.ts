import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Connection {
  id: number;
  first_name: string;
  last_name: string;
  company: string;
  position: string;
}

export interface Job {
  id: number;
  job_id: string;
  title: string;
  company: string;
  location: string | null;
  apply_link: string | null;
}

export interface Match {
  Company: string;
  'Target Role': string;
  Location: string;
  'Inside Contact': string;
  'Contact Position': string;
  'Application Link': string;
}

export interface MatcherFilterConfig {
  target_location?: string;
  target_company?: string;
  min_connections?: number;
}

export interface ScrapeRequest {
  search_query: string;
  location: string;
}

export interface OutreachDraft {
  subject_line: string | null;
  message_body: string;
}

// API Functions
export const connectionsApi = {
  getAll: () => api.get<Connection[]>('/api/connections/'),
  create: (data: Omit<Connection, 'id'>) => api.post<Connection>('/api/connections/', data),
  delete: (id: number) => api.delete(`/api/connections/${id}`),
};

export const jobsApi = {
  getAll: () => api.get<Job[]>('/api/jobs/'),
  scrape: (data: ScrapeRequest) => api.post('/api/jobs/scrape', data),
};

export const matchesApi = {
  sweep: (filters: MatcherFilterConfig) => api.post<Match[]>('/api/matches/sweep', filters),
  draftOutreach: (matchContext: Match) => api.post<OutreachDraft>('/api/matches/draft-outreach', matchContext),
};

export default api;

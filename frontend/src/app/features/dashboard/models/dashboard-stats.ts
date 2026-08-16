export interface DashboardStats {
  projects: number;
  test_runs: number;
  test_results: number;
  pass_rate: number;
  failed: number;
  errors: number;
  pending: number;
  status_distribution: {
    PASSED: number;
    FAILED: number;
    ERROR: number;
    PENDING: number;
  };
  recent_runs: RecentTestRun[];
}

export interface RecentTestRun {
  id: string;
  run_id: string;
  project_id: string;
  test_suite_id: string;
  software_version: string;
  status: 'PASSED' | 'FAILED' | 'ERROR' | 'PENDING';
  started_at: string;
  completed_at: string | null;
  created_at: string;
}
import { TestStatus } from '../../../shared/models/test-status';

export interface TestRun {
  id: string;
  run_id: string;
  project_id: string;
  test_suite_id: string;
  software_version: string;
  status: TestStatus;
  started_at: string;
  completed_at: string | null;
  created_at: string;
}

export interface CreateTestRunRequest {
  project_id: string;
  test_suite_id: string;
  software_version: string;
}

export interface TestRunFilters {
  project_id?: string;
  status?: TestStatus;
  software_version?: string;
  date_from?: string;
  date_to?: string;
}
import { TestStatus } from '../../../shared/models/test-status';

export interface TestResult {
  id: string;
  test_run_id: string;
  test_name: string;
  status: TestStatus;
  duration_ms: number;
  timestamp: string;
  error_message: string | null;
  measurements: Record<string, unknown> | null;
}
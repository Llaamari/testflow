export interface TestSuite {
  id: string;
  project_id: string;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTestSuiteRequest {
  name: string;
  description: string;
}
export interface ImportSummary {
  imported_count: number;
  run_status: 'PASSED' | 'FAILED' | 'ERROR' | 'PENDING';
}

export interface ImportValidationDetail {
  row?: number;
  field: string | null;
  message: string;
}

export interface ImportApiError {
  error: {
    code: string;
    message: string;
    details?: ImportValidationDetail[];
  };
}
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateTestRunRequest,
  TestRun,
} from '../models/test-run';
import { TestRunService } from './test-run';

describe('TestRunService', () => {
  let service: TestRunService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(TestRunService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should load test runs', () => {
    const runs: TestRun[] = [];

    service.getRuns().subscribe((result) => {
      expect(result).toEqual(runs);
    });

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs`,
    );

    expect(request.request.method).toBe('GET');

    request.flush(runs);
  });

  it('should send filters as query parameters', () => {
    service.getRuns({
      status: 'FAILED',
      software_version: '2.4.0',
    }).subscribe();

    const request = httpTesting.expectOne(
      (request) =>
        request.url === `${API_BASE_URL}/test-runs`
        && request.params.get('status') === 'FAILED'
        && request.params.get('software_version') === '2.4.0',
    );

    expect(request.request.method).toBe('GET');

    request.flush([]);
  });

  it('should create a test run', () => {
    const payload: CreateTestRunRequest = {
      project_id: 'project-1',
      test_suite_id: 'suite-1',
      software_version: '2.4.0',
    };

    service.createRun(payload).subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs`,
    );

    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);

    request.flush({
      id: 'run-1',
      run_id: 'RUN-20260816',
      ...payload,
      status: 'PENDING',
      started_at: '2026-08-16T10:00:00Z',
      completed_at: null,
      created_at: '2026-08-16T10:00:00Z',
    });
  });

  it('should load a test run by id', () => {
    service.getRun('run-1').subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs/run-1`,
    );

    expect(request.request.method).toBe('GET');

    request.flush({
      id: 'run-1',
      run_id: 'RUN-1',
      project_id: 'project-1',
      test_suite_id: 'suite-1',
      software_version: '2.4.0',
      status: 'PASSED',
      started_at: '2026-08-16T10:00:00Z',
      completed_at: null,
      created_at: '2026-08-16T10:00:00Z',
    });
  });


  it('should load results for a test run', () => {
    service.getResults('run-1').subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs/run-1/results`,
    );

    expect(request.request.method).toBe('GET');

    request.flush([]);
  });
});
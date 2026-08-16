import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { API_BASE_URL } from '../../../core/api/api.config';
import { ResultImportService } from './result-import';

describe('ResultImportService', () => {
  let service: ResultImportService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(ResultImportService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should import JSON results', () => {
    const payload = {
      results: [
        {
          test_name: 'test_one',
          status: 'PASSED',
          duration_ms: 100,
        },
      ],
    };

    service
      .importJson('run-1', payload)
      .subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs/run-1/results/import/json`,
    );

    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);

    request.flush({
      imported_count: 1,
      run_status: 'PASSED',
    });
  });

  it('should import a Parquet file', () => {
    const file = new File(
      ['test'],
      'results.parquet',
    );

    service
      .importParquet('run-1', file)
      .subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-runs/run-1/results/import/parquet`,
    );

    expect(request.request.method).toBe('POST');
    expect(
      request.request.body instanceof FormData,
    ).toBe(true);

    request.flush({
      imported_count: 1,
      run_status: 'PASSED',
    });
  });
});
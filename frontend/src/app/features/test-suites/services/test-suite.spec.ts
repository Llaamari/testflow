import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateTestSuiteRequest,
  TestSuite,
} from '../models/test-suite';
import { TestSuiteService } from './test-suite';

describe('TestSuiteService', () => {
  let service: TestSuiteService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(TestSuiteService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should load suites for a project', () => {
    const suites: TestSuite[] = [
      {
        id: 'suite-1',
        project_id: 'project-1',
        name: 'Navigation Tests',
        description: 'Fictional suite.',
        created_at: '2026-08-16T09:00:00Z',
        updated_at: '2026-08-16T09:00:00Z',
      },
    ];

    service
      .getSuitesForProject('project-1')
      .subscribe((result) => {
        expect(result).toEqual(suites);
      });

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/projects/project-1/test-suites`,
    );

    expect(request.request.method).toBe('GET');

    request.flush(suites);
  });

  it('should create a test suite', () => {
    const payload: CreateTestSuiteRequest = {
      name: 'Sensor Tests',
      description: 'Fictional suite.',
    };

    service
      .createSuite('project-1', payload)
      .subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/projects/project-1/test-suites`,
    );

    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);

    request.flush({
      id: 'suite-2',
      project_id: 'project-1',
      ...payload,
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T09:00:00Z',
    });
  });

  it('should update a test suite', () => {
    const payload: CreateTestSuiteRequest = {
      name: 'Updated Navigation Tests',
      description: 'Updated description.',
    };

    service
      .updateSuite('suite-1', payload)
      .subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-suites/suite-1`,
    );

    expect(request.request.method).toBe('PATCH');
    expect(request.request.body).toEqual(payload);

    request.flush({
      id: 'suite-1',
      project_id: 'project-1',
      ...payload,
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T10:00:00Z',
    });
  });

  it('should delete a test suite', () => {
    service
      .deleteSuite('suite-1')
      .subscribe();

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/test-suites/suite-1`,
    );

    expect(request.request.method).toBe('DELETE');

    request.flush(null);
  });
});
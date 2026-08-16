import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateTestRunRequest,
  TestRun,
  TestRunFilters,
} from '../models/test-run';
import { TestResult } from '../models/test-result';

@Injectable({
  providedIn: 'root',
})
export class TestRunService {
  private readonly http = inject(HttpClient);

  getRuns(
    filters: TestRunFilters = {},
  ): Observable<TestRun[]> {
    let params = new HttpParams();

    if (filters.project_id) {
      params = params.set(
        'project_id',
        filters.project_id,
      );
    }

    if (filters.status) {
      params = params.set(
        'status',
        filters.status,
      );
    }

    if (filters.software_version) {
      params = params.set(
        'software_version',
        filters.software_version,
      );
    }

    if (filters.date_from) {
      params = params.set(
        'date_from',
        filters.date_from,
      );
    }

    if (filters.date_to) {
      params = params.set(
        'date_to',
        filters.date_to,
      );
    }

    return this.http.get<TestRun[]>(
      `${API_BASE_URL}/test-runs`,
      { params },
    );
  }

  createRun(
    request: CreateTestRunRequest,
  ): Observable<TestRun> {
    return this.http.post<TestRun>(
      `${API_BASE_URL}/test-runs`,
      request,
    );
  }

  getRun(
    testRunId: string,
  ): Observable<TestRun> {
    return this.http.get<TestRun>(
      `${API_BASE_URL}/test-runs/${testRunId}`,
    );
  }

  deleteRun(
    testRunId: string,
  ): Observable<void> {
    return this.http.delete<void>(
      `${API_BASE_URL}/test-runs/${testRunId}`,
    );
  }

  getResults(
    testRunId: string,
  ): Observable<TestResult[]> {
    return this.http.get<TestResult[]>(
      `${API_BASE_URL}/test-runs/${testRunId}/results`,
    );
  }
}
import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateTestSuiteRequest,
  TestSuite,
} from '../models/test-suite';

@Injectable({
  providedIn: 'root',
})
export class TestSuiteService {
  private readonly http = inject(HttpClient);

  getSuitesForProject(
    projectId: string,
  ): Observable<TestSuite[]> {
    return this.http.get<TestSuite[]>(
      `${API_BASE_URL}/projects/${projectId}/test-suites`,
    );
  }

  createSuite(
    projectId: string,
    request: CreateTestSuiteRequest,
  ): Observable<TestSuite> {
    return this.http.post<TestSuite>(
      `${API_BASE_URL}/projects/${projectId}/test-suites`,
      request,
    );
  }

  updateSuite(
    suiteId: string,
    request: CreateTestSuiteRequest,
  ): Observable<TestSuite> {
    return this.http.patch<TestSuite>(
      `${API_BASE_URL}/test-suites/${suiteId}`,
      request,
    );
  }

  deleteSuite(
    suiteId: string,
  ): Observable<void> {
    return this.http.delete<void>(
      `${API_BASE_URL}/test-suites/${suiteId}`,
    );
  }
}
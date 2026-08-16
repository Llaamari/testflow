import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../../core/api/api.config';
import { ImportSummary } from '../models/import-result';

@Injectable({
  providedIn: 'root',
})
export class ResultImportService {
  private readonly http = inject(HttpClient);

  importJson(
    testRunId: string,
    payload: unknown,
  ): Observable<ImportSummary> {
    return this.http.post<ImportSummary>(
      `${API_BASE_URL}/test-runs/${testRunId}/results/import/json`,
      payload,
    );
  }

  importParquet(
    testRunId: string,
    file: File,
  ): Observable<ImportSummary> {
    const formData = new FormData();

    formData.append('file', file);

    return this.http.post<ImportSummary>(
      `${API_BASE_URL}/test-runs/${testRunId}/results/import/parquet`,
      formData,
    );
  }
}
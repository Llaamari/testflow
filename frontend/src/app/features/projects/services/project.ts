import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateProjectRequest,
  Project,
} from '../models/project';

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private readonly http = inject(HttpClient);

  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(
      `${API_BASE_URL}/projects`,
    );
  }

  createProject(
    request: CreateProjectRequest,
  ): Observable<Project> {
    return this.http.post<Project>(
      `${API_BASE_URL}/projects`,
      request,
    );
  }

  updateProject(
    projectId: string,
    request: CreateProjectRequest,
  ): Observable<Project> {
    return this.http.patch<Project>(
      `${API_BASE_URL}/projects/${projectId}`,
      request,
    );
  }

  deleteProject(
    projectId: string,
  ): Observable<void> {
    return this.http.delete<void>(
      `${API_BASE_URL}/projects/${projectId}`,
    );
  }
}
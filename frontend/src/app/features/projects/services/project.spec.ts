import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

import { API_BASE_URL } from '../../../core/api/api.config';
import {
  CreateProjectRequest,
  Project,
} from '../models/project';
import { ProjectService } from './project';

describe('ProjectService', () => {
  let service: ProjectService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(ProjectService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should load projects', () => {
    const projects: Project[] = [
      {
        id: 'project-1',
        name: 'Autonomous Drone Control System',
        description: 'Fictional project.',
        created_at: '2026-08-16T09:00:00Z',
        updated_at: '2026-08-16T09:00:00Z',
      },
    ];

    service.getProjects().subscribe((result) => {
      expect(result).toEqual(projects);
    });

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/projects`,
    );

    expect(request.request.method).toBe('GET');

    request.flush(projects);
  });

  it('should create a project', () => {
    const payload: CreateProjectRequest = {
      name: 'Smart Greenhouse Monitoring Platform',
      description: 'Fictional project.',
    };

    const createdProject: Project = {
      id: 'project-2',
      ...payload,
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T09:00:00Z',
    };

    service.createProject(payload).subscribe((result) => {
      expect(result).toEqual(createdProject);
    });

    const request = httpTesting.expectOne(
      `${API_BASE_URL}/projects`,
    );

    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);

    request.flush(createdProject);
  });

  it('should update a project', () => {
    const payload: CreateProjectRequest = {
        name: 'Updated Project',
        description: 'Updated description.',
    };

    const updatedProject: Project = {
        id: 'project-1',
        ...payload,
        created_at: '2026-08-16T09:00:00Z',
        updated_at: '2026-08-16T10:00:00Z',
    };

    service.updateProject(
        'project-1',
        payload,
    ).subscribe((result) => {
        expect(result).toEqual(updatedProject);
    });

    const request = httpTesting.expectOne(
        `${API_BASE_URL}/projects/project-1`,
    );

    expect(request.request.method).toBe('PATCH');
    expect(request.request.body).toEqual(payload);

    request.flush(updatedProject);
    });


    it('should delete a project', () => {
        service.deleteProject(
            'project-1',
        ).subscribe();

        const request = httpTesting.expectOne(
            `${API_BASE_URL}/projects/project-1`,
        );

        expect(request.request.method).toBe('DELETE');

        request.flush(null);
    });
});
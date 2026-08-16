import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Project } from '../../../projects/models/project';
import { ProjectService } from '../../../projects/services/project';
import { TestSuiteService } from '../../../test-suites/services/test-suite';
import { TestRun } from '../../models/test-run';
import { TestRunService } from '../../services/test-run';
import { TestRunListPage } from './test-run-list-page';

describe('TestRunListPage', () => {
  let component: TestRunListPage;
  let fixture: ComponentFixture<TestRunListPage>;

  const projects: Project[] = [
    {
      id: 'project-1',
      name: 'Autonomous Drone Control System',
      description: 'Fictional project.',
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T09:00:00Z',
    },
  ];

  const runs: TestRun[] = [
    {
      id: 'run-1',
      run_id: 'RUN-20260816',
      project_id: 'project-1',
      test_suite_id: 'suite-1',
      software_version: '2.4.0',
      status: 'PENDING',
      started_at: '2026-08-16T10:00:00Z',
      completed_at: null,
      created_at: '2026-08-16T10:00:00Z',
    },
  ];

  const projectServiceMock = {
    getProjects: () => of(projects),
  };

  const testRunServiceMock = {
    getRuns: () => of(runs),
    createRun: () => of(runs[0]),
  };

  const testSuiteServiceMock = {
    getSuitesForProject: () => of([]),
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestRunListPage],
      providers: [
        provideRouter([]),
        {
          provide: ProjectService,
          useValue: projectServiceMock,
        },
        {
          provide: TestRunService,
          useValue: testRunServiceMock,
        },
        {
          provide: TestSuiteService,
          useValue: testSuiteServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(
      TestRunListPage,
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load test runs', () => {
    expect(component.runs()).toEqual(runs);
    expect(component.loading()).toBe(false);
  });

  it('should load projects', () => {
    expect(component.projects()).toEqual(projects);
  });
});
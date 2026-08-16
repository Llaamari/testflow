import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

import { ProjectDetailsPage } from './project-details-page';
import { ProjectService } from '../../services/project';
import { TestSuiteService } from '../../../test-suites/services/test-suite';
import { Project } from '../../models/project';
import { TestSuite } from '../../../test-suites/models/test-suite';

describe('ProjectDetailsPage', () => {
  let component: ProjectDetailsPage;
  let fixture: ComponentFixture<ProjectDetailsPage>;

  const project: Project = {
    id: 'project-1',
    name: 'Autonomous Drone Control System',
    description: 'Fictional project.',
    created_at: '2026-08-16T09:00:00Z',
    updated_at: '2026-08-16T09:00:00Z',
  };

  const suites: TestSuite[] = [
    {
      id: 'suite-1',
      project_id: 'project-1',
      name: 'Navigation Tests',
      description: 'Fictional test suite.',
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T09:00:00Z',
    },
  ];

  const projectServiceMock = {
    getProject: () => of(project),
  };

  const testSuiteServiceMock = {
    getSuitesForProject: () => of(suites),
    createSuite: () => of(suites[0]),
  };

  const activatedRouteMock = {
    snapshot: {
      paramMap: {
        get: (key: string) => {
          return key === 'id' ? 'project-1' : null;
        },
      },
    },
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectDetailsPage],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: activatedRouteMock,
        },
        {
          provide: ProjectService,
          useValue: projectServiceMock,
        },
        {
          provide: TestSuiteService,
          useValue: testSuiteServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ProjectDetailsPage);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load the project', () => {
    expect(component.project()).toEqual(project);
    expect(component.loading()).toBe(false);
  });

  it('should load test suites', () => {
    expect(component.suites()).toEqual(suites);
  });

  it('should render project details', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.textContent).toContain(
      'Autonomous Drone Control System',
    );

    expect(element.textContent).toContain(
      'Navigation Tests',
    );
  });
});
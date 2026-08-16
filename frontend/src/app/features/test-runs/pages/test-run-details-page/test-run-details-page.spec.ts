import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

import { TestRunDetailsPage } from './test-run-details-page';
import { TestRunService } from '../../services/test-run';
import { TestRun } from '../../models/test-run';
import { TestResult } from '../../models/test-result';

describe('TestRunDetailsPage', () => {
  let component: TestRunDetailsPage;
  let fixture: ComponentFixture<TestRunDetailsPage>;

  const run: TestRun = {
    id: 'run-1',
    run_id: 'RUN-20260816',
    project_id: 'project-1',
    test_suite_id: 'suite-1',
    software_version: '2.4.0',
    status: 'FAILED',
    started_at: '2026-08-16T10:00:00Z',
    completed_at: null,
    created_at: '2026-08-16T10:00:00Z',
  };

  const results: TestResult[] = [
    {
      id: 'result-1',
      test_run_id: 'run-1',
      test_name: 'waypoint_navigation',
      status: 'FAILED',
      duration_ms: 120,
      timestamp: '2026-08-16T10:01:00Z',
      error_message: 'Fictional failure.',
      measurements: null,
    },
  ];

  const testRunServiceMock = {
    getRun: () => of(run),
    getResults: () => of(results),
  };

  const activatedRouteMock = {
    snapshot: {
      paramMap: {
        get: (key: string) =>
          key === 'id' ? 'run-1' : null,
      },
    },
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestRunDetailsPage],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: activatedRouteMock,
        },
        {
          provide: TestRunService,
          useValue: testRunServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(
      TestRunDetailsPage,
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load test run and results', () => {
    expect(component.run()).toEqual(run);
    expect(component.results()).toEqual(results);
  });

  it('should render the test run', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.textContent).toContain(
      'RUN-20260816',
    );

    expect(element.textContent).toContain(
      'waypoint_navigation',
    );
  });
});
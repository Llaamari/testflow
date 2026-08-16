import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';
import { of } from 'rxjs';

import { TestRun } from '../../../test-runs/models/test-run';
import { TestRunService } from '../../../test-runs/services/test-run';
import { ResultImportService } from '../../services/result-import';
import { ImportResultsPage } from './import-results-page';

describe('ImportResultsPage', () => {
  let component: ImportResultsPage;
  let fixture: ComponentFixture<ImportResultsPage>;

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

  const testRunServiceMock = {
    getRuns: () => of(runs),
  };

  const importServiceMock = {
    importJson: () =>
      of({
        imported_count: 1,
        run_status: 'PASSED',
      }),
    importParquet: () =>
      of({
        imported_count: 1,
        run_status: 'PASSED',
      }),
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportResultsPage],
      providers: [
        {
          provide: TestRunService,
          useValue: testRunServiceMock,
        },
        {
          provide: ResultImportService,
          useValue: importServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(
      ImportResultsPage,
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load test runs', () => {
    expect(component.runs()).toEqual(runs);
    expect(component.loadingRuns()).toBe(false);
  });
});
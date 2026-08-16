import { DatePipe } from '@angular/common';
import {
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { Project } from '../../../projects/models/project';
import { ProjectService } from '../../../projects/services/project';
import { TestSuite } from '../../../test-suites/models/test-suite';
import { TestSuiteService } from '../../../test-suites/services/test-suite';
import { StatusBadge } from '../../../../shared/components/status-badge/status-badge';
import { TestStatus } from '../../../../shared/models/test-status';
import { TestRun } from '../../models/test-run';
import { TestRunService } from '../../services/test-run';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-test-run-list-page',
  imports: [
    DatePipe,
    ReactiveFormsModule,
    StatusBadge,
    RouterLink,
  ],
  templateUrl: './test-run-list-page.html',
  styleUrl: './test-run-list-page.css',
})
export class TestRunListPage implements OnInit {
  private readonly testRunService = inject(TestRunService);
  private readonly projectService = inject(ProjectService);
  private readonly testSuiteService = inject(TestSuiteService);
  private readonly formBuilder = inject(FormBuilder);

  readonly runs = signal<TestRun[]>([]);
  readonly projects = signal<Project[]>([]);
  readonly suites = signal<TestSuite[]>([]);

  readonly loading = signal(true);
  readonly creating = signal(false);
  readonly errorMessage = signal<string | null>(null);

  readonly statuses: TestStatus[] = [
    'PASSED',
    'FAILED',
    'ERROR',
    'PENDING',
  ];

  readonly filterForm = this.formBuilder.nonNullable.group({
    project_id: [''],
    status: [''],
    software_version: [''],
  });

  readonly runForm = this.formBuilder.nonNullable.group({
    project_id: ['', Validators.required],

    test_suite_id: [
      {
        value: '',
        disabled: true,
      },
      Validators.required,
    ],

    software_version: [
      '',
      Validators.required,
    ],
  });

  ngOnInit(): void {
    this.loadProjects();
    this.loadRuns();
  }

  applyFilters(): void {
    const filters = this.filterForm.getRawValue();

    this.loadRuns({
      project_id: filters.project_id || undefined,
      status: (
        filters.status
          ? filters.status as TestStatus
          : undefined
      ),
      software_version:
        filters.software_version || undefined,
    });
  }

  clearFilters(): void {
    this.filterForm.reset({
      project_id: '',
      status: '',
      software_version: '',
    });

    this.loadRuns();
  }

  onRunProjectChange(): void {
    const projectId =
      this.runForm.controls.project_id.value;

    const suiteControl =
      this.runForm.controls.test_suite_id;

    suiteControl.reset('');
    suiteControl.disable();

    if (!projectId) {
      this.suites.set([]);
      return;
    }

    this.testSuiteService
      .getSuitesForProject(projectId)
      .subscribe({
        next: (suites) => {
          this.suites.set(suites);

          if (suites.length > 0) {
            suiteControl.enable();
          }
        },
        error: (error) => {
          console.error(
            'Test suites request failed:',
            error,
          );

          this.suites.set([]);

          this.errorMessage.set(
            'Test suites could not be loaded.',
          );
        },
      });
  }

  createRun(): void {
    if (this.runForm.invalid) {
      this.runForm.markAllAsTouched();
      return;
    }

    this.creating.set(true);
    this.errorMessage.set(null);

    this.testRunService
      .createRun(
        this.runForm.getRawValue(),
      )
      .subscribe({
        next: (run) => {
          this.runs.update(
            (runs) => [run, ...runs],
          );

          this.runForm.reset({
            project_id: '',
            test_suite_id: '',
            software_version: '',
          });
          
          this.runForm.controls.test_suite_id.disable();
          
          this.suites.set([]);
          this.creating.set(false);
        },
        error: (error) => {
          console.error(
            'Test run creation failed:',
            error,
          );

          this.errorMessage.set(
            'Test run could not be created.',
          );

          this.creating.set(false);
        },
      });
  }

  private loadProjects(): void {
    this.projectService.getProjects().subscribe({
      next: (projects) => {
        this.projects.set(projects);
      },
      error: (error) => {
        console.error(
          'Projects request failed:',
          error,
        );

        this.errorMessage.set(
          'Projects could not be loaded.',
        );
      },
    });
  }

  private loadRuns(
    filters: {
      project_id?: string;
      status?: TestStatus;
      software_version?: string;
    } = {},
  ): void {
    this.loading.set(true);
    this.errorMessage.set(null);

    this.testRunService
      .getRuns(filters)
      .subscribe({
        next: (runs) => {
          this.runs.set(runs);
          this.loading.set(false);
        },
        error: (error) => {
          console.error(
            'Test runs request failed:',
            error,
          );

          this.errorMessage.set(
            'Test runs could not be loaded.',
          );

          this.loading.set(false);
        },
      });
  }
}
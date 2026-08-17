import {
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { Project } from '../../models/project';
import { ProjectService } from '../../services/project';
import { TestSuite } from '../../../test-suites/models/test-suite';
import { TestSuiteService } from '../../../test-suites/services/test-suite';
import { getApiErrorMessage } from '../../../../core/api/api-error';

@Component({
  selector: 'app-project-details-page',
  imports: [
    DatePipe,
    RouterLink,
    ReactiveFormsModule,
  ],
  templateUrl: './project-details-page.html',
  styleUrl: './project-details-page.css',
})
export class ProjectDetailsPage implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly projectService = inject(ProjectService);
  private readonly testSuiteService = inject(TestSuiteService);
  private readonly formBuilder = inject(FormBuilder);

  readonly project = signal<Project | null>(null);
  readonly suites = signal<TestSuite[]>([]);

  readonly loading = signal(true);
  readonly savingSuite = signal(false);
  readonly errorMessage = signal<string | null>(null);

  readonly editingSuiteId = signal<string | null>(null);
  readonly deletingSuiteId = signal<string | null>(null);
  readonly savingEditedSuite = signal(false);

  readonly suiteForm = this.formBuilder.nonNullable.group({
    name: [
      '',
      [
        Validators.required,
        Validators.maxLength(120),
      ],
    ],
    description: [
      '',
      [
        Validators.maxLength(500),
      ],
    ],
  });

  readonly editSuiteForm = this.formBuilder.nonNullable.group({
    name: [
      '',
      [
        Validators.required,
        Validators.maxLength(120),
      ],
    ],
    description: [
      '',
      [
        Validators.maxLength(500),
      ],
    ],
  });

  ngOnInit(): void {
    const projectId = this.route.snapshot.paramMap.get('id');

    if (!projectId) {
      this.errorMessage.set('Project ID is missing.');
      this.loading.set(false);
      return;
    }

    this.loadProject(projectId);
    this.loadSuites(projectId);
  }

  createSuite(): void {
    const project = this.project();

    if (!project) {
      return;
    }

    if (this.suiteForm.invalid) {
      this.suiteForm.markAllAsTouched();
      return;
    }

    this.savingSuite.set(true);
    this.errorMessage.set(null);

    this.testSuiteService
      .createSuite(
        project.id,
        this.suiteForm.getRawValue(),
      )
      .subscribe({
        next: (suite) => {
          this.suites.update(
            (suites) => [suite, ...suites],
          );

          this.suiteForm.reset({
            name: '',
            description: '',
          });

          this.savingSuite.set(false);
        },
        error: (error) => {
          console.error('Test suite creation failed:', error);

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Test suite could not be created.',
            ),
          );

          this.savingSuite.set(false);
        },
      });
  }

  startEditingSuite(suite: TestSuite): void {
    this.editingSuiteId.set(suite.id);

    this.editSuiteForm.setValue({
      name: suite.name,
      description: suite.description,
    });
  }

  cancelEditingSuite(): void {
    this.editingSuiteId.set(null);

    this.editSuiteForm.reset({
      name: '',
      description: '',
    });
  }

  saveSuite(suiteId: string): void {
    if (this.editSuiteForm.invalid) {
      this.editSuiteForm.markAllAsTouched();
      return;
    }

    this.savingEditedSuite.set(true);
    this.errorMessage.set(null);

    this.testSuiteService
      .updateSuite(
        suiteId,
        this.editSuiteForm.getRawValue(),
      )
      .subscribe({
        next: (updatedSuite) => {
          this.suites.update((suites) =>
            suites.map((suite) =>
              suite.id === updatedSuite.id
                ? updatedSuite
                : suite,
            ),
          );

          this.editingSuiteId.set(null);
          this.savingEditedSuite.set(false);
        },
        error: (error) => {
          console.error(
            'Test suite update failed:',
            error,
          );

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Test suite could not be updated.',
            )
          );

          this.savingEditedSuite.set(false);
        },
      });
  }

  deleteSuite(suiteId: string): void {
    const confirmed = window.confirm(
      'Delete this test suite? This action cannot be undone.',
    );

    if (!confirmed) {
      return;
    }

    this.deletingSuiteId.set(suiteId);
    this.errorMessage.set(null);

    this.testSuiteService
      .deleteSuite(suiteId)
      .subscribe({
        next: () => {
          this.suites.update((suites) =>
            suites.filter(
              (suite) => suite.id !== suiteId,
            ),
          );

          this.deletingSuiteId.set(null);
        },
        error: (error) => {
          console.error(
            'Test suite deletion failed:',
            error,
          );

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Test suite could not be deleted.',
            )
          );

          this.deletingSuiteId.set(null);
        },
      });
  }

  private loadProject(projectId: string): void {
    this.projectService.getProject(projectId).subscribe({
      next: (project) => {
        this.project.set(project);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Project request failed:', error);

        this.errorMessage.set(
          getApiErrorMessage(
            error,
            'Project could not be loaded.',
          )
        );

        this.loading.set(false);
      },
    });
  }

  private loadSuites(projectId: string): void {
    this.testSuiteService
      .getSuitesForProject(projectId)
      .subscribe({
        next: (suites) => {
          this.suites.set(suites);
        },
        error: (error) => {
          console.error('Test suites request failed:', error);

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Test suites could not be loaded.',
            )
          );
        },
      });
  }
}
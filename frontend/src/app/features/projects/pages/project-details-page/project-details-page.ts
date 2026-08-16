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
            'Test suite could not be created.',
          );

          this.savingSuite.set(false);
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
          'Project could not be loaded.',
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
            'Test suites could not be loaded.',
          );
        },
      });
  }
}
import {
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { DatePipe } from '@angular/common';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { Project } from '../../models/project';
import { ProjectService } from '../../services/project';
import { RouterLink } from '@angular/router';
import { getApiErrorMessage } from '../../../../core/api/api-error';

@Component({
  selector: 'app-project-list-page',
  imports: [
    DatePipe,
    ReactiveFormsModule,
    RouterLink,
  ],
  templateUrl: './project-list-page.html',
  styleUrl: './project-list-page.css',
})
export class ProjectListPage implements OnInit {
  private readonly projectService = inject(ProjectService);
  private readonly formBuilder = inject(FormBuilder);

  readonly projects = signal<Project[]>([]);

  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly errorMessage = signal<string | null>(null);

  readonly editingProjectId = signal<string | null>(null);
  readonly deletingProjectId = signal<string | null>(null);

  readonly projectForm = this.formBuilder.nonNullable.group({
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

  readonly editForm = this.formBuilder.nonNullable.group({
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
    this.loadProjects();
  }

  createProject(): void {
    if (this.projectForm.invalid) {
      this.projectForm.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    this.errorMessage.set(null);

    const request = this.projectForm.getRawValue();

    this.projectService.createProject(request).subscribe({
      next: (project) => {
        this.projects.update(
          (projects) => [project, ...projects],
        );

        this.projectForm.reset({
          name: '',
          description: '',
        });

        this.saving.set(false);
      },
      error: (error) => {
        console.error('Project creation failed:', error);

        this.errorMessage.set(
          getApiErrorMessage(
            error,
            'Project could not be created.',
          ),
        );

        this.saving.set(false);
      },
    });
  }

  startEditing(project: Project): void {
    this.editingProjectId.set(project.id);

    this.editForm.setValue({
      name: project.name,
      description: project.description,
    });
  }

  cancelEditing(): void {
    this.editingProjectId.set(null);

    this.editForm.reset({
      name: '',
      description: '',
    });
  }

  saveProject(projectId: string): void {
    if (this.editForm.invalid) {
      this.editForm.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    this.errorMessage.set(null);

    this.projectService
      .updateProject(
        projectId,
        this.editForm.getRawValue(),
      )
      .subscribe({
        next: (updatedProject) => {
          this.projects.update((projects) =>
            projects.map((project) =>
              project.id === updatedProject.id
                ? updatedProject
                : project,
            ),
          );

          this.editingProjectId.set(null);
          this.saving.set(false);
        },
        error: (error) => {
          console.error('Project update failed:', error);

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Project could not be updated.',
            ),
          );

          this.saving.set(false);
        },
      });
  }

  deleteProject(projectId: string): void {
    const confirmed = window.confirm(
      'Delete this project? This action cannot be undone.',
    );

    if (!confirmed) {
      return;
    }

    this.deletingProjectId.set(projectId);
    this.errorMessage.set(null);

    this.projectService
      .deleteProject(projectId)
      .subscribe({
        next: () => {
          this.projects.update((projects) =>
            projects.filter(
              (project) => project.id !== projectId,
            ),
          );

          this.deletingProjectId.set(null);
        },
        error: (error) => {
          console.error(
            'Project deletion failed:',
            error,
          );

          this.errorMessage.set(
            getApiErrorMessage(
              error,
              'Project could not be deleted.',
            ),
          );

          this.deletingProjectId.set(null);
        },
      });
  }

  private loadProjects(): void {
    this.loading.set(true);
    this.errorMessage.set(null);

    this.projectService.getProjects().subscribe({
      next: (projects) => {
        this.projects.set(projects);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Projects request failed:', error);

        this.errorMessage.set(
          getApiErrorMessage(
            error,
            'Projects could not be loaded.',
          ),
        );

        this.loading.set(false);
      },
    });
  }
}
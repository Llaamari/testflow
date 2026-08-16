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

import { Project } from '../../models/project';
import { ProjectService } from '../../services/project';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-project-list-page',
  imports: [
    DatePipe,
    ReactiveFormsModule
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
          'Project could not be created.',
        );

        this.saving.set(false);
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
          'Projects could not be loaded.',
        );

        this.loading.set(false);
      },
    });
  }
}
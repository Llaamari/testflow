import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Project } from '../../models/project';
import { ProjectService } from '../../services/project';
import { ProjectListPage } from './project-list-page';

describe('ProjectListPage', () => {
  let component: ProjectListPage;
  let fixture: ComponentFixture<ProjectListPage>;

  const projects: Project[] = [
    {
      id: 'project-1',
      name: 'Autonomous Drone Control System',
      description: 'Fictional project.',
      created_at: '2026-08-16T09:00:00Z',
      updated_at: '2026-08-16T09:00:00Z',
    },
  ];

  const projectServiceMock = {
    getProjects: () => of(projects),
    createProject: () => of(projects[0]),
    updateProject: () => of(projects[0]),
    deleteProject: () => of(undefined),
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectListPage],
      providers: [
        provideRouter([]),
        {
          provide: ProjectService,
          useValue: projectServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ProjectListPage);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load projects', () => {
    expect(component.projects()).toEqual(projects);
    expect(component.loading()).toBe(false);
  });

  it('should render project name', () => {
    const element: HTMLElement =
      fixture.nativeElement;

    expect(element.textContent).toContain(
      'Autonomous Drone Control System',
    );
  });
});
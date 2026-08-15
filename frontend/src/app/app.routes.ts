import { Routes } from '@angular/router';

import { DashboardPage } from './features/dashboard/pages/dashboard-page/dashboard-page';
import { ImportResultsPage } from './features/import-results/pages/import-results-page/import-results-page';
import { ProjectListPage } from './features/projects/pages/project-list-page/project-list-page';
import { TestRunListPage } from './features/test-runs/pages/test-run-list-page/test-run-list-page';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'dashboard',
  },
  {
    path: 'dashboard',
    component: DashboardPage,
  },
  {
    path: 'projects',
    component: ProjectListPage,
  },
  {
    path: 'test-runs',
    component: TestRunListPage,
  },
  {
    path: 'import',
    component: ImportResultsPage,
  },
  {
    path: '**',
    redirectTo: 'dashboard',
  },
];
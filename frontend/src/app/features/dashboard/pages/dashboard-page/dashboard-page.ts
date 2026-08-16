import { Component, inject, OnInit, signal } from '@angular/core';

import { StatisticsCard } from '../../../../shared/components/statistics-card/statistics-card';
import { DashboardStats } from '../../models/dashboard-stats';
import { DashboardService } from '../../services/dashboard';
import { StatusBadge } from '../../../../shared/components/status-badge/status-badge';
import { DatePipe } from '@angular/common';
import { ErrorState } from '../../../../shared/components/error-state/error-state';
import { EmptyState } from '../../../../shared/components/empty-state/empty-state';
import { LoadingState } from '../../../../shared/components/loading-state/loading-state';

@Component({
  selector: 'app-dashboard-page',
  imports: [
    DatePipe,
    StatisticsCard,
    StatusBadge,
    LoadingState,
    EmptyState,
    ErrorState,
  ],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.css',
})
export class DashboardPage implements OnInit {
  private readonly dashboardService = inject(DashboardService);

  readonly stats = signal<DashboardStats | null>(null);
  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loadDashboard();
  }

  private loadDashboard(): void {
    this.loading.set(true);
    this.errorMessage.set(null);

    this.dashboardService.getStats().subscribe({
      next: (stats) => {
        this.stats.set(stats);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Dashboard request failed:', error);

        this.errorMessage.set(
          'Dashboard data could not be loaded.',
        );

        this.loading.set(false);
      },
    });
  }
}
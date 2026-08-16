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

  passedPercentage(stats: DashboardStats): number {
    return this.calculatePercentage(
      stats.status_distribution.PASSED,
      stats.test_results,
    );
  }

  failedPercentage(stats: DashboardStats): number {
    return this.calculatePercentage(
      stats.status_distribution.FAILED,
      stats.test_results,
    );
  }

  errorPercentage(stats: DashboardStats): number {
    return this.calculatePercentage(
      stats.status_distribution.ERROR,
      stats.test_results,
    );
  }

  pendingPercentage(stats: DashboardStats): number {
    return this.calculatePercentage(
      stats.status_distribution.PENDING,
      stats.test_results,
    );
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

  private calculatePercentage(
    value: number,
    total: number,
  ): number {
    if (total === 0) {
      return 0;
    }

    return Math.round(
      (value / total) * 1000,
    ) / 10;
  }
}
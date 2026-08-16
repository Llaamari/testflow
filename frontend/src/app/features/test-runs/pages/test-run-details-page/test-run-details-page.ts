import { DatePipe, JsonPipe } from '@angular/common';
import {
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { StatusBadge } from '../../../../shared/components/status-badge/status-badge';
import { TestResult } from '../../models/test-result';
import { TestRun } from '../../models/test-run';
import { TestRunService } from '../../services/test-run';

@Component({
  selector: 'app-test-run-details-page',
  imports: [
    DatePipe,
    JsonPipe,
    RouterLink,
    StatusBadge,
  ],
  templateUrl: './test-run-details-page.html',
  styleUrl: './test-run-details-page.css',
})
export class TestRunDetailsPage implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly testRunService = inject(TestRunService);

  readonly run = signal<TestRun | null>(null);
  readonly results = signal<TestResult[]>([]);

  readonly loading = signal(true);
  readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const testRunId = this.route.snapshot.paramMap.get('id');

    if (!testRunId) {
      this.errorMessage.set('Test run ID is missing.');
      this.loading.set(false);
      return;
    }

    this.loadRun(testRunId);
    this.loadResults(testRunId);
  }

  private loadRun(testRunId: string): void {
    this.testRunService.getRun(testRunId).subscribe({
      next: (run) => {
        this.run.set(run);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Test run request failed:', error);

        this.errorMessage.set(
          'Test run could not be loaded.',
        );

        this.loading.set(false);
      },
    });
  }

  private loadResults(testRunId: string): void {
    this.testRunService.getResults(testRunId).subscribe({
      next: (results) => {
        this.results.set(results);
      },
      error: (error) => {
        console.error(
          'Test results request failed:',
          error,
        );

        this.errorMessage.set(
          'Test results could not be loaded.',
        );
      },
    });
  }
}
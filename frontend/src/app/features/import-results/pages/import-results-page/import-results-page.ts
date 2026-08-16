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

import { StatusBadge } from '../../../../shared/components/status-badge/status-badge';
import { TestRun } from '../../../test-runs/models/test-run';
import { TestRunService } from '../../../test-runs/services/test-run';
import {
  ImportSummary,
  ImportValidationDetail,
} from '../../models/import-result';
import { ResultImportService } from '../../services/result-import';

@Component({
  selector: 'app-import-results-page',
  imports: [
    ReactiveFormsModule,
    StatusBadge,
  ],
  templateUrl: './import-results-page.html',
  styleUrl: './import-results-page.css',
})
export class ImportResultsPage implements OnInit {
  private readonly formBuilder = inject(FormBuilder);
  private readonly testRunService = inject(TestRunService);
  private readonly importService = inject(ResultImportService);

  readonly runs = signal<TestRun[]>([]);

  readonly loadingRuns = signal(true);
  readonly importing = signal(false);

  readonly selectedFile = signal<File | null>(null);

  readonly errorMessage = signal<string | null>(null);
  readonly validationErrors =
    signal<ImportValidationDetail[]>([]);

  readonly importSummary =
    signal<ImportSummary | null>(null);

  readonly importForm = this.formBuilder.nonNullable.group({
    test_run_id: ['', Validators.required],
    json_data: [''],
  });

  ngOnInit(): void {
    this.loadRuns();
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;

    this.selectedFile.set(file);
    this.clearMessages();
  }

  importJson(): void {
    const testRunId =
      this.importForm.controls.test_run_id.value;

    const jsonText =
      this.importForm.controls.json_data.value;

    if (!testRunId) {
      this.errorMessage.set(
        'Select a test run before importing results.',
      );
      return;
    }

    if (!jsonText.trim()) {
      this.errorMessage.set(
        'JSON data is required.',
      );
      return;
    }

    let payload: unknown;

    try {
      payload = JSON.parse(jsonText);
    } catch {
      this.errorMessage.set(
        'JSON data is not valid JSON.',
      );
      return;
    }

    this.startImport();

    this.importService
      .importJson(testRunId, payload)
      .subscribe({
        next: (summary) => {
          this.finishImport(summary);
        },
        error: (error) => {
          this.handleImportError(error);
        },
      });
  }

  importParquet(): void {
    const testRunId =
      this.importForm.controls.test_run_id.value;

    const file = this.selectedFile();

    if (!testRunId) {
      this.errorMessage.set(
        'Select a test run before importing results.',
      );
      return;
    }

    if (!file) {
      this.errorMessage.set(
        'Select a Parquet file first.',
      );
      return;
    }

    this.startImport();

    this.importService
      .importParquet(testRunId, file)
      .subscribe({
        next: (summary) => {
          this.finishImport(summary);
        },
        error: (error) => {
          this.handleImportError(error);
        },
      });
  }

  private loadRuns(): void {
    this.loadingRuns.set(true);

    this.testRunService.getRuns().subscribe({
      next: (runs) => {
        this.runs.set(runs);
        this.loadingRuns.set(false);
      },
      error: (error) => {
        console.error(
          'Test runs request failed:',
          error,
        );

        this.errorMessage.set(
          'Test runs could not be loaded.',
        );

        this.loadingRuns.set(false);
      },
    });
  }

  private startImport(): void {
    this.importing.set(true);
    this.clearMessages();
  }

  private finishImport(
    summary: ImportSummary,
  ): void {
    this.importSummary.set(summary);
    this.importing.set(false);
  }

  private handleImportError(error: any): void {
    console.error('Result import failed:', error);

    const response = error?.error;

    this.errorMessage.set(
      response?.error?.message
        ?? 'Results could not be imported.',
    );

    this.validationErrors.set(
      response?.error?.details ?? [],
    );

    this.importing.set(false);
  }

  private clearMessages(): void {
    this.errorMessage.set(null);
    this.validationErrors.set([]);
    this.importSummary.set(null);
  }
}
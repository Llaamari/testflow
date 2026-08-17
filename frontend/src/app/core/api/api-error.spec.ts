import { HttpErrorResponse } from '@angular/common/http';

import { getApiErrorMessage } from './api-error';

describe('getApiErrorMessage', () => {
  it('should return API error message', () => {
    const error = new HttpErrorResponse({
      status: 400,
      error: {
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid date range.',
        },
      },
    });

    expect(
      getApiErrorMessage(
        error,
        'Fallback message.',
      ),
    ).toBe('Invalid date range.');
  });

  it('should return fallback when API message is missing', () => {
    const error = new HttpErrorResponse({
      status: 500,
      error: {},
    });

    expect(
      getApiErrorMessage(
        error,
        'Fallback message.',
      ),
    ).toBe('Fallback message.');
  });

  it('should return fallback for unknown errors', () => {
    expect(
      getApiErrorMessage(
        new Error('Unknown'),
        'Fallback message.',
      ),
    ).toBe('Fallback message.');
  });
});
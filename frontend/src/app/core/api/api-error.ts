interface ApiErrorResponse {
  error?: {
    error?: {
      code?: string;
      message?: string;
    };
  };
}

export function getApiErrorMessage(
  error: unknown,
  fallbackMessage: string,
): string {
  if (
    typeof error !== 'object'
    || error === null
  ) {
    return fallbackMessage;
  }

  const response = error as ApiErrorResponse;

  return (
    response.error?.error?.message
    ?? fallbackMessage
  );
}
import { TestBed } from '@angular/core/testing';

import { ThemeService } from './theme';

describe('ThemeService', () => {
  beforeEach(() => {
    TestBed.resetTestingModule();

    document.documentElement.removeAttribute(
      'data-theme',
    );
  });

  it('should create', () => {
    const service = TestBed.inject(ThemeService);

    expect(service).toBeTruthy();
  });

  it('should toggle the theme', () => {
    const service = TestBed.inject(ThemeService);

    const initialTheme = service.theme();

    service.toggleTheme();

    const expectedTheme =
      initialTheme === 'light'
        ? 'dark'
        : 'light';

    expect(service.theme()).toBe(expectedTheme);

    expect(
      document.documentElement.getAttribute(
        'data-theme',
      ),
    ).toBe(expectedTheme);
  });
});
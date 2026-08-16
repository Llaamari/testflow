import {
  DOCUMENT,
  isPlatformBrowser,
} from '@angular/common';
import {
  inject,
  Injectable,
  PLATFORM_ID,
  signal,
} from '@angular/core';

export type Theme = 'light' | 'dark';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private readonly document = inject(DOCUMENT);
  private readonly platformId = inject(PLATFORM_ID);

  readonly theme = signal<Theme>(
    this.getInitialTheme(),
  );

  constructor() {
    this.applyTheme(this.theme());
  }

  toggleTheme(): void {
    const nextTheme: Theme =
      this.theme() === 'light'
        ? 'dark'
        : 'light';

    this.theme.set(nextTheme);
    this.applyTheme(nextTheme);

    if (this.isBrowser()) {
      this.getStorage()?.setItem(
        'testflow-theme',
        nextTheme,
      );
    }
  }

  private getInitialTheme(): Theme {
    if (!this.isBrowser()) {
      return 'light';
    }

    const storedTheme =
      this.getStorage()?.getItem('testflow-theme');

    if (
      storedTheme === 'light'
      || storedTheme === 'dark'
    ) {
      return storedTheme;
    }

    if (
      typeof window.matchMedia === 'function'
      && window.matchMedia(
        '(prefers-color-scheme: dark)',
      ).matches
    ) {
      return 'dark';
    }

    return 'light';
  }

  private applyTheme(theme: Theme): void {
    this.document.documentElement.setAttribute(
      'data-theme',
      theme,
    );
  }

  private isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  private getStorage(): Storage | null {
    if (
      typeof localStorage === 'undefined'
      || typeof localStorage.getItem !== 'function'
      || typeof localStorage.setItem !== 'function'
    ) {
      return null;
    }

    return localStorage;
  }
}
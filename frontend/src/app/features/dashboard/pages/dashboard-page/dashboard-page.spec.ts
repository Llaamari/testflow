import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { DashboardPage } from './dashboard-page';
import { DashboardService } from '../../services/dashboard';
import { DashboardStats } from '../../models/dashboard-stats';

describe('DashboardPage', () => {
  let component: DashboardPage;
  let fixture: ComponentFixture<DashboardPage>;

  const dashboardStats: DashboardStats = {
    projects: 4,
    test_runs: 12,
    test_results: 187,
    pass_rate: 91.2,
    failed: 8,
    errors: 3,
    pending: 5,
    status_distribution: {
      PASSED: 171,
      FAILED: 8,
      ERROR: 3,
      PENDING: 5,
    },
    recent_runs: [],
  };

  const dashboardServiceMock = {
    getStats: () => of(dashboardStats),
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardPage],
      providers: [
        {
          provide: DashboardService,
          useValue: dashboardServiceMock,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardPage);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load dashboard statistics', () => {
    expect(component.stats()).toEqual(dashboardStats);
    expect(component.loading()).toBe(false);
    expect(component.errorMessage()).toBeNull();
  });

  it('should display dashboard statistics', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.textContent).toContain('4');
    expect(element.textContent).toContain('12');
    expect(element.textContent).toContain('187');
    expect(element.textContent).toContain('91.2%');
  });
});
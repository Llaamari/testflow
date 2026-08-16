import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatisticsCard } from './statistics-card';

describe('StatisticsCard', () => {
  let component: StatisticsCard;
  let fixture: ComponentFixture<StatisticsCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatisticsCard],
    }).compileComponents();

    fixture = TestBed.createComponent(StatisticsCard);

    fixture.componentRef.setInput('label', 'Projects');
    fixture.componentRef.setInput('value', 4);

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display the label and value', () => {
    const element: HTMLElement = fixture.nativeElement;

    expect(element.textContent).toContain('Projects');
    expect(element.textContent).toContain('4');
  });
});
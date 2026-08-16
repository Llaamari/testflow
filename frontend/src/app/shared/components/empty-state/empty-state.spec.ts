import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';

import { EmptyState } from './empty-state';

describe('EmptyState', () => {
  let component: EmptyState;
  let fixture: ComponentFixture<EmptyState>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmptyState],
    }).compileComponents();

    fixture = TestBed.createComponent(EmptyState);

    fixture.componentRef.setInput(
      'title',
      'No results',
    );

    fixture.componentRef.setInput(
      'message',
      'Nothing to display.',
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display title and message', () => {
    const element: HTMLElement =
      fixture.nativeElement;

    expect(element.textContent).toContain(
      'No results',
    );

    expect(element.textContent).toContain(
      'Nothing to display.',
    );
  });
});
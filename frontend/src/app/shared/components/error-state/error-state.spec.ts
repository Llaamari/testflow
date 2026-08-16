import {
  ComponentFixture,
  TestBed,
} from '@angular/core/testing';

import { ErrorState } from './error-state';

describe('ErrorState', () => {
  let component: ErrorState;
  let fixture: ComponentFixture<ErrorState>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ErrorState],
    }).compileComponents();

    fixture = TestBed.createComponent(ErrorState);

    fixture.componentRef.setInput(
      'message',
      'Something failed.',
    );

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display the error message', () => {
    const element: HTMLElement =
      fixture.nativeElement;

    expect(element.textContent).toContain(
      'Something failed.',
    );
  });
});
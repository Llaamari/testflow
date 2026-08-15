import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestRunListPage } from './test-run-list-page';

describe('TestRunListPage', () => {
  let component: TestRunListPage;
  let fixture: ComponentFixture<TestRunListPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestRunListPage],
    }).compileComponents();

    fixture = TestBed.createComponent(TestRunListPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

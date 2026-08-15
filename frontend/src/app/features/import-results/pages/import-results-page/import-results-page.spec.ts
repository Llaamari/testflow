import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportResultsPage } from './import-results-page';

describe('ImportResultsPage', () => {
  let component: ImportResultsPage;
  let fixture: ComponentFixture<ImportResultsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportResultsPage],
    }).compileComponents();

    fixture = TestBed.createComponent(ImportResultsPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

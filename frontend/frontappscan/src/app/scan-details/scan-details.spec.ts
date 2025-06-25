import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScanDetailsComponent } from './scan-details';

describe('ScanDetails', () => {
  let component: ScanDetailsComponent;
  let fixture: ComponentFixture<ScanDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScanDetailsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScanDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

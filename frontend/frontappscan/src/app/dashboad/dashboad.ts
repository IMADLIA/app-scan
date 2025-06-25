import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ScanService } from '../shared/scan.service';
import { Scan } from '../shared/models/vulnirability.model';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboad.html',
  styleUrls: ['./dashboad.scss'],
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
})
export class DashboadComponent implements OnInit {
  scans: Scan[] = [];
  errorMessage = '';
  scanDetails: any = null;

  constructor(private scanService: ScanService, private router: Router) {}

  ngOnInit() {
    this.loadScans();
  }

  loadScans() {
    this.scanService.getScans().subscribe({
      next: (data) => {
        this.scans = data;
        this.errorMessage = '';
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des scans.';
      },
    });
  }

  openScanDetails(scanId: number) {
    this.router.navigate(['/scan', scanId]); // 👉 navigation vers page dédiée
  }

  goToNewScan() {
    this.router.navigate(['/scan']);
  }

  goToNotification() {
    this.router.navigate(['/notification']);
  }
}

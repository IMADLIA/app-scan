import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScanService } from '../shared/scan.service';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-scan-details',
  templateUrl: './scan-details.html',
  styleUrls: ['./scan-details.scss'],
  imports:[ReactiveFormsModule, CommonModule]
})
export class ScanDetailsComponent implements OnInit {
  scan: any = null;
  vulnerabilities: any[] = [];
  errorMessage = '';

  constructor(private route: ActivatedRoute, private scanService: ScanService) {}

  ngOnInit() {
    const scanId = this.route.snapshot.paramMap.get('id');
    if (!scanId) {
      this.errorMessage = 'ID de scan manquant';
      return;
    }

    this.scanService.getScanDetails(scanId).subscribe({
      next: (data) => {
        this.scan = data.scan;
        this.vulnerabilities = data.vulnerabilities;
      },
      error: () => this.errorMessage = 'Erreur récupération détails scan'
    });
  }

  downloadPdf() {
    if (!this.scan) return;
    this.scanService.downloadReport(this.scan.id.toString()).subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `rapport_scan_${this.scan.id}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    });
  }
}

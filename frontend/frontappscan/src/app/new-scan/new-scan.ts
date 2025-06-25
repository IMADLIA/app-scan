import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ScanService } from '../shared/scan.service';
import { Scan } from '../shared/models/vulnirability.model';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-new-scan',
  templateUrl: './new-scan.html',
  styleUrls: ['./new-scan.scss'],
  imports:[ReactiveFormsModule,CommonModule ]
})
export class NewScanComponent implements OnInit {
  scanForm!: FormGroup;
  isSubmitting = false;
  errorMessage = '';
  scanResult?: Scan;

  constructor(
    private fb: FormBuilder,
    private scanService: ScanService,
    private router: Router
  ) {}

  ngOnInit() {
    this.scanForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern(/https?:\/\/.+/)]],
      name: [''],
      scan_type: ['passif', Validators.required],
    });
  }

  onSubmit() {
    if (this.scanForm.invalid) return;

    this.isSubmitting = true;
    this.errorMessage = '';

    const { url, scan_type, name } = this.scanForm.value;

    this.scanService.startScan(url, scan_type, name).subscribe({
      next: (res) => {
        this.scanResult = res;
        this.isSubmitting = false;
        // Après création, redirection vers dashboard ou détails
        this.router.navigate(['/scan', res.id]);
      },
      error: () => {
        this.errorMessage = 'Erreur lors du lancement du scan';
        this.isSubmitting = false;
      }
    });
  }
  downloadPdf() {
    if (!this.scanResult?.id) return;
  
    this.scanService.downloadReport(this.scanResult.id.toString())
      .subscribe({
        next: (blob: Blob) => {
          console.log("Blob reçu, taille:", blob.size);
          if (blob.size === 0) {
            console.error("Blob vide");
            return;
          }
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `rapport_scan_${this.scanResult!.id}.pdf`;
          document.body.appendChild(a);  // Nécessaire pour certains navigateurs
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
          console.log("Téléchargement PDF déclenché");
        },
        error: err => {
          console.error("Erreur téléchargement PDF", err);
        }
      });
  }
  }  
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Scan, Vulnerability } from './models/vulnirability.model';

@Injectable({
  providedIn: 'root',
})
export class ScanService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  /**
   * Lancer un nouveau scan (POST /scan)
   */
  startScan(url: string, scanType: string, name?: string): Observable<Scan> {
    return this.http.post<Scan>(`${this.baseUrl}/scan`, {
      url: url,
      scan_type: scanType,
      name: name || `Scan - ${url}`
    });
  }
  

  /**
   * Télécharger le rapport PDF d’un scan.
   * GET /scan/{scanId}/report
   */
  downloadReport(scanId: string): Observable<Blob> {
    return this.http.get(`http://localhost:8000/scan/${scanId}/report`, {
      responseType: 'blob'
    });
  }
  
  
  
  

  /**
   * Récupérer la liste des scans (GET /scan)
   */
  getScans(): Observable<Scan[]> {
    return this.http.get<Scan[]>(`${this.baseUrl}/scan`);
  }

  /**
   * Récupérer les détails d’un scan (GET /scan/{scanId})
   */
  getScanDetails(scanId: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/scan/${scanId}`);
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private apiUrl = 'http://localhost:8000/api/notifications';

  constructor(private http: HttpClient) {}

 

  //  Obtenir les préférences de notification
  getNotificationPreferences(userId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/settings/${userId}`);
  }

  // Mettre à jour les préférences
  updateNotificationPreferences(userId: number, preferences: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/settings/${userId}`, preferences);
  }

  // Envoyer une notification manuelle
  sendNotification(scanId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/send`, { scan_id: scanId });
  }
}


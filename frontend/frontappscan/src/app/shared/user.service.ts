import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthResponse } from './models/user.model';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = 'http://localhost:8000/api/users'; 

  constructor(private http: HttpClient) {}

  //  Récupérer le profil utilisateur
  getUserProfile(): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${this.apiUrl}/profile`);
  }

  //  Mettre à jour le profil utilisateur
  updateUserProfile(user: Partial<AuthResponse>): Observable<AuthResponse> {
    return this.http.put<AuthResponse>(`${this.apiUrl}/profile`, user);
  }
}

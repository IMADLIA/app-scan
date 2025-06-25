import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { User, AuthResponse } from '../shared/models/user.model';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  name: string;
  email: string;
  password: string;
  company?: string;
}

@Injectable({
  providedIn: 'root',
})


export class AuthService {
  private tokenKey = 'auth_token';
  private userKey = 'current_user';
  private apiUrl = 'http://localhost:8000'; // ton backend FastAPI

  constructor(private http: HttpClient) {}

  login(credentials: LoginCredentials): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login`, credentials).pipe(
      tap((response) => {
        this.storeAuthData(response);
      }),
      catchError(this.handleError)
    );
  }

  signup(userData: SignupData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/signup`, userData).pipe(
      tap((response) => {
        this.storeAuthData(response);
      }),
      catchError(this.handleError)
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem(this.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  isTokenValid(): boolean {
    const token = this.getToken();
    // Ici, pour un vrai token JWT, on pourrait vérifier la validité
    return !!token;
  }

  private storeAuthData(response: AuthResponse): void {
    localStorage.setItem(this.tokenKey, response.token);
    localStorage.setItem(this.userKey, JSON.stringify({
      id: response.id,
      name: response.name,
      email: response.email,
      company: response.company,
    }));
  }

  private handleError(error: HttpErrorResponse) {
    let errorMsg = 'An unknown error occurred!';
    if (error.error instanceof ErrorEvent) {
      // Client-side/network error
      errorMsg = `Error: ${error.error.message}`;
    } else {
      // Backend returned an error response
      errorMsg = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(() => new Error(errorMsg));
  }
}

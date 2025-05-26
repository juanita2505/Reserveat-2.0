import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1';
  private loggedIn = new BehaviorSubject<boolean>(false);
  private currentUserRole = new BehaviorSubject<string>('customer');

  constructor(private http: HttpClient, private router: Router) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.loggedIn.next(true);
      const role = localStorage.getItem('user_role') || 'customer';
      this.currentUserRole.next(role);
    }
  }

  get isLoggedIn(): boolean {
    return this.loggedIn.value;
  }

  get userRole(): string {
    return this.currentUserRole.value;
  }

  register(userData: {
    full_name: string;
    email: string;
    password: string;
    role: string;
    username?: string; 
  }): Observable<unknown> {
    const username = userData.username || this.generateUsername(userData.full_name);
    const payload = { ...userData, username };

    return this.http.post(`${this.apiUrl}/register`, payload).pipe(
      tap((response: unknown) => {
        this.handleAuthSuccess(response as any);
      })
    );
  }

  login(credentials: { email: string; password: string }): Observable<unknown> {
    return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
      tap((response: unknown) => {
        this.handleAuthSuccess(response as any);
      })
    );
  }

  private handleAuthSuccess(response: any): void {
    localStorage.setItem('auth_token', response.token);
    localStorage.setItem('user_role', response.role || 'customer');

    this.loggedIn.next(true);
    this.currentUserRole.next(response.role || 'customer');

    const redirectPath = response.role === 'restaurant_owner' ? '/owner' : '/restaurants';
    this.router.navigate([redirectPath]);
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_role');
    this.loggedIn.next(false);
    this.currentUserRole.next('customer');
    this.router.navigate(['/auth/login']);
  }

  isAuthenticated(): Observable<boolean> {
    return this.loggedIn.asObservable();
  }

  getCurrentUserRole(): Observable<string> {
    return this.currentUserRole.asObservable();
  }

  // generar username a partir del nombre
  private generateUsername(fullName: string): string {
    const base = fullName.trim().toLowerCase().replace(/\s+/g, '');
    const suffix = Math.floor(Math.random() * 10000);
    return `${base}${suffix}`;
  }
}

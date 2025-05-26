import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';
  private loggedIn = new BehaviorSubject<boolean>(false);
  private currentUserRole = new BehaviorSubject<string>('customer');

  constructor(private http: HttpClient, private router: Router) {
    // Check localStorage for existing auth
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.loggedIn.next(true);
      const role = localStorage.getItem('user_role') || 'customer';
      this.currentUserRole.next(role);
    }
  }

  // Añade esta propiedad getter
  get isLoggedIn(): boolean {
    return this.loggedIn.value;
  }

  // Añade esta propiedad getter
  get userRole(): string {
    return this.currentUserRole.value;
  }

  register(userData: { 
    full_name: string;  
    email: string; 
    password: string;
    role: string; 
  }): Observable<any> {
    return this.http.post('${this.apiUrl}/register', userData).pipe(
      tap((response: any) => {
        this.handleAuthSuccess(response);
      })
    );
  }

  login(credentials: {email: string, password: string}): Observable<any> {
    return this.http.post('${this.apiUrl}/login', credentials).pipe(
      tap((response: any) => {
        this.handleAuthSuccess(response);
      })
    );
  }

  private handleAuthSuccess(response: any): void {
    localStorage.setItem('auth_token', response.token);
    localStorage.setItem('user_role', response.role || 'customer');
    this.loggedIn.next(true);
    this.currentUserRole.next(response.role || 'customer');
    
    // Redirect based on role
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
}
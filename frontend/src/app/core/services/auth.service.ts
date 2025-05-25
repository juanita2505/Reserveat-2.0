import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
  
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';
  private authUrl = 'api/auth';
  private loggedIn = new BehaviorSubject<boolean>(false);
  private currentUserRole = new BehaviorSubject<string>('user'); // 'user' o 'admin'

  constructor(private http: HttpClient, private router: Router) {}

  register(userData: { 
  full_name: string;  
  email: string; 
  password: string;
  role:string; 
}): Observable<any> {
  return this.http.post(`${this.apiUrl}/register`, userData);
}

  login(credentials: {email: string, password: string}): Observable<any> {
    return this.http.post(`${this.authUrl}/login`, credentials).pipe(
      tap((response: any) => {
        this.loggedIn.next(true);
        this.currentUserRole.next(response.role || 'user');
      })
    );
  }

  logout(): void {
    this.loggedIn.next(false);
    this.currentUserRole.next('user');
    this.router.navigate(['/login']);
  }

  isAuthenticated(): Observable<boolean> {
    return this.loggedIn.asObservable();
  }

  isAdmin(): boolean {
    return this.currentUserRole.value === 'admin';
  }

  getCurrentUserRole(): Observable<string> {
    return this.currentUserRole.asObservable();
  }
}
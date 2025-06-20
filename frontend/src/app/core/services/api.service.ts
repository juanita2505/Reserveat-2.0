import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  get<T>(endpoint: string, params: any = {}) {
    // Convierte los params a HttpParams
    let httpParams = new HttpParams();
    Object.keys(params).forEach(key => {
      httpParams = httpParams.append(key, params[key]);
    });

    return this.http.get<T>(`${this.apiUrl}/${endpoint}`, { 
      params: httpParams 
    });
  }

  post<T>(endpoint: string, body: any = {}) {
    return this.http.post<T>(`${this.apiUrl}/${endpoint}`, body, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Métodos adicionales recomendados
  put<T>(endpoint: string, body: any = {}) {
    return this.http.put<T>(`${this.apiUrl}/${endpoint}`, body);
  }

  delete<T>(endpoint: string) {
    return this.http.delete<T>(`${this.apiUrl}/${endpoint}`);
  }
}
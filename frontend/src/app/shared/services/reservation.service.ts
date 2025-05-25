import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

interface Reservation {
  id: number;
  restaurant_id: number;
  user_id: number;
  date: string;
  guests: number;
  status: 'pending' | 'confirmed' | 'cancelled';
}

@Injectable({ providedIn: 'root' })
export class ReservationService {
  private readonly API_URL = ${environment.apiUrl}/reservations;

  constructor(private http: HttpClient) {}

  getUserReservations(): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(this.API_URL);
  }

  create(reservation: Omit<Reservation, 'id' | 'status'>): Observable<Reservation> {
    return this.http.post<Reservation>(this.API_URL, reservation);
  }

  cancel(id: number): Observable<void> {
    return this.http.patch<void>(${this.API_URL}/${id}/cancel, {});
  }
}
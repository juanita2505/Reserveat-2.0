import { Injectable } from '@angular/core';
import { ApiService } from '../../core/services/api.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {
  constructor(private api: ApiService) {}

  getRestaurants(): Observable<any> {
    return this.api.get('restaurants');
  }
}

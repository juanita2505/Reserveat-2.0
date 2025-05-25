import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RestaurantService } from '../../shared/services/restaurant.service';

@Component({
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="restaurants.length > 0">
      <div *ngFor="let r of restaurants">
        {{ r.name }} - {{ r.address }}
      </div>
    </div>
  `
})
export class RestaurantListComponent {
  restaurants: any[] = [];
  private restaurantService = inject(RestaurantService);

  constructor() {
    this.restaurantService.getAll().subscribe({
      next: (data: any) => this.restaurants = data,
      error: (err) => console.error('Error:', err)
    });
  }
}
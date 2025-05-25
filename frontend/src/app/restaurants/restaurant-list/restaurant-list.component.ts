import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RestaurantService } from '../../core/services/restaurant.service';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './restaurant-list.component.html'
})
export class RestaurantListComponent implements OnInit {
  restaurants: any[] = [];
  loading = true;

  constructor(private restaurantService: RestaurantService) {}

  ngOnInit(): void {
    this.restaurantService.getAll().subscribe({
      next: (data) => {
        this.restaurants = data;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }
}
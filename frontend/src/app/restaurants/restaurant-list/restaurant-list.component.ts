import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RestaurantService } from '../../shared/services/restaurant.service';
import { RouterModule } from '@angular/router';
import { LoadingComponent } from '../../shared/components/loading/loading.component';

@Component({
  standalone: true,
  imports: [CommonModule, RouterModule, LoadingComponent],
  templateUrl: './restaurant-list.component.html',
  styleUrls: ['./restaurant-list.component.scss']
})
export class RestaurantListComponent implements OnInit {
  restaurants: any[] = [];
  loading = true;

  constructor(private restaurantService: RestaurantService) {}

  ngOnInit(): void {
    this.restaurantService.getAll().subscribe({
      next: (data: any) => {
        this.restaurants = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error:', err);
        this.loading = false;
      }
    });
  }
}
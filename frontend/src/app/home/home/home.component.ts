import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface Restaurant {
  id: number;
  name: string;
  image: string;
  cuisine: string;
  priceRange: string;
  reviews: number;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  featuredRestaurants: Restaurant[] = [
    {
      id: 1,
      name: 'Gourmet Place',
      image: 'assets/restaurants/restaurant1.jpg',
      cuisine: 'Internacional',
      priceRange: '$$$',
      reviews: 124
    },
    {
      id: 2,
      name: 'Sushi Master',
      image: 'assets/restaurants/restaurant2.jpg',
      cuisine: 'Japonés',
      priceRange: '$$',
      reviews: 89
    },
    {
      id: 3,
      name: 'La Trattoria',
      image: 'assets/restaurants/restaurant3.jpg',
      cuisine: 'Italiano',
      priceRange: '$$',
      reviews: 156
    },
    {
      id: 4,
      name: 'Steak House',
      image: 'assets/restaurants/restaurant4.jpg',
      cuisine: 'Carnes',
      priceRange: '$$$',
      reviews: 201
    }
  ];
}
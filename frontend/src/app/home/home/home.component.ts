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
  rating?: number; // Propiedad opcional añadida
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  // Datos de ejemplo mejorados con rating
  featuredRestaurants: Restaurant[] = [
    {
      id: 1,
      name: 'Gourmet Place',
      image: 'assets/restaurants/restaurant1.jpg',
      cuisine: 'Internacional',
      priceRange: '$$$',
      reviews: 124,
      rating: 4.5
    },
    {
      id: 2,
      name: 'Sushi Master',
      image: 'assets/restaurants/restaurant2.jpg',
      cuisine: 'Japonés',
      priceRange: '$$',
      reviews: 89,
      rating: 4.7
    },
    {
      id: 3,
      name: 'La Trattoria',
      image: 'assets/restaurants/restaurant3.jpg',
      cuisine: 'Italiano',
      priceRange: '$$',
      reviews: 156,
      rating: 4.3
    },
    {
      id: 4,
      name: 'Steak House',
      image: 'assets/restaurants/restaurant4.jpg',
      cuisine: 'Carnes',
      priceRange: '$$$',
      reviews: 201,
      rating: 4.8
    }
  ];

  // Método para generar estrellas (opcional)
  getStars(rating: number | undefined): string {
    if (!rating) return '★★★★★';
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? '½' : '';
    return '★'.repeat(fullStars) + halfStar + '☆'.repeat(5 - fullStars - (halfStar ? 1 : 0));
  }
}
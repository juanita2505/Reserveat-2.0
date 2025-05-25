import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./home/home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'restaurants',
    loadComponent: () =>
      import('./restaurants/restaurant-list/restaurant-list.component').then(
        (m) => m.RestaurantListComponent
      ),
    canActivate: [AuthGuard],
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./auth/login/login.component').then((m) => m.LoginComponent),
  },
  { path: '**', redirectTo: '' },
];

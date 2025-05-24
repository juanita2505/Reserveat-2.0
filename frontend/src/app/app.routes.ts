import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then(m => m.HomeComponent),
    title: 'Reserveat - Inicio'
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.routes').then(m => m.AUTH_ROUTES),
  },
  {
    path: 'restaurants',
    loadChildren: () => import('./restaurants/restaurants.routes').then(m => m.RESTAURANT_ROUTES),
  },
  {
    path: 'reservations',
    canActivate: [AuthGuard],
    loadChildren: () => import('./reservations/reservations.routes').then(m => m.RESERVATION_ROUTES),
  },
  {
    path: 'profile',
    canActivate: [AuthGuard],
    loadComponent: () => import('./user/profile/profile.component').then(m => m.ProfileComponent),
    title: 'Mi Perfil'
  },
  {
    path: 'owner',
    canActivate: [AuthGuard, RoleGuard],
    data: { role: 'restaurant_owner' },
    loadChildren: () => import('./owner/owner.routes').then(m => m.OWNER_ROUTES),
  },
  {
    path: '**',
    redirectTo: ''
  }
];
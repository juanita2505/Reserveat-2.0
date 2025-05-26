import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';
import { MainLayoutComponent } from './shared/layouts/main-layout/main-layout.component';
import { AuthLayoutComponent } from './shared/layouts/auth-layout/auth-layout.component';

export const routes: Routes = [
  // Rutas Públicas (Auth) - Usan AuthLayout
  {
    path: 'auth',
    component: AuthLayoutComponent,
    children: [
      {
        path: '',
        loadComponent: () => import('./auth/auth-tabs.component').then(m => m.AuthTabsComponent),
        children: [
          { path: 'login', loadComponent: () => import('./auth/login/login.component').then(m => m.LoginComponent) },
          { path: 'register', loadComponent: () => import('./auth/register/register.component').then(m => m.RegisterComponent) },
          { path: '', redirectTo: 'login', pathMatch: 'full' }
        ]
      }
    ]
  },

  // Rutas Principales - Usan MainLayout y AuthGuard
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [AuthGuard],
    children: [
      { path: '', loadComponent: () => import('./home/home/home.component').then(m => m.HomeComponent) },
      {
        path: 'restaurants',
        loadComponent: () => import('./restaurants/restaurant-list/restaurant-list.component').then(m => m.RestaurantListComponent)
      },
      
      // Rutas de Owner (con RoleGuard adicional)
      {
        path: 'owner',
        canActivate: [RoleGuard],
        data: { role: 'restaurant_owner' },
        children: [
          { path: '', loadComponent: () => import('./owner/dashboard/dashboard.component').then(m => m.DashboardComponent) },
          { path: 'restaurants', loadComponent: () => import('./owner/restaurants/restaurants.component').then(m => m.RestaurantsComponent) },
          { path: 'reservations', loadComponent: () => import('./owner/reservations/reservations.component').then(m => m.ReservationsComponent) }
        ]
      }
    ]
  },

  // Redirecciones
  { path: '', redirectTo: 'auth/login', pathMatch: 'full' }, // Redirige a login por defecto
  { path: '**', redirectTo: '' } // Manejo de rutas no encontradas
];
import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

// Definición de rutas principales de la aplicación
export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./auth/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'restaurants',
    loadComponent: () =>
      import('./restaurants/restaurant-list/restaurant-list.component').then(
        m => m.RestaurantListComponent
      ),
    canActivate: [AuthGuard]  // Protege la ruta con autenticación
  },

  // Redirección por defecto a login
  { path: '', redirectTo: '/login', pathMatch: 'full' },

  // Ruta comodín para rutas no existentes - redirige a login
  { path: '**', redirectTo: '/login' }
];
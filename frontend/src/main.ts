import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideRouter, withDebugTracing, withEnabledBlockingInitialNavigation } from '@angular/router';
import { routes } from './app/app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { authInterceptor } from './app/core/interceptors/auth.interceptor';
import { importProvidersFrom } from '@angular/core';
import { MatSnackBarModule } from '@angular/material/snack-bar';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(
      routes,
      withEnabledBlockingInitialNavigation(), // Mejor experiencia de carga inicial
      // withDebugTracing() // Solo para desarrollo
    ),
    provideHttpClient(
      withInterceptors([authInterceptor]) // Interceptores HTTP
    ),
    provideAnimations(), // Animaciones de Angular
    importProvidersFrom(
      MatSnackBarModule // Ejemplo de módulo de Angular Material
    ),
    // Otros providers globales
  ]
}).catch(err => console.error('Error al iniciar la aplicación:', err));
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({ providedIn: 'root' })
export class RoleGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const expectedRole = route.data['role'];
    const userRole = this.authService.userRole;

    if (userRole === expectedRole) {
      return true;
    }
    
    // Redirect to appropriate page based on role
    const redirectPath = this.authService.isLoggedIn ? 
      (userRole === 'restaurant_owner' ? '/owner' : '/restaurants') : 
      '/auth/login';
    
    this.router.navigate([redirectPath]);
    return false;
  }
}
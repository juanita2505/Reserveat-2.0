import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router'; // Importación correcta
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs/operators';
import { NavigationEnd } from '@angular/router'; // Importación adicional necesaria

@Component({
  selector: 'app-auth-tabs',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule // Asegúrate de incluirlo aquí
  ],
  templateUrl: './auth-tabs.component.html',
  styleUrls: ['./auth-tabs.component.scss']
})
export class AuthTabsComponent {
  activeTab: 'login' | 'register' = 'login';

  constructor(private router: Router) {
    this.router.events
      .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.activeTab = event.url.includes('register') ? 'register' : 'login';
      });
  }

  navigateTo(tab: 'login' | 'register'): void {
    this.router.navigate(['/auth', tab]);
  }
}
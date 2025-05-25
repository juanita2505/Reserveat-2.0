import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { LoadingComponent } from '../../shared/components/loading/loading.component';
import { AlertComponent } from '../../shared/components/alert/alert.component';

@Component({
  standalone: true,
  imports: [
    ReactiveFormsModule,
    CommonModule,
    RouterModule,
    LoadingComponent,
    AlertComponent
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$/)
    ])
  });

  isLoading = false;
  errorMessage: string | null = null;
  private authSubscription: Subscription | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (this.authService.isAuthenticated()) {
      this.redirectBasedOnRole();
    }
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    const { email, password } = this.loginForm.value;

    this.authSubscription = this.authService.login(email!, password!).subscribe({
      next: () => {
        this.isLoading = false;
        this.redirectBasedOnRole();
      },
      error: (error) => {
        this.isLoading = false;
        this.handleError(error);
      }
    });
  }

  private redirectBasedOnRole(): void {
    const userRole = this.authService.getCurrentUserRole();

    switch (userRole) {
      case 'restaurant_owner':
        this.router.navigate(['/owner/dashboard']);
        break;
      case 'admin':
        this.router.navigate(['/admin/dashboard']);
        break;
      default:
        this.router.navigate(['/home']);
    }
  }

  private markAllAsTouched(): void {
    Object.values(this.loginForm.controls).forEach(control => control.markAsTouched());
  }

  private handleError(error: any): void {
    if (error.status === 401) {
      this.errorMessage = 'Credenciales inválidas. Por favor, inténtalo de nuevo.';
    } else if (error.status === 0) {
      this.errorMessage = 'No se puede conectar al servidor. Verifica tu conexión a internet.';
    } else {
      this.errorMessage = 'Ocurrió un error inesperado. Por favor, inténtalo más tarde.';
    }
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }
}
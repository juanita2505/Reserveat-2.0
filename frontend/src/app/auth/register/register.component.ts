import { Component, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormControl,
  FormGroup,
  Validators,
  AbstractControl,
  ValidationErrors,
  ReactiveFormsModule
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '@app/core/services/auth.service';
import { Subscription } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { AlertComponent } from '@app/shared/components/alert/alert.component';
import { LoadingComponent } from '@app/shared/components/loading/loading.component';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    AlertComponent,
    LoadingComponent
  ],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnDestroy {
  registerForm = new FormGroup({
    fullName: new FormControl('', [
      Validators.required,
      Validators.minLength(3),
      Validators.maxLength(50)
    ]),
    email: new FormControl('', [
      Validators.required,
      Validators.email,
      Validators.maxLength(100)
    ]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$/)
    ]),
    confirmPassword: new FormControl('', [Validators.required]),
    role: new FormControl('customer')
  }, { validators: RegisterComponent.passwordMatchValidator });

  private authSubscription?: Subscription;
  isLoading = false;
  errorMessage: string | null = null;
  showRoleSelector = true;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    const { fullName, email, password, role } = this.registerForm.value;

    // ⚠️ username generado automáticamente
    const username = fullName?.trim().toLowerCase().replace(/\s+/g, '') || `user${Date.now()}`;

    this.authSubscription = this.authService.register({
      username: username,
      full_name: fullName?.trim() ?? '',
      email: email?.trim() ?? '',
      password: password ?? '',
      role: role ?? 'customer'
    }).pipe(
      finalize(() => this.isLoading = false)
    ).subscribe({
      next: () => {
        this.router.navigate(['/auth/login']);
      },
      error: (error) => {
        this.handleError(error);
      }
    });
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
  }

  private markAllAsTouched(): void {
    Object.values(this.registerForm.controls).forEach(control => {
      control.markAsTouched();
    });
  }

  private handleError(error: any): void {
    console.error('Registration error:', error);

    if (error.status === 400 && error.error?.detail === "Email already registered") {
      this.errorMessage = 'Este correo electrónico ya está registrado';
      this.registerForm.get('email')?.setErrors({ emailTaken: true });
    } else if (error.status === 0) {
      this.errorMessage = 'No se pudo conectar al servidor. Verifica tu conexión.';
    } else {
      this.errorMessage = error.error?.message || 'Error en el registro. Por favor intenta nuevamente.';
    }
  }

  private static passwordMatchValidator(form: AbstractControl): ValidationErrors | null {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  // Getters
  get fullName() { return this.registerForm.get('fullName'); }
  get email() { return this.registerForm.get('email'); }
  get password() { return this.registerForm.get('password'); }
  get confirmPassword() { return this.registerForm.get('confirmPassword'); }
  get role() { return this.registerForm.get('role'); }
}

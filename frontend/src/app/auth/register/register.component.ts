import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators, AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
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
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit, OnDestroy {
  registerForm = new FormGroup({
    fullName: new FormControl('', [
      Validators.required,
      Validators.minLength(3)
    ]),
    email: new FormControl('', [
      Validators.required,
      Validators.email,
    ]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$/)
    ]),
    confirmPassword: new FormControl('', [
      Validators.required
    ]),
    role: new FormControl('customer')
  }, { validators: this.passwordMatchValidator() });

  private authSubscription: Subscription | null = null;

  isLoading = false;
  errorMessage: string | null = null;
  showRoleSelector = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.showRoleSelector = !this.router.url.includes('owner');
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    const fullName = this.fullName?.value!;
    const email = this.email?.value!;
    const password = this.password?.value!;
    const role = this.role?.value!;

    this.authSubscription = this.authService.register({
      full_name: fullName,
      email,
      password,
      role
    }).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/verify-email']);
      },
      error: (error) => {
        this.isLoading = false;
        this.handleError(error);
      }
    });
  }

  private markAllAsTouched(): void {
    Object.values(this.registerForm.controls).forEach(control => control.markAsTouched());
  }

  private handleError(error: any): void {
    if (error.status === 400 && error.error?.detail === "Email already registered") {
      this.errorMessage = 'Este correo electrónico ya está registrado';
    } else if (error.status === 0) {
      this.errorMessage = 'No se puede conectar al servidor. Verifica tu conexión a internet.';
    } else {
      this.errorMessage = 'Ocurrió un error inesperado. Por favor, inténtalo más tarde.';
    }
  }

  private passwordMatchValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
      const formGroup = control as FormGroup;
      const password = formGroup.get('password')?.value;
      const confirmPassword = formGroup.get('confirmPassword')?.value;
      return password === confirmPassword ? null : { mismatch: true };
    };
  }

  // Getters para acceso limpio en el template
  get fullName() {
    return this.registerForm.get('fullName');
  }
  get email() {
    return this.registerForm.get('email');
  }
  get password() {
    return this.registerForm.get('password');
  }
  get confirmPassword() {
    return this.registerForm.get('confirmPassword');
  }
  get role() {
    return this.registerForm.get('role');
  }
}
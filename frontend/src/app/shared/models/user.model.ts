export interface RegisterUser {
  full_name: string;
  email: string;
  password: string;
  role: string; // El signo ? lo hace opcional
}
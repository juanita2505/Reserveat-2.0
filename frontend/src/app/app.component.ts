import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  standalone: true,
  imports: [RouterOutlet], // Solo RouterOutlet, eliminamos NavbarComponent
  template: `<router-outlet></router-outlet>`
})
export class AppComponent {}
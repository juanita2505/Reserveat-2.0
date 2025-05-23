import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// Componentes
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { LoadingComponent } from './components/loading/loading.component';
import { AlertComponent } from './components/alert/alert.component';

@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    LoadingComponent,
    AlertComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [
    NavbarComponent,
    FooterComponent,
    LoadingComponent,
    AlertComponent
  ]
})
export class SharedModule {}

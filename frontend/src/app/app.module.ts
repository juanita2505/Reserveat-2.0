import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { SharedModule } from './shared/shared.module'; // Asegúrate que esta línea existe

@NgModule({
  imports: [
    BrowserModule,
    SharedModule  // Debe estar aquí
  ],
  // ... otras configuraciones
})
export class AppModule { }
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MAT_COLOR_FORMATS, NGX_MAT_COLOR_FORMATS } from '@angular/material/core';
import { provideClientHydration } from '@angular/platform-browser';

export function provideMaterial() {
  return [
    provideClientHydration(),
    provideAnimationsAsync(),
    { provide: MAT_COLOR_FORMATS, useValue: NGX_MAT_COLOR_FORMATS }
  ];
}
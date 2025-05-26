import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideClientHydration } from '@angular/platform-browser';

export function provideMaterial() {
  return [
    provideClientHydration(),
    provideAnimationsAsync()
  ];
}
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="loading-container" 
         [class.small]="size === 'small'"
         [class.medium]="size === 'medium'" 
         [class.large]="size === 'large'">
      <div class="loading-spinner"></div>
      @if (showText) {
        <span class="loading-text">{{ text }}</span>
      }
    </div>
  `,
  styleUrls: ['./loading.component.scss']
})
export class LoadingComponent {
  @Input() size: 'small' | 'medium' | 'large' = 'medium';
  @Input() showText: boolean = true;
  @Input() text: string = 'Cargando...';
}
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="alert" [class]="'alert-' + type" *ngIf="message">
      <span>{{ message }}</span>
      <button *ngIf="dismissible" (click)="onDismiss()" class="close-btn">&times;</button>
    </div>
  `,
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent {
  @Input() message: string | null = null;
  @Input() type: 'success' | 'error' | 'info' | 'warning' = 'info';
  @Input() dismissible: boolean = true;
  @Output() dismiss = new EventEmitter<void>();

  onDismiss() {
    this.dismiss.emit();
  }
}
import { Component, input } from '@angular/core';

@Component({
  selector: 'app-statistics-card',
  templateUrl: './statistics-card.html',
  styleUrl: './statistics-card.css',
})
export class StatisticsCard {
  readonly label = input.required<string>();
  readonly value = input.required<string | number>();
  readonly helperText = input<string>();
}
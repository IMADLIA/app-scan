import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <h1>Welcome to App Scanner!</h1>
    <router-outlet></router-outlet>
  `,
})
export class AppComponent {}
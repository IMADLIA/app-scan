import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './auth/auth.guard';
import { NgModel } from '@angular/forms';
import { NgModule } from '@angular/core';
export const routes: Routes = [
  {
    path: 'login',
    title: 'Login',
    loadComponent: () => import('./auth/login/login').then((m) => m.LoginComponent),
  },
  {
    path: 'signup',
    title: 'Register',
    loadComponent: () => import('./auth/signup/signup').then((m) => m.SignupComponent),
  },
 {path: 'dashboard',
    title: 'Dashboard',

    loadComponent: () => import('./dashboad/dashboad').then((m) => m.DashboadComponent),
  },
  {
    path: 'scan/:id',
    title: 'Scan Details',
    
    loadComponent: () => import('./scan-details/scan-details').then((m) => m.ScanDetailsComponent),
  },
  {
    path: 'scan',
    title: 'New Scan',
    
    loadComponent: () => import('./new-scan/new-scan').then((m) => m.NewScanComponent),
  },
  {
    path: 'settings',
    title: 'Settings',
    
    loadComponent: () => import('./settings/settings').then((m) => m.SettingsComponent),
  },
  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full',
  },
  {
  path: 'notification',
  title: 'notification',
  loadComponent: () => import('./notification/notification').then((m) => m.NotificationComponent),
    },
  {
    path: '**',
    redirectTo: '/login',
    pathMatch: 'full',
  },
];
@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
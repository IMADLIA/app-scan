import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
// Module de routage (assure-toi que c'est le bon nom de fichier)
import { AppRoutingModule } from './app-routing';
import { FormsModule } from '@angular/forms'; 
// Composant principal
import { AppComponent } from './appComponent'; 

// Services
import { AuthService } from './auth/auth.service'; 
import { AuthGuard } from './auth/auth.guard';

import { ScanService } from './shared/scan.service';
import { UserService } from './shared/user.service';
import { NotificationService } from './shared/notification.service';
import { LoginComponent } from './auth/login/login';
import { SignupComponent } from './auth/signup/signup';
import { DashboadComponent } from './dashboad/dashboad';
import { ScanDetailsComponent } from './scan-details/scan-details';
import { NewScanComponent } from './new-scan/new-scan';
import  { NotificationComponent } from './notification/notification';

@NgModule({
  declarations: [
    // Ajoute ton composant principal
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    AppRoutingModule, 
     AppComponent,
     LoginComponent,
     SignupComponent,
     ReactiveFormsModule ,
     CommonModule ,
     FormsModule
  // Import du module de routing
  ],
  providers: [
    AuthService,
    AuthGuard,
    ScanService,
    UserService,
    NotificationService,
  ],
  // Composant de démarrage
})
export class AppModule { }
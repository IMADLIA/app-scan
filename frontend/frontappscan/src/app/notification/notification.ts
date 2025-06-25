import { Component, OnInit } from '@angular/core';
import { NotificationService } from '../shared/notification.service';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-notification',
  templateUrl: './notification.html',
  styleUrls: ['./notification.scss'],
  imports:[ReactiveFormsModule, CommonModule, FormsModule ]
})
export class NotificationComponent implements OnInit {
  userId = 1;
  scanId: number = 1;  // à remplacer par la logique utilisateur connectée
  preferences: any = {
    emailEnabled: false,
    pushEnabled: false,
    webhookUrl: ''
  };
  loading = false;
  errorMessage = '';
  successMessage = '';

  constructor(private notificationService: NotificationService) {}

  ngOnInit(): void {
    const userId = 1;  // à ajuster si tu as une auth réelle
    this.loading = true;
  
    this.notificationService.getNotificationPreferences(userId).subscribe({
      next: (data) => {
        this.preferences = data;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = "Erreur lors du chargement des préférences.";
        this.loading = false;
      }
    });
  }

  savePreferences() {
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.notificationService.updateNotificationPreferences(this.userId, this.preferences).subscribe({
      next: () => {
        this.successMessage = 'Préférences sauvegardées avec succès.';
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Erreur lors de la sauvegarde des préférences.';
        this.loading = false;
      }
    });
  }

  sendNotification() {
    if (!this.scanId) {
      this.errorMessage = "ID du scan non fourni.";
      return;
    }
  
    this.notificationService.sendNotification(this.scanId).subscribe({
      next: () => {
        this.successMessage = "Notification envoyée avec succès.";
        this.errorMessage = '';
      },
      error: () => {
        this.successMessage = '';
        this.errorMessage = "Erreur lors de l’envoi de la notification.";
      }
    });
  }
    }

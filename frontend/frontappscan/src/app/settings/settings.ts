import { Component, OnInit } from '@angular/core';
import { NotificationService } from '../shared/notification.service';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  imports: [CommonModule, FormsModule],
  templateUrl: './settings.html',
})
export class SettingsComponent implements OnInit {
  notificationPrefs: any = {
    emailNotifications: false,
    pushNotifications: false,
    criticalSeverity: false,
    highSeverity: false,
    mediumSeverity: false,
    lowSeverity: false,
    scanCompleted: false,
    scanFailed: false,
  };

  userId: number = 1; // Remplace avec AuthService ou localStorage si besoin

  constructor(private notificationService: NotificationService) {}

  ngOnInit(): void {
    this.notificationService
      .getNotificationPreferences(this.userId)
      .subscribe((prefs: any) => {
        this.notificationPrefs = prefs;
      });
  }

  savePreferences(): void {
    this.notificationService
      .updateNotificationPreferences(this.userId, this.notificationPrefs)
      .subscribe(() => {
        alert('Préférences de notification mises à jour avec succès ✅');
      });
  }
}

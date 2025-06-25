import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/appComponent';
import { importProvidersFrom } from '@angular/core';
import { AppModule } from './app/app.module';
import'zone.js';
bootstrapApplication(AppComponent, {
  providers: [importProvidersFrom(AppModule)],
}).catch((err) => console.error(err));
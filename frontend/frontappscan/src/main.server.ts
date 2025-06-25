import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/appComponent';
import { config } from './app/app.config.server';
import 'zone.js/node'; // ✅ Import spécifique pour SSR

const bootstrap = () => bootstrapApplication(AppComponent, config);

export default bootstrap;

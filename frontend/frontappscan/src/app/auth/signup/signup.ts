import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService,SignupData } from '../auth.service'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,RouterLink],
  templateUrl: './signup.html',
  styleUrls: ['./signup.scss'],
})
export class SignupComponent implements OnInit {
  signupForm!: FormGroup;
  errorMessage = '';
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.signupForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      company: [''],
    });
  }

  onSubmit(): void {
    if (this.signupForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';
      const data: SignupData = this.signupForm.value;
      this.authService.signup(data).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/login']);
        },
        error: (error) => {
          this.isLoading = false;
          this.errorMessage = error.message;
        },
      });
    } else {
      this.signupForm.markAllAsTouched();
    }
  }
}
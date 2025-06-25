export interface User {
  id: string;
  name: string;
  email: string;
  company?: string;
}

export interface AuthResponse extends User {
  token: string;
}
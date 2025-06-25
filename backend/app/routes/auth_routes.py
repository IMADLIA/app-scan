# app/routes/auth_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid


router = APIRouter(tags=["Auth"])

# Modèles
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    company: Optional[str] = ""

class AuthResponse(BaseModel):
    id: str
    name: str
    email: str
    company: Optional[str]
    token: str

# Simuler une "DB" temporaire
mock_users = {}

# Routes
@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    user = mock_users.get(request.email)
    if user and user["password"] == request.password:
        return AuthResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            company=user.get("company", ""),
            token="mock-jwt-token"
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    if request.email in mock_users:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = str(uuid.uuid4())
    mock_users[request.email] = {
        "id": user_id,
        "name": request.name,
        "email": request.email,
        "password": request.password,  # ATTENTION: en prod, il faut hasher le password
        "company": request.company
    }
    return AuthResponse(
        id=user_id,
        name=request.name,
        email=request.email,
        company=request.company,
        token="mock-jwt-token"
    )

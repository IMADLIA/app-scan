from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Base de données simulée
settings_db = {}
settings_db[1] = {
    "user_id": 1,
    "email_enabled": True,
    "push_enabled": False,
    "webhook_url": ""
}

class NotificationSettings(BaseModel):
    user_id: int
    email_enabled: bool = True
    push_enabled: bool = False
    webhook_url: Optional[str] = ""

@router.get("/settings/{user_id}")
def get_settings(user_id: int):
    if user_id not in settings_db:
        raise HTTPException(status_code=404, detail="Préférences non trouvées")
    return settings_db[user_id]

@router.put("/settings/{user_id}")
def update_settings(user_id: int, settings: NotificationSettings):
    settings_db[user_id] = settings.dict()
    return {"message": "Préférences mises à jour", "settings": settings_db[user_id]}

class NotificationRequest(BaseModel):
    scan_id: int

@router.post("/send")
def send_notification(payload: NotificationRequest):
    try:
        # Exemple simple : affiche dans la console
        print(f" Notification envoyée pour le scan {payload.scan_id}")
        return {"message": f"Notification envoyée pour le scan {payload.scan_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
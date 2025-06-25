from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import select, func

# Base de données
from .database.connexion import init_database, check_database_connection, AsyncSessionLocal
from .database.models import User

# Routes
from app.routes import auth_routes
from app.routes import scan_routes  
from app.routes import notification_routes


#  Cycle de vie (startup / shutdown)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(" Démarrage de l'application...")

        # Vérification et initialisation DB
        if not await check_database_connection():
            raise Exception(" Impossible de se connecter à la base de données")

        await init_database()
        print("Application démarrée avec succès")
        yield

    except Exception as e:
        print(f"Erreur au démarrage: {e}")
        raise e

    finally:
        print("Arrêt de l'application...")

 
# Création de l'application

app = FastAPI(
    title="Vulnerability Scanner API",
    description="API pour scanner des vulnérabilités avec gestion utilisateur",
    version="1.0.0",
    lifespan=lifespan
)


# Middleware CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000", "http://localhost:49573"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclusion des routes

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentification"])
app.include_router(scan_routes.router, tags=["Scan"])  # ✅ Route ajoutée
app.include_router(notification_routes.router, prefix="/api/notifications", tags=["Notifications"])




#  Endpoints basiques

@app.get("/")
async def root():
    return {
        "message": "🔒 Vulnerability Scanner API",
        "version": "1.0.0",
        "database": "SQLite",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    db_status = await check_database_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }

@app.get("/test-db")
async def test_database():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(User.id)))
            user_count = result.scalar()
            return {
                "status": "success",
                "message": "Connexion à la base de données réussie",
                "users_count": user_count
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur base de données: {str(e)}")



# Lancement avec uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)



 
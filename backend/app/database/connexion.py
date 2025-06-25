import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import logging
from sqlalchemy import text 

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# URL de connexion
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas définie dans le fichier .env")

print(f"Connexion à la base de données: SQLite ({DATABASE_URL.split(':///')[1]})")

# Créer le moteur de base de données
engine = create_async_engine(
    DATABASE_URL,
    echo=True if os.getenv("DEBUG") == "True" else False,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

# Créer la factory de sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base pour les modèles ORM
Base = declarative_base()

async def get_db():
    """
    Générateur de session de base de données pour l'injection de dépendance FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def init_database():
    """
    Initialiser la base de données (créer les tables)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables de base de données créées avec succès")

async def check_database_connection():
    """
    Vérifier la connexion à la base de données
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))  
            print(" Connexion à la base de données réussie")
            return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False

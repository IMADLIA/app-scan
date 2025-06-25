#!/usr/bin/env python3
"""Script d'initialisation de la base de données"""

import asyncio
import sys
import os

# Ajouter le chemin de l'app au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database.connexion import init_database, check_database_connection, AsyncSessionLocal
from app.database.models import User, NotificationSetting

async def create_admin_user():
    """Créer un utilisateur administrateur par défaut"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        
        # Vérifier si l'admin existe déjà
        result = await session.execute(
            select(User).where(User.email == "admin@scanner.local")
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("👤 Utilisateur admin existe déjà")
            return existing_admin
        
        # Créer l'utilisateur admin
        admin = User(
            email="admin@scanner.local",
            first_name="Admin",
            last_name="Scanner",
            is_verified=True
        )
        admin.set_password("admin123")  # Changez ce mot de passe en production !
        
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        
        # Créer les paramètres de notification par défaut
        notification_settings = NotificationSetting(
            user_id=admin.id,
            email_enabled=True,
            push_enabled=False
        )
        session.add(notification_settings)
        await session.commit()
        
        print("👤 Utilisateur admin créé:")
        print(f"   📧 Email: admin@scanner.local")
        print(f"   🔑 Mot de passe: admin123")
        print("   ⚠️  CHANGEZ CE MOT DE PASSE EN PRODUCTION !")
        
        return admin

async def main():
    """Fonction principale d'initialisation"""
    print("🔄 Initialisation de la base de données...")
    
    # Vérifier la connexion
    if not await check_database_connection():
        print("❌ Impossible de se connecter à la base de données")
        print("   Vérifiez que le fichier SQLite est accessible")
        print("   et que les paramètres de connexion sont corrects")
        return False
    
    print("✅ Connexion à la base de données réussie")
    
    # Initialiser les tables
    print("🔄 Création des tables...")
    await init_database()
    
    # Créer l'utilisateur admin
    print("🔄 Création de l'utilisateur administrateur...")
    await create_admin_user()
    
    print(" Initialisation terminée avec succès !")
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
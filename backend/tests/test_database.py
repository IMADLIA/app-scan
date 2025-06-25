import pytest
import asyncio
from app.database.connexion import AsyncSessionLocal, init_database
from app.database.models import User, Scan, Vulnerability

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def db_session():
    """Fixture pour les tests de base de données"""
    await init_database()
    async with AsyncSessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test de création d'utilisateur"""
    user = User(
        email="test@scan.com",
        first_name="Test",
        last_name="User"
    )
    user.set_password("testpassword123")
    
    db_session.add(user)
    await db_session.commit()
    
    assert user.id is not None
    assert user.check_password("testpassword123")
    assert not user.check_password("wrongpassword")

@pytest.mark.asyncio
async def test_create_scan(db_session):
    """Test de création de scan"""
    # Créer un utilisateur d'abord
    user = User(email="scanner@test.com", first_name="Scanner", last_name="Test")
    user.set_password("password123")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    # Créer un scan
    scan = Scan(
        user_id=user.id,
        target_url="https://scan.com",
        scan_type="web_security",
        config='{"depth": 2}'  # SQLite utilise Text, donc JSON sous forme de chaîne
    )
    db_session.add(scan)
    await db_session.commit()
    
    assert scan.id is not None
    assert scan.status == "pending"
    assert scan.config == '{"depth": 2}'
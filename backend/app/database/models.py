import bcrypt
import jwt
import os
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .connexion import Base


# Modèle Utilisateur

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relations
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
    notification_settings = relationship("NotificationSetting", backref="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_jwt_token(self) -> str:
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, os.getenv("JWT_SECRET", "default_secret"), algorithm='HS256')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"



#  Modèle Scan

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=True)
    target_url = Column(String(500), nullable=False)
    scan_type = Column(String(50), nullable=False, index=True)
    scan_tool = Column(String(100), default="mock")
    status = Column(String(20), default="pending", index=True)
    config = Column(Text, default="{}")
    results = Column(Text, default="{}")
    raw_output = Column(Text, default="")
    report_file_path = Column(String(500), nullable=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    # Relations
    user = relationship("User", back_populates="scans")
    vulnerabilities = relationship("Vulnerability", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan(id={self.id}, target='{self.target_url}', status='{self.status}')>"



#  Modèle Vulnérabilité

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    severity = Column(String(20), nullable=False)  # Low, Medium, High, Critical
    title = Column(String(500), nullable=False)
    description = Column(Text)
    cve_id = Column(String(20))  # CVE identifier
    solution = Column(Text)
    url = Column(String(500))
    parameter = Column(String(200))
    evidence = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relations
    scan = relationship("Scan", back_populates="vulnerabilities")

    def __repr__(self):
        return f"<Vulnerability(id={self.id}, severity='{self.severity}', title='{self.title[:50]}...')>"



#  Modèle Notification

class NotificationSetting(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    push_enabled = Column(Boolean, default=False)
    email_enabled = Column(Boolean, default=True)
    webhook_url = Column(String(500))
    push_subscription = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<NotificationSetting(user_id={self.user_id}, push_enabled={self.push_enabled})>"

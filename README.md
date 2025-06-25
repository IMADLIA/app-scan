# 🔐 Application de Scan de Vulnérabilités

Cette application simule un outil de scan de vulnérabilités avec une interface Angular pour le frontend et FastAPI pour le backend.

---

## 🧪 Backend – FastAPI

### 🛠️ Technologies :
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- FPDF (génération PDF)
- CORS

### 🔧 Fonctionnalités :
- Création de scans simulés avec vulnérabilités
- Récupération des détails de chaque scan
- Génération de rapports PDF
- Gestion des préférences de notification utilisateur
- Envoi de notification manuelle

### ▶️ Démarrage du Backend :

1. Aller dans le dossier `backend` :
```bash
cd backend
```

2. Activer l’environnement virtuel (si utilisé) :
```bash
source ../venv/bin/activate       # (Linux/macOS)
# ou
.env\Scriptsctivate           # (Windows)
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancer le serveur FastAPI :
```bash
uvicorn app.main:app --reload
```

📍 Accès au backend : [http://localhost:8000](http://localhost:8000)

---

## 💻 Frontend – Angular

### 🛠️ Technologies :
- Angular 17+
- TypeScript
- SCSS
- Reactive Forms
- HTTPClient

### 🔧 Fonctionnalités :
- Formulaire de lancement de scan
- Liste des scans dans un dashboard
- Visualisation des détails
- Téléchargement de rapports PDF
- Gestion des préférences de notifications

### ▶️ Démarrage du Frontend :

1. Aller dans le dossier `frontend` :
```bash
cd frontend
```

2. Installer les dépendances :
```bash
npm install
```

3. Démarrer le serveur Angular :
```bash
ng serve
```

📍 Accès au frontend : [http://localhost:4200](http://localhost:4200)

---

## 📁 Structure du projet

```
project-root/
│
├── backend/              # FastAPI backend
│   ├── app/              # Fichiers principaux de l’API
│   ├── database.db       # SQLite DB
│   └── requirements.txt  # Dépendances
│
├── frontend/             # Application Angular
│   ├── src/
│   └── angular.json
│
└── README.md             # Documentation
```

---

## 🧑‍💻 Auteur

Développé par **Imad Liazidi**
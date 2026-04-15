# 🚀 MarketPro – Application Web de Marketing & Publicité

<div align="center">

**Application professionnelle de catalogue produits avec interface d'administration complète.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## 📋 Description

MarketPro est une application web complète de marketing et publicité de produits, construite avec Flask. Elle permet de gérer un catalogue de produits avec des catégories, des images multiples, et offre une interface d'administration intuitive.

### ✨ Fonctionnalités

- 🏠 **Page d'accueil** avec produits en vedette et derniers ajouts
- 📦 **Catalogue produits** avec catégories et filtres de recherche
- 🖼️ **Multi-photos par produit** avec carrousel interactif
- 🔍 **Recherche avancée** par nom, catégorie et prix
- 🔐 **Interface d'administration** protégée par mot de passe
- 📱 **Design responsive** adapté mobile/tablette/desktop
- ⚡ **Animations fluides** et interface moderne

---

## 📸 Captures d'écran

| Page d'accueil | Détail produit | Administration |
|:-:|:-:|:-:|
| ![Accueil](https://via.placeholder.com/300x200?text=Accueil) | ![Produit](https://via.placeholder.com/300x200?text=Produit) | ![Admin](https://via.placeholder.com/300x200?text=Admin) |

---

## 🛠️ Installation locale

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-utilisateur/marketpro.git
cd marketpro

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python app.py
```

L'application sera accessible à l'adresse : **http://localhost:5000**

### Variables d'environnement (optionnel)

```bash
export SECRET_KEY="votre-clé-secrète"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="admin123"
export FLASK_DEBUG="true"
```

---

## 🌐 Déploiement gratuit

### 🟢 Option 1 : Render.com (Recommandé)

Render.com offre un hébergement gratuit pour les applications web Python. C'est la méthode la plus simple.

#### Étape 1 : Préparer le dépôt

Assurez-vous que votre code est poussé sur GitHub avec les fichiers suivants à la racine :
- `app.py` – Application principale
- `requirements.txt` – Dépendances Python
- `Procfile` – Commande de démarrage
- `render.yaml` – Configuration Render
- `runtime.txt` – Version Python

#### Étape 2 : Créer un compte Render

1. Allez sur **[render.com](https://render.com)** et cliquez sur **"Get Started for Free"**
2. Connectez-vous avec votre compte **GitHub**
3. Autorisez Render à accéder à vos dépôts

#### Étape 3 : Créer un nouveau Web Service

1. Depuis le tableau de bord Render, cliquez sur **"New +"** → **"Web Service"**
2. Sélectionnez votre dépôt GitHub contenant MarketPro
3. Configurez les paramètres :
   - **Name** : `marketpro` (ou le nom de votre choix)
   - **Region** : Choisissez la plus proche de vous (ex: Frankfurt pour l'Europe)
   - **Branch** : `main`
   - **Runtime** : `Python`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Plan** : **Free**

#### Étape 4 : Configurer les variables d'environnement

Dans la section **"Environment Variables"**, ajoutez :

| Clé | Valeur | Description |
|-----|--------|-------------|
| `SECRET_KEY` | *(Cliquez sur "Generate")* | Clé secrète pour les sessions |
| `ADMIN_PASSWORD` | `votre_mot_de_passe` | Mot de passe admin |
| `FLASK_DEBUG` | `false` | Désactiver le mode debug |

#### Étape 5 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va automatiquement installer les dépendances et lancer l'application
3. Attendez quelques minutes que le déploiement se termine
4. Votre application sera accessible à : `https://marketpro.onrender.com`

#### 📝 Notes importantes pour Render

- Le plan gratuit met l'application en veille après 15 min d'inactivité
- Le premier chargement après une veille peut prendre ~30 secondes
- La base de données SQLite est réinitialisée à chaque déploiement (les données de démonstration sont recréées automatiquement)
- Pour une base de données persistante, considérez Render PostgreSQL (gratuit aussi)

---

### 🟣 Option 2 : Railway.app

Railway offre un déploiement simple avec un crédit gratuit mensuel.

#### Étapes

1. Allez sur **[railway.app](https://railway.app)** et connectez-vous avec GitHub
2. Cliquez sur **"New Project"** → **"Deploy from GitHub repo"**
3. Sélectionnez votre dépôt MarketPro
4. Railway détecte automatiquement Python et utilise le `Procfile`
5. Ajoutez les variables d'environnement dans l'onglet **"Variables"** :
   ```
   SECRET_KEY=une-cle-secrete-aleatoire
   ADMIN_PASSWORD=votre_mot_de_passe
   FLASK_DEBUG=false
   ```
6. Cliquez sur **"Deploy"**
7. Dans **"Settings"** → **"Networking"**, cliquez sur **"Generate Domain"** pour obtenir une URL publique

#### 📝 Notes Railway

- Railway offre 5$ de crédit gratuit par mois (suffisant pour un petit projet)
- Pas de mise en veille automatique
- Support des bases de données PostgreSQL et MySQL

---

### 🟡 Option 3 : PythonAnywhere

PythonAnywhere est idéal pour les débutants avec une interface entièrement web.

#### Étape 1 : Créer un compte

1. Allez sur **[pythonanywhere.com](https://www.pythonanywhere.com)** et créez un compte gratuit (Beginner)

#### Étape 2 : Uploader le code

1. Allez dans l'onglet **"Files"**
2. Créez un dossier `marketpro`
3. Uploadez tous les fichiers du projet dans ce dossier
4. Ou utilisez la console Bash pour cloner depuis GitHub :
   ```bash
   git clone https://github.com/votre-utilisateur/marketpro.git
   ```

#### Étape 3 : Installer les dépendances

1. Ouvrez une **Console Bash** depuis l'onglet "Consoles"
2. Exécutez :
   ```bash
   cd marketpro
   pip3 install --user -r requirements.txt
   ```

#### Étape 4 : Configurer l'application web

1. Allez dans l'onglet **"Web"**
2. Cliquez sur **"Add a new web app"**
3. Choisissez **"Manual configuration"** → **Python 3.11**
4. Dans **"Source code"**, indiquez : `/home/votre-username/marketpro`
5. Dans **"WSGI configuration file"**, cliquez pour éditer et remplacez le contenu par :
   ```python
   import sys
   sys.path.insert(0, '/home/votre-username/marketpro')
   from app import app as application
   ```
6. Dans **"Virtualenv"**, vous pouvez laisser vide si vous avez utilisé `--user`

#### Étape 5 : Variables d'environnement

1. Dans l'onglet "Web", section **"Environment variables"** (ou fichier `.env`)
2. Ajoutez vos variables :
   ```
   SECRET_KEY=une-cle-secrete
   ADMIN_PASSWORD=votre_mot_de_passe
   ```

#### Étape 6 : Lancer

1. Cliquez sur **"Reload"** dans l'onglet Web
2. Votre app est accessible à : `https://votre-username.pythonanywhere.com`

#### 📝 Notes PythonAnywhere

- Le plan gratuit inclut un seul site web
- Domaine `votre-username.pythonanywhere.com`
- Fichiers persistants (la base SQLite est conservée)
- Rechargement quotidien nécessaire pour le plan gratuit

---

### 🔵 Option 4 : Fly.io

Fly.io offre des performances excellentes avec un déploiement via CLI.

#### Étape 1 : Installer flyctl

```bash
# Linux
curl -L https://fly.io/install.sh | sh

# macOS
brew install flyctl

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### Étape 2 : Se connecter

```bash
fly auth signup  # Créer un compte
# ou
fly auth login   # Se connecter
```

#### Étape 3 : Lancer le déploiement

```bash
cd marketpro

# Initialiser l'application Fly
fly launch
# Suivez les instructions :
# - Nom de l'app : marketpro (ou autre)
# - Région : choisissez la plus proche
# - Ne pas créer de base de données PostgreSQL
# - Ne pas déployer maintenant
```

#### Étape 4 : Configurer les secrets

```bash
fly secrets set SECRET_KEY="une-cle-secrete-aleatoire"
fly secrets set ADMIN_PASSWORD="votre_mot_de_passe"
fly secrets set FLASK_DEBUG="false"
```

#### Étape 5 : Déployer

```bash
fly deploy
```

Votre application sera accessible à : `https://marketpro.fly.dev`

#### 📝 Notes Fly.io

- Plan gratuit avec 3 machines virtuelles partagées
- Pas de mise en veille
- Excellentes performances globales
- Nécessite une carte bancaire pour l'inscription (pas de facturation pour le plan gratuit)

---

## 🔐 Accès Administrateur

| Paramètre | Valeur par défaut |
|-----------|-------------------|
| **URL** | `/admin/login` |
| **Nom d'utilisateur** | `admin` |
| **Mot de passe** | `admin123` |

> ⚠️ **Important** : Changez le mot de passe par défaut en production via la variable d'environnement `ADMIN_PASSWORD`.

---

## ⚙️ Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SECRET_KEY` | Clé secrète pour les sessions Flask | `marketing-app-secret-2024` |
| `ADMIN_USERNAME` | Nom d'utilisateur admin | `admin` |
| `ADMIN_PASSWORD` | Mot de passe admin | `admin123` |
| `FLASK_DEBUG` | Mode debug (`true`/`false`) | `false` |

---

## 📁 Structure du projet

```
marketpro/
├── app.py                  # Application Flask principale
├── requirements.txt        # Dépendances Python
├── Procfile                # Commande de démarrage (Render/Heroku)
├── render.yaml             # Configuration Render.com
├── runtime.txt             # Version Python
├── .gitignore
├── README.md
├── static/
│   ├── css/
│   │   ├── style.css       # Styles client
│   │   └── admin.css       # Styles administration
│   ├── js/
│   │   ├── main.js         # JavaScript client
│   │   └── admin.js        # JavaScript administration
│   ├── img/
│   │   └── placeholder.svg # Image par défaut
│   └── uploads/            # Images uploadées
│       └── .gitkeep
└── templates/
    ├── base.html           # Template de base
    ├── index.html          # Page d'accueil
    ├── product.html        # Détail produit (avec carrousel)
    ├── category.html       # Page catégorie
    ├── search.html         # Page recherche
    └── admin/
        ├── base_admin.html # Template admin
        ├── login.html      # Connexion admin
        ├── dashboard.html  # Tableau de bord
        ├── products.html   # Liste produits
        ├── product_form.html # Formulaire produit (multi-photos)
        └── categories.html # Gestion catégories
```

---

## 🧰 Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| **Flask 3.1** | Framework web Python |
| **SQLAlchemy** | ORM pour la base de données |
| **SQLite** | Base de données légère |
| **Jinja2** | Moteur de templates |
| **Gunicorn** | Serveur WSGI de production |
| **Pillow** | Traitement d'images |
| **HTML5/CSS3** | Interface utilisateur |
| **JavaScript** | Interactions côté client |
| **Font Awesome** | Icônes |

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">
  Fait avec ❤️ par l'équipe MarketPro
</div>

# MarketPro – Application Web de Marketing de Produits

Une application web professionnelle pour la publicité et le marketing de produits, construite avec **Flask** et **SQLAlchemy**.

## 🚀 Fonctionnalités

### Interface Client (Public)
- 🏠 Page d'accueil avec hero animé et statistiques
- 🃏 Affichage des produits en cartes avec animations fluides
- 🔍 Recherche et filtrage par catégorie et prix
- 📱 Design responsive (mobile, tablette, desktop)
- 🔗 Partage sur WhatsApp, Facebook, Twitter
- ⭐ Produits en vedette mis en avant

### Interface Admin (Protégée)
- 🔐 Authentification sécurisée
- 📊 Dashboard avec statistiques en temps réel
- ➕ Ajouter / modifier / supprimer des produits
- 🖼️ Upload d'images avec aperçu et drag & drop
- 🏷️ Gestion des catégories avec icônes FontAwesome
- ⭐ Toggle produits en vedette
- 📦 Gestion du stock

## 🛠️ Technologies

- **Backend**: Flask 3.x + SQLAlchemy
- **Base de données**: SQLite
- **Frontend**: HTML5, CSS3 (Animations CSS), JavaScript vanilla
- **Icônes**: FontAwesome 6
- **Polices**: Google Fonts (Inter)

## 📦 Installation

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
python app.py
```

L'application sera accessible sur **http://localhost:5000**

## 🔑 Accès Admin

- URL: `http://localhost:5000/admin/login`
- Nom d'utilisateur: `admin`
- Mot de passe: `admin123`

> ⚠️ Changez le mot de passe via la variable d'environnement `ADMIN_PASSWORD` en production.

## ⚙️ Variables d'Environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `SECRET_KEY` | `marketing-app-secret-2024` | Clé secrète Flask |
| `ADMIN_USERNAME` | `admin` | Nom d'utilisateur admin |
| `ADMIN_PASSWORD` | `admin123` | Mot de passe admin |

## 📁 Structure du Projet

```
projet/
├── app.py                  # Application Flask principale
├── requirements.txt        # Dépendances Python
├── products.db             # Base de données SQLite (auto-créée)
├── static/
│   ├── css/
│   │   ├── style.css       # CSS client (animations, design)
│   │   └── admin.css       # CSS interface admin
│   ├── js/
│   │   ├── main.js         # JavaScript client
│   │   └── admin.js        # JavaScript admin
│   ├── img/
│   │   └── placeholder.svg # Image par défaut
│   └── uploads/            # Images uploadées
└── templates/
    ├── base.html           # Template de base (client)
    ├── index.html          # Page d'accueil
    ├── category.html       # Page catégorie
    ├── product.html        # Détail produit
    ├── search.html         # Recherche
    └── admin/
        ├── login.html      # Page de connexion
        ├── base_admin.html # Template de base admin
        ├── dashboard.html  # Tableau de bord
        ├── products.html   # Liste des produits
        ├── product_form.html # Formulaire produit
        └── categories.html # Gestion catégories
```

## 🚀 Déploiement

Pour déployer sur un serveur de production:

```bash
# Utiliser Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Avec variables d'environnement
SECRET_KEY=votre-cle-secrete ADMIN_PASSWORD=mot-de-passe-fort gunicorn -w 4 app:app
```

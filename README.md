# WorkStamp API

WorkStamp API est une API RESTful permettant de gérer et suivre le temps de travail.

## Fonctionnalités

- Gestion des utilisateurs
- Suivi des heures de travail
- Calcul du salaire

## Installation

```bash
git clone https://github.com/nicomeuwly/WorkStamp-API.git
cd WorkStamp-API
python3 -m venv .venv
source .venv/bin/activate           
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn app.main:app --reload 
```

## Migrations Alembic

Après une modification des modèles de la base de données, il faut exécuter les commandes suivantes pour que les changements se fassent concrètement dans la base de données :

- Générer une migration : `alembic revision --autogenerate -m "Information sur la migration"`
- Appliquer la migration : `alembic upgrade head`

Plus d'infos ici : [FastAPI SQLAlchemy Migrations Guide](https://fastapi.blog/blog/posts/2023-07-20-fastapi-sqlalchemy-migrations-guide/)

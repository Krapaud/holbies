# Commandes du projet Holbies

Voici la liste des commandes utiles pour le projet, à exécuter depuis la racine du dépôt :

## Docker

- `sudo docker-compose up --build`
  - Lance tous les services (web et base de données) avec reconstruction des images si besoin.
- `sudo docker-compose down`
  - Arrête et supprime tous les conteneurs, réseaux et volumes anonymes créés par `up`.
- `sudo docker-compose exec web python scripts/delete_all_users.py`
  - Supprime tous les utilisateurs de la base de données.

## Scripts de gestion

- `python scripts/create_admin.py`
  - Crée un utilisateur administrateur dans la base.
- `python scripts/create_test_user.py`
  - Crée un utilisateur de test.
- `python scripts/reset_db.py`
  - Réinitialise la base de données (attention, destructive !).
- `python scripts/init_db.py`
  - Initialise la base de données.
- `python scripts/complete_reset_db.py`
  - Réinitialisation complète de la base de données.
- `python scripts/populate_db_balanced.py`
  - Remplit la base avec des données équilibrées.

## Autres

- `python main.py`
  - Lance l’application en mode local (hors Docker).

> Pour toute commande nécessitant l’accès à la base, assurez-vous que le service `db` est démarré.

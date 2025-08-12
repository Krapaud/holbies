-- Script d'initialisation de la base de données
-- Ce fichier sera exécuté automatiquement lors de la création du conteneur PostgreSQL

-- Créer la base de données si elle n'existe pas déjà
-- (PostgreSQL crée automatiquement la DB spécifiée dans POSTGRES_DB)

-- Créer des extensions utiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Créer un schéma pour l'application si nécessaire
-- CREATE SCHEMA IF NOT EXISTS holberton;

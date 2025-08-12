#!/usr/bin/env python3
"""
Menu interactif pour la gestion des utilisateurs et de l'administration
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

# Configuration du hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)

def clear_screen():
    """Efface l'écran"""
    print("\n" * 50)

def show_header():
    """Affiche l'en-tête du menu"""
    print("🎯" + "=" * 60 + "🎯")
    print("🚀           MENU ADMINISTRATEUR HOLBIES           🚀")
    print("🎯" + "=" * 60 + "🎯")
    print()

def list_all_users():
    """Liste tous les utilisateurs"""
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id).all()
        
        print("👥 LISTE DES UTILISATEURS")
        print("=" * 50)
        
        if not users:
            print("📭 Aucun utilisateur trouvé")
            return
        
        print(f"📊 Total: {len(users)} utilisateur(s)\n")
        
        for user in users:
            admin_badge = "👑 ADMIN" if getattr(user, 'is_admin', False) else "👤 USER"
            status = "✅" if user.is_active else "❌"
            created = user.created_at.strftime("%d/%m/%Y") if user.created_at else "N/A"
            
            print(f"{admin_badge} | {status} | ID:{user.id:2d} | {user.username:15s} | {user.email:25s} | {created}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

def create_user():
    """Crée un nouvel utilisateur"""
    db = SessionLocal()
    try:
        print("✨ CRÉATION D'UN NOUVEL UTILISATEUR")
        print("-" * 40)
        
        username = input("👤 Nom d'utilisateur: ").strip()
        if not username:
            print("❌ Le nom d'utilisateur ne peut pas être vide")
            return
        
        email = input("📧 Email: ").strip()
        if not email:
            print("❌ L'email ne peut pas être vide")
            return
        
        password = input("🔐 Mot de passe: ").strip()
        if not password:
            print("❌ Le mot de passe ne peut pas être vide")
            return
        
        is_admin_input = input("👑 Administrateur ? (o/N): ").strip().lower()
        is_admin = is_admin_input in ['o', 'oui', 'y', 'yes']
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print("❌ Un utilisateur avec ce nom ou cet email existe déjà")
            return
        
        # Créer l'utilisateur
        hashed_pwd = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_pwd,
            is_active=True
        )
        
        # Ajouter le champ is_admin si la migration a été faite
        try:
            setattr(new_user, 'is_admin', is_admin)
        except:
            pass
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        role = "👑 Administrateur" if is_admin else "👤 Utilisateur"
        print(f"✅ Utilisateur créé avec succès!")
        print(f"   ID: {new_user.id}")
        print(f"   Nom: {username}")
        print(f"   Email: {email}")
        print(f"   Rôle: {role}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
    finally:
        db.close()

def delete_user():
    """Supprime un utilisateur"""
    db = SessionLocal()
    try:
        list_all_users()
        print("\n🗑️  SUPPRESSION D'UTILISATEUR")
        print("-" * 30)
        
        user_id = input("ID de l'utilisateur à supprimer: ").strip()
        if not user_id.isdigit():
            print("❌ ID invalide")
            return
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            print("❌ Utilisateur introuvable")
            return
        
        print(f"⚠️  Vous allez supprimer: {user.username} ({user.email})")
        confirm = input("Confirmer la suppression (tapez 'SUPPRIMER'): ").strip()
        
        if confirm != "SUPPRIMER":
            print("❌ Suppression annulée")
            return
        
        db.delete(user)
        db.commit()
        print("✅ Utilisateur supprimé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        db.rollback()
    finally:
        db.close()

def toggle_admin_status():
    """Active/Désactive le statut admin d'un utilisateur"""
    db = SessionLocal()
    try:
        # D'abord, essayons d'ajouter la colonne is_admin si elle n'existe pas
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
            db.commit()
            print("✅ Colonne is_admin ajoutée")
        except:
            # La colonne existe déjà
            pass
        
        list_all_users()
        print("\n👑 GESTION DES DROITS ADMINISTRATEUR")
        print("-" * 40)
        
        user_id = input("ID de l'utilisateur: ").strip()
        if not user_id.isdigit():
            print("❌ ID invalide")
            return
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            print("❌ Utilisateur introuvable")
            return
        
        # Utiliser une requête SQL directe pour mettre à jour is_admin
        current_admin = False
        try:
            result = db.execute(text("SELECT is_admin FROM users WHERE id = :id"), {"id": user.id}).fetchone()
            current_admin = result[0] if result else False
        except:
            pass
        
        new_status = not current_admin
        status_text = "👑 Administrateur" if new_status else "👤 Utilisateur standard"
        
        print(f"👤 Utilisateur: {user.username}")
        print(f"📋 Statut actuel: {'👑 Admin' if current_admin else '👤 User'}")
        print(f"📋 Nouveau statut: {status_text}")
        
        confirm = input("Confirmer le changement (o/N): ").strip().lower()
        if confirm not in ['o', 'oui', 'y', 'yes']:
            print("❌ Changement annulé")
            return
        
        # Mettre à jour via SQL direct
        db.execute(text("UPDATE users SET is_admin = :is_admin WHERE id = :id"), 
                  {"is_admin": new_status, "id": user.id})
        db.commit()
        
        print(f"✅ Statut mis à jour: {user.username} est maintenant {status_text}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def clear_all_users():
    """Vide tous les utilisateurs"""
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        
        if user_count == 0:
            print("📭 Aucun utilisateur à supprimer")
            return
        
        print(f"⚠️  ATTENTION: Suppression de {user_count} utilisateur(s)")
        print("🚨 Cette action est IRRÉVERSIBLE!")
        confirm = input("Tapez 'VIDER TOUT' pour confirmer: ").strip()
        
        if confirm != "VIDER TOUT":
            print("❌ Suppression annulée")
            return
        
        deleted = db.query(User).delete()
        db.commit()
        print(f"✅ {deleted} utilisateur(s) supprimé(s)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_data():
    """Crée des données de test"""
    db = SessionLocal()
    try:
        print("🧪 CRÉATION DE DONNÉES DE TEST")
        print("-" * 30)
        
        # Vérifier s'il y a déjà des utilisateurs
        existing_count = db.query(User).count()
        if existing_count > 0:
            print(f"⚠️  Il y a déjà {existing_count} utilisateur(s)")
            confirm = input("Continuer quand même ? (o/N): ").strip().lower()
            if confirm not in ['o', 'oui', 'y', 'yes']:
                print("❌ Annulé")
                return
        
        # Données de test
        test_users = [
            ("admin", "admin@holbies.dev", "admin123", True),
            ("student1", "student1@holbies.dev", "student123", False),
            ("student2", "student2@holbies.dev", "student123", False),
            ("teacher", "teacher@holbies.dev", "teacher123", True),
            ("demo_user", "demo@holbies.dev", "demo123", False),
        ]
        
        created_count = 0
        for username, email, password, is_admin in test_users:
            # Vérifier si l'utilisateur existe déjà
            existing = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing:
                print(f"⏭️  {username} existe déjà, ignoré")
                continue
            
            # Créer l'utilisateur
            hashed_pwd = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                hashed_password=hashed_pwd,
                is_active=True
            )
            
            db.add(new_user)
            db.flush()  # Pour obtenir l'ID
            
            # Ajouter le statut admin via SQL direct
            try:
                db.execute(text("UPDATE users SET is_admin = :is_admin WHERE id = :id"), 
                          {"is_admin": is_admin, "id": new_user.id})
            except:
                pass
            
            created_count += 1
            role = "👑 Admin" if is_admin else "👤 User"
            print(f"✅ {username} ({role})")
        
        db.commit()
        print(f"\n🎯 {created_count} utilisateur(s) de test créé(s)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def show_database_stats():
    """Affiche les statistiques de la base de données"""
    db = SessionLocal()
    try:
        print("📊 STATISTIQUES DE LA BASE DE DONNÉES")
        print("=" * 40)
        
        # Statistiques des utilisateurs
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        
        # Compter les admins (avec gestion d'erreur)
        admin_count = 0
        try:
            result = db.execute(text("SELECT COUNT(*) FROM users WHERE is_admin = true")).fetchone()
            admin_count = result[0] if result else 0
        except:
            pass
        
        print(f"👥 Utilisateurs totaux: {total_users}")
        print(f"✅ Utilisateurs actifs: {active_users}")
        print(f"❌ Utilisateurs inactifs: {total_users - active_users}")
        print(f"👑 Administrateurs: {admin_count}")
        print(f"👤 Utilisateurs standard: {total_users - admin_count}")
        
        # Autres statistiques si les tables existent
        try:
            quiz_sessions = db.execute(text("SELECT COUNT(*) FROM quiz_sessions")).fetchone()[0]
            questions = db.execute(text("SELECT COUNT(*) FROM questions")).fetchone()[0]
            print(f"🎯 Sessions de quiz: {quiz_sessions}")
            print(f"❓ Questions: {questions}")
        except:
            print("🎯 Sessions de quiz: Table non trouvée")
            print("❓ Questions: Table non trouvée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

def main_menu():
    """Menu principal"""
    while True:
        clear_screen()
        show_header()
        show_database_stats()
        
        print("\n🎮 MENU PRINCIPAL")
        print("=" * 20)
        print("1️⃣  📋 Lister les utilisateurs")
        print("2️⃣  ✨ Créer un utilisateur")
        print("3️⃣  🗑️  Supprimer un utilisateur")
        print("4️⃣  👑 Gérer les droits admin")
        print("5️⃣  🧪 Créer des données de test")
        print("6️⃣  🗑️  Vider tous les utilisateurs")
        print("7️⃣  📊 Actualiser les statistiques")
        print("0️⃣  🚪 Quitter")
        print()
        
        choice = input("🎯 Votre choix: ").strip()
        
        print("\n" + "="*60)
        
        if choice == "1":
            list_all_users()
        elif choice == "2":
            create_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            toggle_admin_status()
        elif choice == "5":
            create_test_data()
        elif choice == "6":
            clear_all_users()
        elif choice == "7":
            continue  # Rafraîchit l'affichage
        elif choice == "0":
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")
        
        if choice != "0" and choice != "7":
            input("\n⏎ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()

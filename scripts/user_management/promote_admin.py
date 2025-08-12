#!/usr/bin/env python3
"""
Script pour promouvoir un utilisateur en administrateur
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User

def promote_to_admin(username_or_id):
    """Promeut un utilisateur en administrateur"""
    db = SessionLocal()
    
    try:
        # Chercher l'utilisateur par nom ou ID
        if username_or_id.isdigit():
            user = db.query(User).filter(User.id == int(username_or_id)).first()
        else:
            user = db.query(User).filter(User.username == username_or_id).first()
        
        if not user:
            print(f"❌ Utilisateur '{username_or_id}' introuvable")
            return
        
        # Vérifier s'il est déjà admin
        try:
            result = db.execute(text("SELECT is_admin FROM users WHERE id = :id"), {"id": user.id}).fetchone()
            is_already_admin = result[0] if result else False
        except:
            is_already_admin = False
        
        if is_already_admin:
            print(f"👑 {user.username} est déjà administrateur")
            return
        
        # Promouvoir en admin
        db.execute(text("UPDATE users SET is_admin = true WHERE id = :id"), {"id": user.id})
        db.commit()
        
        print(f"✅ {user.username} ({user.email}) promu administrateur avec succès!")
        print(f"🔑 Identifiants admin: {user.username} / [mot de passe existant]")
        print(f"🌐 Accès admin: http://localhost:8000/api/users/admin/dashboard")
        
    except Exception as e:
        print(f"❌ Erreur lors de la promotion: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def list_admins():
    """Liste tous les administrateurs"""
    db = SessionLocal()
    
    try:
        print("👑 LISTE DES ADMINISTRATEURS")
        print("=" * 30)
        
        # Récupérer tous les admins
        try:
            admin_users = db.execute(text("""
                SELECT id, username, email, is_active, created_at 
                FROM users 
                WHERE is_admin = true 
                ORDER BY id
            """)).fetchall()
        except:
            print("❌ Erreur lors de la récupération des admins")
            return
        
        if not admin_users:
            print("📭 Aucun administrateur trouvé")
            print("\n💡 Pour créer un admin:")
            print("   docker-compose exec web python /app/promote_admin.py admin")
            return
        
        for admin in admin_users:
            status = "✅ Actif" if admin[3] else "❌ Inactif"
            created = admin[4].strftime("%d/%m/%Y") if admin[4] else "N/A"
            print(f"👑 ID:{admin[0]:2d} | {admin[1]:15s} | {admin[2]:25s} | {status} | {created}")
        
        print(f"\n🎯 Total: {len(admin_users)} administrateur(s)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("👑 GESTION DES ADMINISTRATEURS")
    print("=" * 35)
    
    if len(sys.argv) < 2:
        print("📋 Usage:")
        print("   Promouvoir un utilisateur: python /app/promote_admin.py <username_ou_id>")
        print("   Lister les admins:        python /app/promote_admin.py --list")
        print("\n📋 Exemples:")
        print("   python /app/promote_admin.py admin")
        print("   python /app/promote_admin.py teacher")
        print("   python /app/promote_admin.py 10")
        print("   python /app/promote_admin.py --list")
        
        # Afficher les utilisateurs disponibles
        db = SessionLocal()
        try:
            users = db.query(User).order_by(User.id).all()
            if users:
                print(f"\n👥 UTILISATEURS DISPONIBLES ({len(users)}):")
                print("-" * 40)
                for user in users:
                    try:
                        result = db.execute(text("SELECT is_admin FROM users WHERE id = :id"), {"id": user.id}).fetchone()
                        is_admin = result[0] if result else False
                        role = "👑 Admin" if is_admin else "👤 User"
                        print(f"   {role} | ID:{user.id:2d} | {user.username}")
                    except:
                        print(f"   👤 User  | ID:{user.id:2d} | {user.username}")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des utilisateurs: {e}")
        finally:
            db.close()
        
        sys.exit(0)
    
    if sys.argv[1] == "--list":
        list_admins()
    else:
        username_or_id = sys.argv[1]
        promote_to_admin(username_or_id)

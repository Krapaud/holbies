
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import SessionLocal
from app.models import User

def delete_all_users():
    db = SessionLocal()
    try:
        num_deleted = db.query(User).delete()
        db.commit()
        print(f"{num_deleted} utilisateurs supprimés.")
    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    delete_all_users()

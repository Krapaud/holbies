import os
import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_securisee'  # À changer en production !
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Créer un index pour les performances
    conn.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_email ON users(email)')
    
    # Vérifier si l'admin existe déjà
    admin = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin:
        # Créer le compte administrateur par défaut
        admin_password = hash_password('admin123')
        conn.execute('''
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@geeksite.com', admin_password, True))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash un mot de passe avec SHA-256 et salt"""
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash

def verify_password(stored_password, provided_password):
    """Vérifie un mot de passe"""
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            flash('Tous les champs sont requis', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()
        
        if existing_user:
            flash('Nom d\'utilisateur ou email déjà utilisé', 'error')
            conn.close()
            return render_template('register.html')
        
        # Créer le nouvel utilisateur
        password_hash = hash_password(password)
        conn.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        
        conn.commit()
        conn.close()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        
        if user and verify_password(user['password_hash'], password):
            # Mettre à jour la dernière connexion
            conn.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now(), user['id'])
            )
            conn.commit()
            
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            flash('Connexion réussie !', 'success')
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
        
        conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    
    # Statistiques pour le dashboard
    total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html', user=user, total_users=total_users)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    users = conn.execute(
        'SELECT * FROM users ORDER BY created_at DESC'
    ).fetchall()
    
    # Statistiques pour l'admin
    stats = {
        'total_users': len(users),
        'admin_users': len([u for u in users if u['is_admin']]),
        'recent_logins': len([u for u in users if u['last_login']])
    }
    
    conn.close()
    
    return render_template('admin.html', users=users, stats=stats)

@app.route('/admin/toggle_admin/<int:user_id>')
def toggle_admin(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    new_admin_status = not user['is_admin']
    conn.execute(
        'UPDATE users SET is_admin = ? WHERE id = ?',
        (new_admin_status, user_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'new_status': new_admin_status})

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    # Empêcher la suppression de son propre compte
    if user_id == session['user_id']:
        return jsonify({'error': 'Impossible de supprimer votre propre compte'}), 400
    
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)

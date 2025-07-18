import os
import sqlite3
import hashlib
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from quiz_data import questions, answers, categories

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
            last_login TIMESTAMP,
            level INTEGER DEFAULT 1,
            xp_points INTEGER DEFAULT 0,
            total_quizzes INTEGER DEFAULT 0,
            total_correct_answers INTEGER DEFAULT 0,
            best_category TEXT DEFAULT '',
            completion_rate REAL DEFAULT 0.0
        )
    ''')
    
    # Table pour les scores de quiz
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            time_taken INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Table pour suivre les badges et achievements
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_type TEXT NOT NULL,
            achievement_name TEXT NOT NULL,
            description TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Ajouter les colonnes manquantes si elles n'existent pas (migration)
    try:
        conn.execute('ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1')
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN xp_points INTEGER DEFAULT 0')
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN total_quizzes INTEGER DEFAULT 0')
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN total_correct_answers INTEGER DEFAULT 0')
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN best_category TEXT DEFAULT ""')
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN completion_rate REAL DEFAULT 0.0')
    except:
        pass
    try:
        conn.execute('ALTER TABLE quiz_scores ADD COLUMN percentage REAL DEFAULT 0.0')
    except:
        pass
    try:
        conn.execute('ALTER TABLE quiz_scores ADD COLUMN time_taken INTEGER DEFAULT 0')
    except:
        pass
    
    # Créer un index pour les performances
    conn.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_email ON users(email)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_user_scores ON quiz_scores(user_id)')
    
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

def calculate_level(xp_points):
    """Calcule le niveau basé sur les points XP"""
    # Système de progression exponentiel : niveau = sqrt(xp / 100)
    if xp_points <= 0:
        return 1
    return min(100, max(1, int((xp_points / 100) ** 0.5) + 1))

def calculate_xp_for_quiz(score, total_questions, category_difficulty=1.0):
    """Calcule les points XP gagnés pour un quiz"""
    base_xp = 10  # XP de base par question
    percentage = (score / total_questions) * 100
    
    # Bonus basé sur le pourcentage
    if percentage >= 90:
        bonus_multiplier = 2.0
    elif percentage >= 80:
        bonus_multiplier = 1.5
    elif percentage >= 70:
        bonus_multiplier = 1.2
    elif percentage >= 60:
        bonus_multiplier = 1.0
    else:
        bonus_multiplier = 0.5
    
    # Calcul final avec difficulté de la catégorie
    total_xp = int(base_xp * total_questions * bonus_multiplier * category_difficulty)
    return total_xp

def update_user_progression(user_id, score, total_questions, category, percentage):
    """Met à jour la progression de l'utilisateur après un quiz"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    
    # Récupérer les stats actuelles
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return
    
    # Calculer nouveaux XP
    category_difficulty = get_category_difficulty(category)
    new_xp = calculate_xp_for_quiz(score, total_questions, category_difficulty)
    
    # Calculer nouvelles stats en utilisant les noms de colonnes
    current_xp = user['xp_points'] if user['xp_points'] else 0
    current_level = user['level'] if user['level'] else 1
    current_quizzes = user['total_quizzes'] if user['total_quizzes'] else 0
    current_correct = user['total_correct_answers'] if user['total_correct_answers'] else 0
    
    total_xp = current_xp + new_xp
    new_level = calculate_level(total_xp)
    total_quizzes = current_quizzes + 1
    total_correct = current_correct + score
    
    # Calculer taux de réussite global
    total_questions_answered = conn.execute(
        'SELECT SUM(total_questions) FROM quiz_scores WHERE user_id = ?', 
        (user_id,)
    ).fetchone()[0] or 0
    total_questions_answered += total_questions
    
    completion_rate = (total_correct / total_questions_answered) * 100 if total_questions_answered > 0 else 0
    
    # Déterminer la meilleure catégorie
    best_category = get_best_category(user_id, conn)
    
    # Mettre à jour l'utilisateur
    conn.execute('''
        UPDATE users 
        SET level = ?, xp_points = ?, total_quizzes = ?, total_correct_answers = ?, 
            completion_rate = ?, best_category = ?
        WHERE id = ?
    ''', (new_level, total_xp, total_quizzes, total_correct, completion_rate, best_category, user_id))
    
    # Vérifier et attribuer des achievements
    check_and_award_achievements(user_id, conn, new_level, total_quizzes, completion_rate, percentage)
    
    conn.commit()
    conn.close()
    
    return {
        'xp_gained': new_xp,
        'new_level': new_level,
        'total_xp': total_xp,
        'level_up': new_level > current_level
    }

def get_category_difficulty(category):
    """Retourne le multiplicateur de difficulté pour chaque catégorie"""
    difficulty_map = {
        'Notions de base': 1.0,
        'Variables et types': 1.1,
        'Structures de contrôle': 1.2,
        'Fonctions': 1.3,
        'Tableaux': 1.4,
        'Pointeurs': 1.6,
        'Structures': 1.5,
        'Fichiers': 1.7,
        'Allocation mémoire': 1.8,
        'Concepts avancés': 2.0
    }
    return difficulty_map.get(category, 1.0)

def get_best_category(user_id, conn):
    """Détermine la meilleure catégorie de l'utilisateur"""
    categories = conn.execute('''
        SELECT category, AVG(percentage) as avg_score, COUNT(*) as attempts
        FROM quiz_scores 
        WHERE user_id = ? 
        GROUP BY category
        HAVING attempts >= 2
        ORDER BY avg_score DESC, attempts DESC
        LIMIT 1
    ''', (user_id,)).fetchone()
    
    return categories[0] if categories else ''

def check_and_award_achievements(user_id, conn, level, total_quizzes, completion_rate, last_percentage):
    """Vérifie et attribue des achievements à l'utilisateur"""
    achievements = []
    
    # Achievement: Premier quiz
    if total_quizzes == 1:
        achievements.append(('first_quiz', 'Premier Quiz', 'Félicitations pour votre premier quiz !'))
    
    # Achievement: Niveaux
    level_achievements = {
        5: ('level_5', 'Apprenti', 'Vous avez atteint le niveau 5 !'),
        10: ('level_10', 'Développeur Junior', 'Vous avez atteint le niveau 10 !'),
        20: ('level_20', 'Développeur Confirmé', 'Vous avez atteint le niveau 20 !'),
        50: ('level_50', 'Expert C', 'Vous avez atteint le niveau 50 !')
    }
    
    if level in level_achievements:
        achievements.append(level_achievements[level])
    
    # Achievement: Quiz complets
    quiz_achievements = {
        5: ('quiz_5', 'Persévérant', '5 quiz complétés !'),
        10: ('quiz_10', 'Assidu', '10 quiz complétés !'),
        25: ('quiz_25', 'Dévoué', '25 quiz complétés !'),
        50: ('quiz_50', 'Maître Quiz', '50 quiz complétés !')
    }
    
    if total_quizzes in quiz_achievements:
        achievements.append(quiz_achievements[total_quizzes])
    
    # Achievement: Scores parfaits
    if last_percentage == 100:
        achievements.append(('perfect_score', 'Score Parfait', 'Quiz réussi à 100% !'))
    
    # Achievement: Taux de réussite
    if completion_rate >= 90:
        achievements.append(('high_performer', 'Excellent Élève', 'Plus de 90% de réussite globale !'))
    elif completion_rate >= 80:
        achievements.append(('good_performer', 'Bon Élève', 'Plus de 80% de réussite globale !'))
    
    # Insérer les nouveaux achievements
    for achievement in achievements:
        # Vérifier si l'achievement n'existe pas déjà
        existing = conn.execute(
            'SELECT id FROM user_achievements WHERE user_id = ? AND achievement_type = ?',
            (user_id, achievement[0])
        ).fetchone()
        
        if not existing:
            conn.execute('''
                INSERT INTO user_achievements (user_id, achievement_type, achievement_name, description)
                VALUES (?, ?, ?, ?)
            ''', (user_id, achievement[0], achievement[1], achievement[2]))

def get_user_achievements(user_id):
    """Récupère tous les achievements d'un utilisateur"""
    conn = sqlite3.connect('users.db')
    achievements = conn.execute('''
        SELECT achievement_name, description, earned_at 
        FROM user_achievements 
        WHERE user_id = ? 
        ORDER BY earned_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return achievements

def get_xp_for_next_level(current_level):
    """Calcule les XP nécessaires pour le niveau suivant"""
    next_level = current_level + 1
    return (next_level - 1) ** 2 * 100

def get_level_progress(xp_points, level):
    """Calcule le pourcentage de progression vers le niveau suivant"""
    current_level_xp = (level - 1) ** 2 * 100
    next_level_xp = level ** 2 * 100
    
    if next_level_xp - current_level_xp == 0:
        return 100
    
    progress = ((xp_points - current_level_xp) / (next_level_xp - current_level_xp)) * 100
    return max(0, min(100, progress))

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
    
    # Statistiques de quiz pour l'utilisateur
    quiz_stats = conn.execute('''
        SELECT 
            COUNT(*) as total_quizzes,
            AVG(CAST(score AS FLOAT) / total_questions * 100) as avg_percentage,
            MAX(CAST(score AS FLOAT) / total_questions * 100) as best_percentage
        FROM quiz_scores 
        WHERE user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    # Derniers scores
    recent_scores = conn.execute('''
        SELECT category, score, total_questions, completed_at, percentage
        FROM quiz_scores 
        WHERE user_id = ? 
        ORDER BY completed_at DESC 
        LIMIT 3
    ''', (session['user_id'],)).fetchall()
    
    # Statistiques de progression
    level_progress = get_level_progress(user['xp_points'], user['level'])
    xp_for_next = get_xp_for_next_level(user['level'])
    
    # Récupérer les achievements récents
    user_achievements = get_user_achievements(session['user_id'])
    
    # Calcul des statistiques par catégorie
    category_stats = conn.execute('''
        SELECT 
            category,
            COUNT(*) as attempts,
            AVG(percentage) as avg_score,
            MAX(percentage) as best_score
        FROM quiz_scores 
        WHERE user_id = ?
        GROUP BY category
        ORDER BY avg_score DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         user=user, 
                         total_users=total_users,
                         quiz_stats=quiz_stats,
                         recent_scores=recent_scores,
                         level_progress=level_progress,
                         xp_for_next=xp_for_next,
                         achievements=user_achievements[:5],
                         category_stats=category_stats)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    
    # Récupérer les scores de quiz de l'utilisateur
    scores = conn.execute('''
        SELECT category, score, total_questions, completed_at
        FROM quiz_scores 
        WHERE user_id = ? 
        ORDER BY completed_at DESC
        LIMIT 10
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('profile.html', user=user, quiz_scores=scores)

@app.route('/test-matrix')
def test_matrix():
    """Page de test pour diagnostiquer les effets Matrix"""
    return render_template('test_matrix.html')

@app.route('/quiz')
def quiz_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('quiz_home.html', categories=categories)

@app.route('/quiz/<category>')
def quiz_category(category):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if category not in categories:
        flash('Catégorie de quiz non trouvée', 'error')
        return redirect(url_for('quiz_home'))
    
    # Sélectionner 5 questions aléatoires de la catégorie
    question_indices = random.sample(categories[category], min(5, len(categories[category])))
    quiz_questions = [questions[i] for i in question_indices]
    
    # Stocker les indices dans la session pour la correction
    session['current_quiz'] = {
        'category': category,
        'question_indices': question_indices,
        'current_question': 0,
        'score': 0,
        'answers': []
    }
    
    return redirect(url_for('quiz_question'))

@app.route('/quiz/question')
def quiz_question():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'current_quiz' not in session:
        return redirect(url_for('quiz_home'))
    
    quiz_data = session['current_quiz']
    current_idx = quiz_data['current_question']
    
    if current_idx >= len(quiz_data['question_indices']):
        return redirect(url_for('quiz_results'))
    
    question_index = quiz_data['question_indices'][current_idx]
    question = questions[question_index]
    
    # Progression
    progress = {
        'current': current_idx + 1,
        'total': len(quiz_data['question_indices'])
    }
    
    return render_template('quiz_question.html', 
                         question=question, 
                         progress=progress,
                         category=quiz_data['category'])

@app.route('/quiz/answer', methods=['POST'])
def quiz_answer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'current_quiz' not in session:
        return redirect(url_for('quiz_home'))
    
    user_answer = request.form.get('answer', '').strip()
    
    quiz_data = session['current_quiz']
    current_idx = quiz_data['current_question']
    question_index = quiz_data['question_indices'][current_idx]
    
    correct_answer = answers[question_index]
    
    # Stocker la réponse de l'utilisateur
    quiz_data['answers'].append({
        'question': questions[question_index],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': len(user_answer) > 10  # Simple scoring: réponse de plus de 10 caractères
    })
    
    if quiz_data['answers'][-1]['is_correct']:
        quiz_data['score'] += 1
    
    quiz_data['current_question'] += 1
    session['current_quiz'] = quiz_data
    
    if quiz_data['current_question'] >= len(quiz_data['question_indices']):
        return redirect(url_for('quiz_results'))
    
    return redirect(url_for('quiz_question'))

@app.route('/quiz/results')
def quiz_results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'current_quiz' not in session:
        return redirect(url_for('quiz_home'))
    
    quiz_data = session['current_quiz']
    
    # Calculer le pourcentage
    percentage = (quiz_data['score'] / len(quiz_data['question_indices'])) * 100
    
    # Sauvegarder le score en base de données avec le pourcentage
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO quiz_scores (user_id, category, score, total_questions, percentage)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], quiz_data['category'], 
          quiz_data['score'], len(quiz_data['question_indices']), percentage))
    conn.commit()
    conn.close()
    
    # Mettre à jour la progression de l'utilisateur
    progression_data = update_user_progression(
        session['user_id'], 
        quiz_data['score'], 
        len(quiz_data['question_indices']), 
        quiz_data['category'], 
        percentage
    )
    
    # Récupérer les nouveaux achievements
    new_achievements = get_user_achievements(session['user_id'])
    
    results = {
        'category': quiz_data['category'],
        'score': quiz_data['score'],
        'total': len(quiz_data['question_indices']),
        'percentage': round(percentage, 1),
        'answers': quiz_data['answers'],
        'progression': progression_data,
        'achievements': new_achievements[:3]  # Les 3 derniers achievements
    }
    
    # Nettoyer la session
    session.pop('current_quiz', None)
    
    return render_template('quiz_results.html', results=results)

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

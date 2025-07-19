from flask import Flask, jsonify, render_template, request
import sqlite3
import subprocess
import os
import tempfile
import uuid
import time

app = Flask(__name__)

def get_all_questions():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, question FROM questions')
    rows = c.fetchall()
    conn.close()
    return [{'id': row[0], 'question': row[1]} for row in rows]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions', methods=['GET'])
def list_questions():
    return jsonify(get_all_questions())

@app.route('/question/<int:qid>', methods=['GET'])
def get_question(qid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, question FROM questions WHERE id = ?', (qid,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'question': row[1]})
    else:
        return jsonify({'error': 'Question non trouvée'}), 404

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        # Récupérer le code C depuis la requête
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Code C manquant'}), 400
        
        c_code = data['code']
        
        # Créer un nom de fichier unique
        file_id = str(uuid.uuid4())
        c_file = f"/home/jordann/hackaton/temp_code/{file_id}.c"
        executable = f"/home/jordann/hackaton/temp_code/{file_id}"
        
        try:
            # Écrire le code dans un fichier temporaire
            with open(c_file, 'w') as f:
                f.write(c_code)
            
            # Compiler le code
            compile_result = subprocess.run(
                ['gcc', c_file, '-o', executable],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if compile_result.returncode != 0:
                return jsonify({
                    'success': False,
                    'error': 'Erreur de compilation',
                    'details': compile_result.stderr
                })
            
            # Exécuter le programme
            execute_result = subprocess.run(
                [executable],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return jsonify({
                'success': True,
                'output': execute_result.stdout,
                'error_output': execute_result.stderr,
                'return_code': execute_result.returncode
            })
            
        finally:
            # Nettoyer les fichiers temporaires
            try:
                if os.path.exists(c_file):
                    os.remove(c_file)
                if os.path.exists(executable):
                    os.remove(executable)
            except:
                pass
                
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Timeout: Le code a pris trop de temps à s\'exécuter'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur inattendue: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)

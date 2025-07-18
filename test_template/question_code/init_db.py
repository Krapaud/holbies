import sqlite3
from questions import questions

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Créer la table
c.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
)
''')

# Vider les anciennes entrées (si tu veux repartir à zéro)
c.execute('DELETE FROM questions')

# Insérer les questions
for q in questions:
    c.execute("INSERT INTO questions (question) VALUES (?)", (q,))

conn.commit()
conn.close()

print("Base de données initialisée avec succès.")

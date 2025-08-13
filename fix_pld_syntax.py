#!/usr/bin/env python3
"""
Script pour corriger la ligne cassée dans pld.js
"""

def fix_pld_js():
    file_path = '/home/krapaud/project-holbies/src/static/js/pld.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    
    # Trouver et corriger la ligne problématique
    for i, line in enumerate(lines):
        if 'this.cu' in line and 'rrentSession.id' in lines[i+1] if i+1 < len(lines) else False:
            print(f"Ligne {i+1} problématique trouvée:")
            print(f"  Avant: {repr(line.strip())}")
            print(f"  Suivante: {repr(lines[i+1].strip())}")
            
            # Corriger en joignant les deux lignes
            fixed_line = '                await window.holbiesApp.apiRequest(`/api/pld/complete?session_id=${this.currentSession.id}`, {\n'
            lines[i] = fixed_line
            lines[i+1] = '                    method: \'POST\'\n'
            
            print(f"  Corrigé: {repr(fixed_line.strip())}")
            break
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fichier corrigé!")

if __name__ == "__main__":
    fix_pld_js()

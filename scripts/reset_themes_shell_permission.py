#!/usr/bin/env python3
"""
Script pour réinitialiser les thèmes PLD et ajouter le nouveau thème "Shell Permission"
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.database import SessionLocal
from app.models import PLDCategory, PLDTheme, PLDQuestion
import json

def reset_and_create_shell_permission_theme():
    """Supprimer tous les thèmes existants et créer le nouveau thème Shell Permission"""
    print("🔄 Réinitialisation des thèmes PLD...")
    
    db = SessionLocal()
    
    try:
        # 1. Supprimer toutes les questions existantes
        print("🗑️ Suppression de toutes les questions existantes...")
        questions_deleted = db.query(PLDQuestion).delete()
        print(f"   ✅ {questions_deleted} questions supprimées")
        
        # 2. Supprimer tous les thèmes existants
        print("🗑️ Suppression de tous les thèmes existants...")
        themes_deleted = db.query(PLDTheme).delete()
        print(f"   ✅ {themes_deleted} thèmes supprimés")
        
        # 3. Vérifier qu'on a au moins une catégorie "shell" ou la créer
        shell_category = db.query(PLDCategory).filter(PLDCategory.name == "shell").first()
        if not shell_category:
            print("📚 Création de la catégorie Shell...")
            shell_category = PLDCategory(
                name="shell",
                display_name="Shell",
                description="Scripts Bash, commandes Unix et système",
                icon="SH"
            )
            db.add(shell_category)
            db.flush()
            print("   ✅ Catégorie Shell créée")
        else:
            print(f"   ✅ Catégorie Shell existante trouvée (ID: {shell_category.id})")
        
        # 4. Créer le nouveau thème "Shell Permission"
        print("🎯 Création du thème 'Shell Permission'...")
        permission_theme = PLDTheme(
            name="permissions",
            display_name="Shell Permission",
            description="Gestion des permissions et commandes système",
            icon="🔐",
            category_id=shell_category.id
        )
        db.add(permission_theme)
        db.flush()
        print(f"   ✅ Thème 'Shell Permission' créé (ID: {permission_theme.id})")
        
        # 5. Créer toutes les questions pour le thème Shell Permission
        print("❓ Création des questions Shell Permission...")
        
        questions_data = [
            {
                "question": "What is an alias ?",
                "answer": "An alias in shell is a short name or abbreviation for a longer command. It allows you to create custom shortcuts for frequently used commands. You create an alias using the 'alias' command, for example: alias ll='ls -la'. This creates a shortcut 'll' that executes 'ls -la'.",
                "technical_terms": ["alias", "command", "shortcut", "shell", "abbreviation"],
                "explanation": "Aliases are useful for creating shortcuts to long or complex commands, improving productivity and reducing typing errors.",
                "difficulty": "easy"
            },
            {
                "question": "What is LTS ?",
                "answer": "LTS stands for Long Term Support. It refers to software versions that receive extended support and maintenance for a longer period than regular releases. LTS versions are typically more stable and are recommended for production environments. Examples include Ubuntu LTS releases (supported for 5 years) and Node.js LTS versions.",
                "technical_terms": ["LTS", "Long Term Support", "stable", "production", "maintenance"],
                "explanation": "LTS versions prioritize stability and security over having the latest features, making them ideal for servers and production systems.",
                "difficulty": "easy"
            },
            {
                "question": "What does the command wc -l filename do ?",
                "answer": "The command 'wc -l filename' counts and displays the number of lines in the specified file. 'wc' stands for word count, and the '-l' option specifically tells it to count lines only. For example, 'wc -l myfile.txt' will output the number of lines in myfile.txt.",
                "technical_terms": ["wc", "-l", "lines", "count", "filename"],
                "explanation": "The wc command is useful for getting quick statistics about files, with -l being one of the most commonly used options.",
                "difficulty": "easy"
            },
            {
                "question": "What is a symbolic link (soft link) ?",
                "answer": "A symbolic link (soft link) is a file that points to another file or directory by storing its path. It's like a shortcut or reference to the original file. If the original file is deleted, the symbolic link becomes broken. You create symbolic links using 'ln -s target linkname'. Symbolic links can point to files on different filesystems.",
                "technical_terms": ["symbolic link", "soft link", "ln -s", "pointer", "reference", "shortcut"],
                "explanation": "Symbolic links are flexible references that can point across filesystems but become invalid if the target is moved or deleted.",
                "difficulty": "medium"
            },
            {
                "question": "What is a hard link ?",
                "answer": "A hard link is a direct reference to the data of a file on the filesystem. Unlike symbolic links, hard links point directly to the inode (the actual data) rather than the filename. Multiple hard links can exist for the same file, and the file only gets deleted when all hard links are removed. Hard links cannot span across different filesystems and cannot link to directories.",
                "technical_terms": ["hard link", "inode", "filesystem", "ln", "direct reference"],
                "explanation": "Hard links create multiple names for the same file data, providing redundancy and ensuring data persistence.",
                "difficulty": "medium"
            },
            {
                "question": "What does su do?",
                "answer": "The 'su' command (substitute user or switch user) allows you to change your user identity to another user account. By default, 'su' switches to the root user account. You can specify a different user with 'su username'. It requires the target user's password. 'su -' provides a complete login environment for the target user.",
                "technical_terms": ["su", "substitute user", "switch user", "root", "password"],
                "explanation": "su is essential for administrative tasks that require different user privileges, especially gaining root access.",
                "difficulty": "easy"
            },
            {
                "question": "What happen when we type chmod ugo+x file_name ?",
                "answer": "The command 'chmod ugo+x file_name' adds execute permission (+x) to the file for all users: user/owner (u), group (g), and others (o). This makes the file executable by everyone. The '+' means add permission, 'x' means execute permission, and 'ugo' specifies that it applies to user, group, and others.",
                "technical_terms": ["chmod", "ugo", "+x", "execute", "permission", "user", "group", "others"],
                "explanation": "This command grants execute permissions to all categories of users, making the file runnable by anyone.",
                "difficulty": "medium"
            },
            {
                "question": "What is the value of rw-r--r--?",
                "answer": "The permission string 'rw-r--r--' represents: owner has read and write permissions (rw-), group has read-only permission (r--), and others have read-only permission (r--). In octal notation, this equals 644: owner (6=4+2=read+write), group (4=read), others (4=read).",
                "technical_terms": ["rw-r--r--", "644", "octal", "read", "write", "owner", "group", "others"],
                "explanation": "This is a common permission pattern for files that the owner can modify but others can only read.",
                "difficulty": "medium"
            },
            {
                "question": "What is chgrp?",
                "answer": "chgrp (change group) is a command used to change the group ownership of files and directories. The syntax is 'chgrp groupname filename'. Only the file owner or root can change the group ownership. For example, 'chgrp developers myfile.txt' changes the group ownership of myfile.txt to the 'developers' group.",
                "technical_terms": ["chgrp", "change group", "group ownership", "groupname", "ownership"],
                "explanation": "chgrp is useful for collaborative environments where different groups need access to specific files.",
                "difficulty": "easy"
            },
            {
                "question": "How to set the mode of the file hello the same as olleh's mode ?",
                "answer": "To set the mode of file 'hello' the same as file 'olleh', you can use: 'chmod --reference=olleh hello'. This copies the permission mode from 'olleh' to 'hello'. Alternatively, you can first check olleh's permissions with 'ls -l olleh' and then apply the same permissions to hello using 'chmod' with the appropriate mode.",
                "technical_terms": ["chmod", "--reference", "mode", "permissions", "copy permissions"],
                "explanation": "The --reference option is a convenient way to copy permissions from one file to another without manually calculating the mode.",
                "difficulty": "medium"
            },
            {
                "question": "What is the difference between chmod chown chgrp ?",
                "answer": "chmod changes file permissions (read, write, execute), chown changes file ownership (user owner), and chgrp changes group ownership. chmod modifies what actions can be performed on the file, chown changes who owns the file, and chgrp changes which group owns the file. For example: 'chmod 755 file' (permissions), 'chown user file' (owner), 'chgrp group file' (group).",
                "technical_terms": ["chmod", "chown", "chgrp", "permissions", "ownership", "user owner", "group ownership"],
                "explanation": "These three commands control different aspects of file access: what can be done (chmod), who owns it (chown), and which group owns it (chgrp).",
                "difficulty": "hard"
            },
            {
                "question": "What is the permission value for a file without any restriction?",
                "answer": "A file without any restrictions would have permission value 777 in octal notation or rwxrwxrwx in symbolic notation. This means all users (owner, group, others) have full permissions: read (r), write (w), and execute (x). However, this is generally not recommended for security reasons, especially for sensitive files.",
                "technical_terms": ["777", "rwxrwxrwx", "full permissions", "read", "write", "execute", "security"],
                "explanation": "777 permissions mean everyone can read, modify, and execute the file, which poses security risks in most scenarios.",
                "difficulty": "medium"
            },
            {
                "question": "What is the numerical value for the rw--wxr-x permission?",
                "answer": "The permission rw--wxr-x converts to 635 in octal notation. Breaking it down: owner has rw- (4+2+0=6), group has -wx (0+2+1=3), others have r-x (4+0+1=5). So the numerical value is 635.",
                "technical_terms": ["635", "rw--wxr-x", "octal", "read", "write", "execute", "numerical value"],
                "explanation": "Each permission group (owner, group, others) is calculated by adding read(4), write(2), and execute(1) values.",
                "difficulty": "hard"
            }
        ]
        
        # Créer les questions
        for i, q_data in enumerate(questions_data, 1):
            question = PLDQuestion(
                question_text=q_data["question"],
                expected_answer=q_data["answer"],
                technical_terms=json.dumps(q_data["technical_terms"]),
                explanation=q_data["explanation"],
                difficulty=q_data["difficulty"],
                max_score=100,
                theme_id=permission_theme.id
            )
            db.add(question)
            print(f"   ✅ Question {i:2d}/13: {q_data['question'][:50]}...")
        
        # 6. Commit toutes les modifications
        db.commit()
        print("\n🎉 Réinitialisation terminée avec succès !")
        
        # 7. Afficher les statistiques finales
        total_categories = db.query(PLDCategory).count()
        total_themes = db.query(PLDTheme).count()
        total_questions = db.query(PLDQuestion).count()
        
        print(f"\n📊 Statistiques finales:")
        print(f"   📚 Catégories PLD: {total_categories}")
        print(f"   🎯 Thèmes PLD: {total_themes}")
        print(f"   ❓ Questions PLD: {total_questions}")
        
        # Détails du nouveau thème
        shell_questions = db.query(PLDQuestion).join(PLDTheme).filter(
            PLDTheme.category_id == shell_category.id
        ).count()
        print(f"\n🔐 Thème 'Shell Permission':")
        print(f"   ❓ Questions: {shell_questions}")
        print(f"   📝 Niveaux: facile, moyen, difficile")
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Lancement de la réinitialisation des thèmes PLD...")
    print("⚠️  ATTENTION: Cette opération va supprimer TOUS les thèmes et questions existants !")
    
    confirm = input("Voulez-vous continuer ? (oui/non): ").lower().strip()
    if confirm in ['oui', 'o', 'yes', 'y']:
        reset_and_create_shell_permission_theme()
        print("\n✅ Opération terminée avec succès !")
    else:
        print("❌ Opération annulée.")

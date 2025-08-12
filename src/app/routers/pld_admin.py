"""
Endpoints d'administration pour la gestion des questions PLD
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models import PLDCategory, PLDTheme, PLDQuestion, User
from app.schemas import (
    PLDCategoryCreate, PLDCategory as PLDCategorySchema, PLDCategoryWithThemes,
    PLDThemeCreate, PLDTheme as PLDThemeSchema, PLDThemeWithQuestions,
    PLDQuestionCreate, PLDQuestion as PLDQuestionSchema
)
from app.auth import get_current_active_user

router = APIRouter(prefix="/admin", tags=["pld-admin"])

def admin_required(current_user: User = Depends(get_current_active_user)):
    """Vérifier que l'utilisateur est admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    return current_user

# ================================
# GESTION DES CATÉGORIES
# ================================

@router.get("/categories", response_model=List[PLDCategoryWithThemes])
async def get_all_categories(
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Récupérer toutes les catégories avec leurs thèmes"""
    categories = db.query(PLDCategory).all()
    return categories

@router.post("/categories", response_model=PLDCategorySchema)
async def create_category(
    category: PLDCategoryCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Créer une nouvelle catégorie"""
    # Vérifier que la catégorie n'existe pas déjà
    existing = db.query(PLDCategory).filter(PLDCategory.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La catégorie '{category.name}' existe déjà"
        )
    
    db_category = PLDCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/categories/{category_id}", response_model=PLDCategorySchema)
async def update_category(
    category_id: int,
    category: PLDCategoryCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Mettre à jour une catégorie"""
    db_category = db.query(PLDCategory).filter(PLDCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie non trouvée"
        )
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Supprimer une catégorie et tous ses thèmes/questions"""
    db_category = db.query(PLDCategory).filter(PLDCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie non trouvée"
        )
    
    db.delete(db_category)
    db.commit()
    return {"message": "Catégorie supprimée avec succès"}

# ================================
# GESTION DES THÈMES
# ================================

@router.get("/themes", response_model=List[PLDThemeWithQuestions])
async def get_all_themes(
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Récupérer tous les thèmes avec leurs questions"""
    themes = db.query(PLDTheme).all()
    return themes

@router.post("/themes", response_model=PLDThemeSchema)
async def create_theme(
    theme: PLDThemeCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Créer un nouveau thème"""
    # Vérifier que la catégorie existe
    category = db.query(PLDCategory).filter(PLDCategory.id == theme.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catégorie non trouvée"
        )
    
    db_theme = PLDTheme(**theme.dict())
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

@router.put("/themes/{theme_id}", response_model=PLDThemeSchema)
async def update_theme(
    theme_id: int,
    theme: PLDThemeCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Mettre à jour un thème"""
    db_theme = db.query(PLDTheme).filter(PLDTheme.id == theme_id).first()
    if not db_theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thème non trouvé"
        )
    
    for key, value in theme.dict().items():
        setattr(db_theme, key, value)
    
    db.commit()
    db.refresh(db_theme)
    return db_theme

@router.delete("/themes/{theme_id}")
async def delete_theme(
    theme_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Supprimer un thème et toutes ses questions"""
    db_theme = db.query(PLDTheme).filter(PLDTheme.id == theme_id).first()
    if not db_theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thème non trouvé"
        )
    
    db.delete(db_theme)
    db.commit()
    return {"message": "Thème supprimé avec succès"}

# ================================
# GESTION DES QUESTIONS
# ================================

@router.get("/questions", response_model=List[PLDQuestionSchema])
async def get_all_questions(
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Récupérer toutes les questions"""
    questions = db.query(PLDQuestion).all()
    return questions

@router.post("/questions", response_model=PLDQuestionSchema)
async def create_question(
    question: PLDQuestionCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Créer une nouvelle question"""
    # Vérifier que le thème existe
    theme = db.query(PLDTheme).filter(PLDTheme.id == question.theme_id).first()
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thème non trouvé"
        )
    
    # Convertir la liste des termes techniques en JSON
    question_data = question.dict()
    question_data["technical_terms"] = json.dumps(question.technical_terms)
    
    db_question = PLDQuestion(**question_data)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.put("/questions/{question_id}", response_model=PLDQuestionSchema)
async def update_question(
    question_id: int,
    question: PLDQuestionCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Mettre à jour une question"""
    db_question = db.query(PLDQuestion).filter(PLDQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question non trouvée"
        )
    
    # Mettre à jour les champs
    question_data = question.dict()
    question_data["technical_terms"] = json.dumps(question.technical_terms)
    
    for key, value in question_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Supprimer une question"""
    db_question = db.query(PLDQuestion).filter(PLDQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question non trouvée"
        )
    
    db.delete(db_question)
    db.commit()
    return {"message": "Question supprimée avec succès"}

# ================================
# ENDPOINTS SPÉCIAUX
# ================================

@router.post("/import-questions")
async def import_questions_from_json(
    data: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Importer des questions depuis un format JSON"""
    try:
        imported_count = 0
        
        for category_name, themes_data in data.items():
            # Créer ou récupérer la catégorie
            category = db.query(PLDCategory).filter(PLDCategory.name == category_name).first()
            if not category:
                category = PLDCategory(
                    name=category_name,
                    display_name=category_name.title(),
                    description=f"Questions de programmation {category_name}",
                    icon="📚"
                )
                db.add(category)
                db.flush()
            
            for theme_name, questions_data in themes_data.items():
                # Créer ou récupérer le thème
                theme = db.query(PLDTheme).filter(
                    PLDTheme.name == theme_name,
                    PLDTheme.category_id == category.id
                ).first()
                
                if not theme:
                    theme = PLDTheme(
                        name=theme_name,
                        display_name=theme_name.title().replace("_", " "),
                        description=f"Questions sur {theme_name}",
                        icon="📝",
                        category_id=category.id
                    )
                    db.add(theme)
                    db.flush()
                
                # Ajouter les questions
                for question_data in questions_data.values():
                    question = PLDQuestion(
                        question_text=question_data["question_text"],
                        expected_answer=question_data["expected_answer"],
                        technical_terms=json.dumps(question_data["technical_terms"]),
                        explanation=question_data["explanation"],
                        difficulty=question_data["difficulty"],
                        max_score=question_data["max_score"],
                        theme_id=theme.id
                    )
                    db.add(question)
                    imported_count += 1
        
        db.commit()
        return {"message": f"{imported_count} questions importées avec succès"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de l'import: {str(e)}"
        )

@router.get("/export-questions")
async def export_questions(
    db: Session = Depends(get_db),
    admin_user: User = Depends(admin_required)
):
    """Exporter toutes les questions au format JSON"""
    categories = db.query(PLDCategory).all()
    export_data = {}
    
    for category in categories:
        export_data[category.name] = {}
        for theme in category.themes:
            export_data[category.name][theme.name] = {}
            for i, question in enumerate(theme.questions, 1):
                export_data[category.name][theme.name][i] = {
                    "question_id": question.id,
                    "question_text": question.question_text,
                    "expected_answer": question.expected_answer,
                    "technical_terms": json.loads(question.technical_terms),
                    "explanation": question.explanation,
                    "difficulty": question.difficulty,
                    "max_score": question.max_score,
                    "category": category.name,
                    "theme": theme.name
                }
    
    return export_data

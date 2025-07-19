from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Any
import subprocess
import tempfile
import os
import sys
import traceback
import json
from app.auth import get_current_user
from app.models import User

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str

class CodeExecutionResponse(BaseModel):
    output: Optional[str] = None
    error: Optional[str] = None
    trace: Optional[List[Any]] = None

class CodeExecutor:
    @staticmethod
    def execute_python(code: str) -> CodeExecutionResponse:
        """Exécute du code Python de manière sécurisée"""
        try:
            # Créer un environnement sécurisé
            import io
            from contextlib import redirect_stdout, redirect_stderr
            
            # Capturer la sortie
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Variables globales limitées pour la sécurité
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'int': int,
                    'float': float,
                    'str': str,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'round': round,
                    'sorted': sorted,
                    'reversed': reversed,
                    'enumerate': enumerate,
                    'zip': zip,
                }
            }
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals)
            
            output = stdout_capture.getvalue()
            error = stderr_capture.getvalue()
            
            return CodeExecutionResponse(
                output=output if output else None,
                error=error if error else None
            )
            
        except Exception as e:
            return CodeExecutionResponse(
                error=f"Erreur d'exécution: {str(e)}"
            )

    @staticmethod
    def execute_javascript(code: str) -> CodeExecutionResponse:
        """Exécute du code JavaScript avec Node.js"""
        try:
            # Wrapper pour capturer console.log
            js_wrapper = f"""
const originalLog = console.log;
const outputs = [];
console.log = (...args) => {{
    outputs.push(args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
    ).join(' '));
}};

try {{
    {code}
    console.log = originalLog;
    console.log(outputs.join('\\n'));
}} catch (error) {{
    console.log = originalLog;
    console.error('Erreur:', error.message);
}}
"""
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(js_wrapper)
                temp_file = f.name
            
            try:
                # Exécuter avec Node.js
                result = subprocess.run(
                    ['node', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return CodeExecutionResponse(output=result.stdout.strip())
                else:
                    return CodeExecutionResponse(error=result.stderr.strip())
                    
            finally:
                # Nettoyer le fichier temporaire
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            return CodeExecutionResponse(error="Timeout: L'exécution a pris trop de temps")
        except FileNotFoundError:
            return CodeExecutionResponse(error="Node.js n'est pas installé sur le serveur")
        except Exception as e:
            return CodeExecutionResponse(error=f"Erreur d'exécution JavaScript: {str(e)}")

    @staticmethod
    def execute_c(code: str) -> CodeExecutionResponse:
        """Compile et exécute du code C avec GCC"""
        try:
            # Créer les fichiers temporaires
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as source_file:
                source_file.write(code)
                source_path = source_file.name
            
            # Nom du fichier exécutable
            executable_path = source_path.replace('.c', '')
            
            try:
                # Compilation
                compile_result = subprocess.run(
                    ['gcc', '-o', executable_path, source_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_result.returncode != 0:
                    return CodeExecutionResponse(error=f"Erreur de compilation:\\n{compile_result.stderr}")
                
                # Exécution
                run_result = subprocess.run(
                    [executable_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if run_result.returncode == 0:
                    return CodeExecutionResponse(output=run_result.stdout.strip())
                else:
                    return CodeExecutionResponse(error=f"Erreur d'exécution:\\n{run_result.stderr}")
                    
            finally:
                # Nettoyer les fichiers temporaires
                if os.path.exists(source_path):
                    os.unlink(source_path)
                if os.path.exists(executable_path):
                    os.unlink(executable_path)
                    
        except subprocess.TimeoutExpired:
            return CodeExecutionResponse(error="Timeout: L'exécution a pris trop de temps")
        except FileNotFoundError:
            return CodeExecutionResponse(error="GCC n'est pas installé sur le serveur")
        except Exception as e:
            return CodeExecutionResponse(error=f"Erreur d'exécution C: {str(e)}")

@router.post("/test", response_model=CodeExecutionResponse)
async def test_execute():
    """Test simple sans authentification"""
    return CodeExecutionResponse(output="✅ Tous les langages sont maintenant supportés: Python, JavaScript (Node.js), C (GCC)")

@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest,
    current_user: User = Depends(get_current_user)
):
    """Exécute du code dans le langage spécifié"""
    
    print(f"DEBUG: User authenticated: {current_user.username}")
    print(f"DEBUG: Code length: {len(request.code)}")
    print(f"DEBUG: Language: {request.language}")
    
    # Validation du langage
    supported_languages = ['python', 'javascript', 'c']
    if request.language not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Langage non supporté. Langages supportés: {', '.join(supported_languages)}"
        )
    
    # Validation de la longueur du code
    if len(request.code) > 10000:  # Limite de 10KB
        raise HTTPException(
            status_code=400,
            detail="Le code est trop long (maximum 10KB)"
        )
    
    # Vérifications de sécurité basiques
    dangerous_keywords = [
        'import os', 'import sys', 'import subprocess', 'import shutil',
        'open(', 'file(', 'exec(', 'eval(', '__import__',
        'system(', 'popen(', 'fork(', 'spawn(',
        'delete', 'remove', 'unlink', 'rmdir'
    ]
    
    for keyword in dangerous_keywords:
        if keyword in request.code.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Code potentiellement dangereux détecté: {keyword}"
            )
    
    # Exécuter le code selon le langage
    executor = CodeExecutor()
    
    if request.language == 'python':
        result = executor.execute_python(request.code)
    elif request.language == 'javascript':
        result = executor.execute_javascript(request.code)
    elif request.language == 'c':
        result = executor.execute_c(request.code)
    
    return result

@router.get("/languages")
async def get_supported_languages():
    """Retourne la liste des langages supportés"""
    return {
        "languages": [
            {
                "code": "python",
                "name": "Python",
                "icon": "🐍",
                "description": "Langage de programmation polyvalent et facile à apprendre"
            },
            {
                "code": "javascript",
                "name": "JavaScript",
                "icon": "📜",
                "description": "Langage de programmation pour le web et Node.js"
            },
            {
                "code": "c",
                "name": "C",
                "icon": "⚙️",
                "description": "Langage de programmation système performant"
            }
        ]
    }

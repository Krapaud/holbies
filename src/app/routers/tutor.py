from fastapi import APIRouter, HTTPException, Depends, Request
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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
# Fichier supprimé : routeur FastAPI pour /tutor
router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str

class CodeExecutionResponse(BaseModel):
    output: Optional[str] = None
    error: Optional[str] = None
    trace: Optional[List[Any]] = None

class CodeExecutor:
    @staticmethod
    def execute_python(code: str) -> CodeExecutionResponse:
        """Exécute du code Python de manière sécurisée et trace chaque étape (façon Python Tutor, avec heap et références)"""
        import io
        import sys
        import linecache
        from contextlib import redirect_stdout, redirect_stderr
        import builtins
        trace_steps = []
        output_progress = []
        
        def get_obj_id(obj):
            try:
                return f"id{str(id(obj))}"
            except Exception:
                return None
        
        def extract_heap(vars_dict, _seen_ids=None):
            if _seen_ids is None:
                _seen_ids = set()
            heap = {}
            refs = {}

            def _extract_obj(obj):
                obj_id = get_obj_id(obj)
                if obj_id is None or obj_id in _seen_ids:
                    return obj_id

                _seen_ids.add(obj_id)
                obj_type = type(obj).__name__
                value = None
                obj_refs = []

                if isinstance(obj, (int, float, bool, type(None), str)):
                    value = obj
                elif isinstance(obj, (list, tuple, set)):
                    value = []
                    for item in obj:
                        item_id = _extract_obj(item)
                        if item_id:
                            value.append({'ref': item_id})
                            obj_refs.append(item_id)
                        else:
                            value.append(item)
                elif isinstance(obj, dict):
                    value = {}
                    for k, v in obj.items():
                        v_id = _extract_obj(v)
                        if v_id:
                            value[k] = {'ref': v_id}
                            obj_refs.append(v_id)
                        else:
                            value[k] = v
                else:
                    # Custom objects
                    try:
                        if hasattr(obj, '__dict__'):
                            value = {}
                            for k, v in obj.__dict__.items():
                                v_id = _extract_obj(v)
                                if v_id:
                                    value[k] = {'ref': v_id}
                                    obj_refs.append(v_id)
                                else:
                                    value[k] = v
                        else:
                            value = repr(obj) # Fallback for objects without __dict__
                    except Exception:
                        value = repr(obj) # Fallback for objects that fail repr

                heap[obj_id] = {'type': obj_type, 'value': value, 'refs': obj_refs}
                return obj_id

            for name, var in vars_dict.items():
                var_id = _extract_obj(var)
                if var_id:
                    refs[name] = var_id
                else:
                    # For simple types that don't go into heap, store directly
                    refs[name] = var

            return heap, refs
        
        def tracer(frame, event, arg):
            if event == 'line':
                lineno = frame.f_lineno
                filename = frame.f_code.co_filename
                line = linecache.getline(filename, lineno).rstrip()
                local_vars = dict(frame.f_locals)
                global_vars = dict(frame.f_globals)
                stack = []
                f = frame
                while f:
                    stack.append({
                        'function': f.f_code.co_name,
                        'lineno': f.f_lineno,
                        'locals': dict(f.f_locals)
                    })
                    f = f.f_back
                stack.reverse()
                # Heap extraction
                heap, refs = extract_heap(local_vars)
                gheap, grefs = extract_heap(global_vars)
                trace_steps.append({
                    'event': event,
                    'lineno': lineno,
                    'line': line,
                    'locals': local_vars,
                    'globals': global_vars,
                    'stack': stack,
                    'output': ''.join(output_progress),
                    'heap': {**heap, **gheap},
                    'refs': {**refs, **grefs}
                })
            return tracer
        
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
        
        # Redéfinir print pour capturer la sortie à chaque étape
        def traced_print(*args, **kwargs):
            s = ' '.join(str(a) for a in args)
            output_progress.append(s + '\n')
            return s
        safe_globals['__builtins__']['print'] = traced_print
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        try:
            sys.settrace(tracer)
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals)
            sys.settrace(None)
        except Exception as e:
            sys.settrace(None)
            return CodeExecutionResponse(
                error=f"Erreur d'exécution: {str(e)}",
                trace=trace_steps
            )
        output = stdout_capture.getvalue()
        error = stderr_capture.getvalue()
        return CodeExecutionResponse(
            output=output if output else None,
            error=error if error else None,
            trace=trace_steps
        )

    

@router.get("/visualizer", response_class=HTMLResponse)
async def get_code_visualizer(request: Request):
    return templates.TemplateResponse("code_visualizer.html", {"request": request})

@router.post("/run-python-code", response_model=CodeExecutionResponse)
async def run_python_code(
    request: CodeExecutionRequest,
    current_user: User = Depends(get_current_user)
):
    print(f"DEBUG: User authenticated: {current_user.username}")
    print(f"DEBUG: Code length: {len(request.code)}")

    if len(request.code) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Le code est trop long (maximum 10KB)"
        )

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
    
    result = CodeExecutor.execute_python(request.code)
    return result

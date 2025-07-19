#!/usr/bin/env python3
"""
DLH Tutor Engine - Version intégrée dans Flask
Moteur d'exécution simplifié pour Python, JavaScript et C
"""

import sys
import subprocess
import tempfile
import os
import json
import traceback

class TutorEngine:
    def __init__(self):
        pass
    
    def execute_python(self, code):
        """Exécute du code Python de manière sécurisée"""
        try:
            # Capture de la sortie
            output = []
            
            # Environnement sécurisé
            def safe_print(*args):
                output.append(" ".join(str(arg) for arg in args))
            
            safe_globals = {
                '__builtins__': {
                    'print': safe_print,
                    'range': range,
                    'len': len,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'bool': bool,
                    'enumerate': enumerate,
                    'zip': zip,
                }
            }
            
            # Variables locales
            local_vars = {}
            
            # Tracer l'exécution
            trace = []
            lines = code.strip().split('\n')
            
            for i, line in enumerate(lines, 1):
                if line.strip():
                    try:
                        # Exécuter la ligne
                        exec(line, safe_globals, local_vars)
                        
                        # Capturer l'état
                        snapshot = {
                            "line": i,
                            "code": line,
                            "locals": dict(local_vars),
                            "output": "\n".join(output) if output else ""
                        }
                        trace.append(snapshot)
                        
                    except Exception as e:
                        # Erreur sur cette ligne
                        snapshot = {
                            "line": i,
                            "code": line,
                            "locals": dict(local_vars),
                            "output": f"Erreur: {str(e)}",
                            "error": str(e)
                        }
                        trace.append(snapshot)
                        break
            
            return {
                "success": True,
                "trace": trace,
                "final_output": "\n".join(output) if output else ""
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'exécution: {str(e)}",
                "trace": []
            }
    
    def execute_javascript(self, code):
        """Exécute du code JavaScript avec Node.js"""
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Exécuter avec Node.js
            result = subprocess.run(
                ['node', temp_file], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            # Nettoyer
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "trace": [{"line": 1, "output": result.stdout}]
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "trace": []
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout: Le code a pris trop de temps à s'exécuter",
                "trace": []
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Node.js n'est pas installé",
                "trace": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur: {str(e)}",
                "trace": []
            }
    
    def execute_c(self, code):
        """Exécute du code C avec GCC"""
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_c_file = f.name
            
            # Compiler
            temp_exe_file = temp_c_file.replace('.c', '.exe')
            compile_result = subprocess.run(
                ['gcc', temp_c_file, '-o', temp_exe_file], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if compile_result.returncode != 0:
                os.unlink(temp_c_file)
                return {
                    "success": False,
                    "error": f"Erreur de compilation: {compile_result.stderr}",
                    "trace": []
                }
            
            # Exécuter
            run_result = subprocess.run(
                [temp_exe_file], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            # Nettoyer
            os.unlink(temp_c_file)
            os.unlink(temp_exe_file)
            
            if run_result.returncode == 0:
                return {
                    "success": True,
                    "output": run_result.stdout,
                    "trace": [{"line": 1, "output": run_result.stdout}]
                }
            else:
                return {
                    "success": False,
                    "error": run_result.stderr,
                    "trace": []
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout: Le code a pris trop de temps",
                "trace": []
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "GCC n'est pas installé",
                "trace": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur: {str(e)}",
                "trace": []
            }
    
    def execute_code(self, code, language):
        """Point d'entrée principal pour exécuter du code"""
        if language == "python":
            return self.execute_python(code)
        elif language == "javascript":
            return self.execute_javascript(code)
        elif language == "c":
            return self.execute_c(code)
        else:
            return {
                "success": False,
                "error": f"Langage '{language}' non supporté",
                "trace": []
            }

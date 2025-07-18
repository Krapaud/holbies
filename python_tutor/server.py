#!/usr/bin/env python3
"""
D.L.H. Tutor API Server
Serveur simple pour exécuter du code Python et retourner les résultats
"""

import sys
import traceback
import subprocess
import tempfile
import os
import json
import http.server
import socketserver
from urllib.parse import parse_qs

class PythonTracer:
    def __init__(self):
        self.trace = []
        self.output = ""

    def _safe_print(self, *args, **kwargs):
        """Print sécurisé qui capture la sortie"""
        self.output += " ".join(str(a) for a in args) + "\n"

    def tracer(self, frame, event, arg):
        """Fonction de traçage pour capturer l'exécution"""
        if event == 'line':
            lineno = frame.f_lineno
            # Nettoyer les variables locales pour éviter les objets non sérialisables
            clean_locals = {}
            for key, value in frame.f_locals.items():
                try:
                    # Tester si la valeur est sérialisable en JSON
                    json.dumps(value)
                    clean_locals[key] = value
                except (TypeError, ValueError):
                    # Si non sérialisable, convertir en string
                    clean_locals[key] = str(type(value).__name__)
            
            snapshot = {
                "line": lineno,
                "locals": clean_locals,
                "globals": {},
                "output": self.output
            }
            self.trace.append(snapshot)
        return self.tracer

    def run_code(self, code):
        """Exécute le code Python avec traçage"""
        self.trace = []
        self.output = ""

        # Environnement sécurisé
        safe_globals = {
            '__builtins__': {
                'print': self._safe_print,
                'range': range,
                'len': len,
                'int': int,
                'float': float,
                'str': str,
                'bool': bool,
                'list': list,
                'dict': dict,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
            }
        }

        try:
            sys.settrace(self.tracer)
            exec(code, safe_globals)
        except Exception as e:
            tb = traceback.format_exc()
            self.trace.append({
                "line": -1,
                "locals": {},
                "globals": {},
                "output": self.output,
                "error": tb
            })
        finally:
            sys.settrace(None)

        return self.trace


class JavaScriptExecutor:
    def run_code(self, code):
        """Exécute du code JavaScript avec Node.js"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                # Code wrapper pour capturer les variables et la sortie
                wrapped_code = f"""
let output = '';
const originalLog = console.log;
console.log = function(...args) {{
    output += args.join(' ') + '\\n';
    originalLog(...args);
}};

try {{
{code}

    console.log('OUTPUT:', output);
}} catch (error) {{
    console.log('ERROR:', error.toString());
}}
"""
                f.write(wrapped_code)
                f.flush()
                
                result = subprocess.run(['node', f.name], 
                                      capture_output=True, text=True, timeout=10)
                
                if result.returncode != 0:
                    return [{
                        "line": -1,
                        "locals": {},
                        "globals": {},
                        "output": "",
                        "error": result.stderr
                    }]
                
                # Parser la sortie
                output_lines = result.stdout.strip().split('\n')
                output_content = ""
                error_content = None
                
                for line in output_lines:
                    if line.startswith('OUTPUT:'):
                        output_content = line[7:].strip()
                    elif line.startswith('ERROR:'):
                        error_content = line[6:].strip()
                    else:
                        output_content += line + "\n"
                
                return [{
                    "line": -1,
                    "locals": {},
                    "globals": {},
                    "output": output_content,
                    "error": error_content
                }]
                
        except Exception as e:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": str(e)
            }]
        finally:
            try:
                os.unlink(f.name)
            except:
                pass


class CExecutor:
    def run_code(self, code):
        """Compile et exécute du code C avec GCC"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                # Code wrapper C avec includes de base
                wrapped_code = f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {{
{code}
    return 0;
}}
"""
                f.write(wrapped_code)
                f.flush()
                
                # Compilation
                exe_name = f.name.replace('.c', '')
                compile_result = subprocess.run(['gcc', f.name, '-o', exe_name], 
                                              capture_output=True, text=True, timeout=10)
                
                if compile_result.returncode != 0:
                    return [{
                        "line": -1,
                        "locals": {},
                        "globals": {},
                        "output": "",
                        "error": "Erreur de compilation:\n" + compile_result.stderr
                    }]
                
                # Exécution
                run_result = subprocess.run([exe_name], 
                                          capture_output=True, text=True, timeout=10)
                
                return [{
                    "line": -1,
                    "locals": {},
                    "globals": {},
                    "output": run_result.stdout,
                    "error": run_result.stderr if run_result.returncode != 0 else None
                }]
                
        except Exception as e:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": str(e)
            }]
        finally:
            try:
                os.unlink(f.name)
                if 'exe_name' in locals():
                    os.unlink(exe_name)
            except:
                pass


class MultiLanguageExecutor:
    def __init__(self):
        self.python_tracer = PythonTracer()
        self.js_executor = JavaScriptExecutor()
        self.c_executor = CExecutor()
    
    def execute(self, code, language):
        """Exécute le code dans le langage spécifié"""
        language = language.lower()
        
        if language == 'python':
            return self.python_tracer.run_code(code)
        elif language in ['javascript', 'js']:
            return self.js_executor.run_code(code)
        elif language == 'c':
            return self.c_executor.run_code(code)
        else:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": f"Langage non supporté: {language}. Langages disponibles: python, javascript, c"
            }]


class CodeExecutionHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.executor = MultiLanguageExecutor()
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Gestion des requêtes CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Gestion des requêtes POST pour exécuter du code"""
        if self.path == '/run':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                code = data.get('code', '')
                language = data.get('language', 'python')
                
                print(f"Exécution de code {language}: {code[:50]}...")
                
                trace = self.executor.execute(code, language)
                response = {"trace": trace}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                print(f"Erreur lors de l'exécution: {e}")
                error_response = {"error": str(e), "trace": []}
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Gestion des requêtes GET pour les informations de l'API"""
        if self.path == '/':
            response = {
                "message": "Multi-Language Code Executor API", 
                "languages": ["python", "javascript", "c"],
                "endpoints": ["/run (POST)", "/ (GET)"]
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Logging personnalisé"""
        print(f"[{self.address_string()}] {format % args}")


if __name__ == "__main__":
    PORT = 8001  # Changement de port pour éviter les conflits
    print(f"🚀 Démarrage du serveur Multi-Language Code Executor...")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"🔧 Langages supportés: Python, JavaScript, C")
    print(f"🌐 CORS activé pour toutes les origines")
    
    try:
        with socketserver.TCPServer(("", PORT), CodeExecutionHandler) as httpd:
            print(f"✅ Serveur en cours d'exécution sur le port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
    except Exception as e:
        print(f"❌ Erreur: {e}")

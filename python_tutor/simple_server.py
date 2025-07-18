#!/usr/bin/env python3
"""
Simple Multi-Language Code Executor
D_L_H Tutor API Server - Version Multi-langages
Support Python, JavaScript et C avec visualisation d'exécution
"""

import sys
import json
import http.server
import socketserver
import subprocess
import tempfile
import os
from urllib.parse import parse_qs

class SimpleCodeExecutor:
    def execute_python(self, code):
        """Exécute du code Python de manière simple"""
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
                }
            }
            
            # Variables pour tracer
            local_vars = {}
            
            # Exécution ligne par ligne
            lines = code.strip().split('\n')
            trace = []
            
            for i, line in enumerate(lines, 1):
                if line.strip():
                    try:
                        exec(line, safe_globals, local_vars)
                        trace.append({
                            "line": i,
                            "locals": dict(local_vars),
                            "globals": {},
                            "output": "\n".join(output)
                        })
                    except Exception as e:
                        trace.append({
                            "line": i,
                            "locals": dict(local_vars),
                            "globals": {},
                            "output": "\n".join(output),
                            "error": str(e)
                        })
                        break
            
            return trace
            
        except Exception as e:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": str(e)
            }]
    
    def execute_javascript(self, code):
        """Exécute du code JavaScript avec Node.js"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    ['node', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                trace = [{
                    "line": -1,
                    "locals": {},
                    "globals": {},
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip() if result.stderr else None
                }]
                
                return trace
                
            finally:
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": "Timeout: Le code a pris trop de temps à s'exécuter"
            }]
        except FileNotFoundError:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": "Node.js n'est pas installé sur ce système"
            }]
        except Exception as e:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": str(e)
            }]
    
    def execute_c(self, code):
        """Compile et exécute du code C avec GCC"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                c_file = f.name
            
            exe_file = c_file.replace('.c', '')
            
            try:
                # Compilation
                compile_result = subprocess.run(
                    ['gcc', '-o', exe_file, c_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_result.returncode != 0:
                    return [{
                        "line": -1,
                        "locals": {},
                        "globals": {},
                        "output": "",
                        "error": f"Erreur de compilation: {compile_result.stderr}"
                    }]
                
                # Exécution
                run_result = subprocess.run(
                    [exe_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                trace = [{
                    "line": -1,
                    "locals": {},
                    "globals": {},
                    "output": run_result.stdout.strip(),
                    "error": run_result.stderr.strip() if run_result.stderr else None
                }]
                
                return trace
                
            finally:
                # Nettoyage
                if os.path.exists(c_file):
                    os.unlink(c_file)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)
                    
        except subprocess.TimeoutExpired:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": "Timeout: Le code a pris trop de temps à s'exécuter"
            }]
        except FileNotFoundError:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": "GCC n'est pas installé sur ce système"
            }]
        except Exception as e:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": str(e)
            }]
    
    def execute(self, code, language):
        """Point d'entrée principal"""
        language = language.lower()
        if language == 'python':
            return self.execute_python(code)
        elif language == 'javascript':
            return self.execute_javascript(code)
        elif language == 'c':
            return self.execute_c(code)
        else:
            return [{
                "line": -1,
                "locals": {},
                "globals": {},
                "output": "",
                "error": f"Langage '{language}' non supporté. Langages disponibles: python, javascript, c"
            }]


class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.executor = SimpleCodeExecutor()
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/run':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                code = data.get('code', '')
                language = data.get('language', 'python')
                
                trace = self.executor.execute(code, language)
                response = {"trace": trace}
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                try:
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except BrokenPipeError:
                    # Client a fermé la connexion
                    pass
                    
            except BrokenPipeError:
                # Client a fermé la connexion pendant la lecture
                pass
            except Exception as e:
                try:
                    error_response = {"error": str(e), "trace": []}
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                except BrokenPipeError:
                    # Client a fermé la connexion
                    pass
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            response = {"message": "D_L_H Tutor API", "status": "OK", "languages": ["python", "javascript", "c"]}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    PORT = 8002
    print(f"🚀 Serveur D_L_H Tutor Multi-langages")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"� Support: Python, JavaScript, C")
    print(f"📋 Dépendances: Node.js (pour JS), GCC (pour C)")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            print(f"✅ Serveur actif sur le port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Erreur: {e}")

import sys
import traceback
import subprocess
import tempfile
import os
import json
from pathlib import Path

class PythonTracer:
    def __init__(self):
        self.trace = []
        self.output = ""

    def tracer(self, frame, event, arg):
        if event == 'line':
            lineno = frame.f_lineno
            snapshot = {
                "line": lineno,
                "locals": frame.f_locals.copy(),
                "globals": frame.f_globals.copy(),
                "output": self.output
            }
            self.trace.append(snapshot)
        return self.tracer

    def run_code(self, code):
        self.trace = []
        self.output = ""

        global_env = {
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
            }
        }

        try:
            sys.settrace(self.tracer)
            exec(code, global_env)
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

    def _safe_print(self, *args, **kwargs):
        self.output += " ".join(str(a) for a in args) + "\n"


class JavaScriptExecutor:
    def run_code(self, code):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                # Wrapper pour capturer les variables et la sortie
                wrapped_code = f"""
const trace = [];
let lineNumber = 1;

// Console.log override pour capturer la sortie
const originalLog = console.log;
let output = '';
console.log = function(...args) {{
    output += args.join(' ') + '\\n';
    originalLog(...args);
}};

// Fonction pour tracer l'exécution (simplifiée)
function traceExecution() {{
    const variables = {{}};
    // Capturer les variables dans le scope global
    for (let key in globalThis) {{
        if (typeof globalThis[key] !== 'function' && !key.startsWith('_') && key !== 'trace' && key !== 'output') {{
            try {{
                variables[key] = globalThis[key];
            }} catch(e) {{
                variables[key] = '[Error accessing variable]';
            }}
        }}
    }}
    return variables;
}}

try {{
    {code}
    
    // Trace finale
    trace.push({{
        line: -1,
        locals: traceExecution(),
        globals: {{}},
        output: output
    }});
}} catch (error) {{
    trace.push({{
        line: -1,
        locals: {{}},
        globals: {{}},
        output: output,
        error: error.toString()
    }});
}}

console.log('TRACE_OUTPUT:', JSON.stringify(trace));
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
                
                # Extraire la trace de la sortie
                output_lines = result.stdout.split('\n')
                trace_line = None
                for line in output_lines:
                    if line.startswith('TRACE_OUTPUT:'):
                        trace_line = line.replace('TRACE_OUTPUT:', '').strip()
                        break
                
                if trace_line:
                    return json.loads(trace_line)
                else:
                    return [{
                        "line": -1,
                        "locals": {},
                        "globals": {},
                        "output": result.stdout,
                        "error": None
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
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                # Wrapper C avec des includes de base
                wrapped_code = f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {{
    printf("=== EXECUTION START ===\\n");
{code}
    printf("=== EXECUTION END ===\\n");
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
                        "error": f"Compilation Error: {compile_result.stderr}"
                    }]
                
                # Exécution
                run_result = subprocess.run([exe_name], 
                                          capture_output=True, text=True, timeout=10)
                
                if run_result.returncode != 0:
                    return [{
                        "line": -1,
                        "locals": {},
                        "globals": {},
                        "output": run_result.stdout,
                        "error": run_result.stderr
                    }]
                
                return [{
                    "line": -1,
                    "locals": {},
                    "globals": {},
                    "output": run_result.stdout,
                    "error": None
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
        language = language.lower()
        
        if language == 'python':
            return self.python_tracer.run_code(code)
        elif language == 'javascript' or language == 'js':
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


# === API HTTP Simple ===

import http.server
import socketserver
import urllib.parse
import json

class CodeExecutionHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.executor = MultiLanguageExecutor()
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
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
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
        if self.path == '/':
            response = {"message": "Multi-Language Code Executor API", "languages": ["python", "javascript", "c"]}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8000
    print(f"🚀 Démarrage du serveur Multi-Language Code Executor...")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"🔧 Langages supportés: Python, JavaScript, C")
    
    with socketserver.TCPServer(("", PORT), CodeExecutionHandler) as httpd:
        print(f"✅ Serveur en cours d'exécution sur le port {PORT}")
        httpd.serve_forever()

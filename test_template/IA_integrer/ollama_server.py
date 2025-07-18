#!/usr/bin/env python3
"""
Serveur Proxy pour Ollama Chatbot
Gère les requêtes CORS et facilite l'interaction avec Ollama
"""

import json
import asyncio
import aiohttp
from aiohttp import web, ClientTimeout
from aiohttp_cors import setup as cors_setup, ResourceOptions
import logging
import sys
from pathlib import Path

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaProxy:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.session = None
        
    async def start(self):
        """Initialise la session HTTP"""
        timeout = ClientTimeout(total=300)  # 5 minutes timeout
        self.session = aiohttp.ClientSession(timeout=timeout)
        
    async def stop(self):
        """Ferme la session HTTP"""
        if self.session:
            await self.session.close()
            
    async def check_ollama_status(self):
        """Vérifie si Ollama est accessible"""
        try:
            async with self.session.get(f"{self.ollama_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "connected", "models": data.get("models", [])}
                else:
                    return {"status": "error", "message": f"HTTP {response.status}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_models(self):
        """Récupère la liste des modèles disponibles"""
        try:
            async with self.session.get(f"{self.ollama_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("models", [])
                else:
                    return []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des modèles: {e}")
            return []
    
    async def chat_with_model(self, model, messages, stream=False):
        """Envoie une requête de chat à Ollama"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            }
            
            async with self.session.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response": data.get("message", {}).get("content", ""),
                        "model": model
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}"
                    }
                    
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Timeout: Le modèle met trop de temps à répondre"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de communication: {str(e)}"
            }

# Instance globale du proxy
ollama_proxy = OllamaProxy()

async def handle_status(request):
    """Endpoint pour vérifier le statut d'Ollama"""
    try:
        result = await ollama_proxy.check_ollama_status()
        return web.json_response(result)
    except Exception as e:
        return web.json_response({
            "status": "error",
            "message": f"Erreur serveur: {str(e)}"
        }, status=500)

async def handle_models(request):
    """Endpoint pour récupérer les modèles disponibles"""
    try:
        models = await ollama_proxy.get_models()
        return web.json_response({"models": models})
    except Exception as e:
        return web.json_response({
            "error": f"Erreur lors de la récupération des modèles: {str(e)}"
        }, status=500)

async def handle_chat(request):
    """Endpoint pour le chat avec Ollama"""
    try:
        data = await request.json()
        
        model = data.get("model", "llama2")
        messages = data.get("messages", [])
        
        if not messages:
            return web.json_response({
                "success": False,
                "error": "Aucun message fourni"
            }, status=400)
        
        result = await ollama_proxy.chat_with_model(model, messages)
        return web.json_response(result)
        
    except json.JSONDecodeError:
        return web.json_response({
            "success": False,
            "error": "JSON invalide"
        }, status=400)
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": f"Erreur serveur: {str(e)}"
        }, status=500)

async def handle_index(request):
    """Sert la page HTML du chatbot"""
    try:
        html_path = Path(__file__).parent / "ollama-chatbot.html"
        
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(
                text="Fichier ollama-chatbot.html non trouvé",
                status=404
            )
    except Exception as e:
        return web.Response(
            text=f"Erreur lors du chargement de la page: {str(e)}",
            status=500
        )

async def init_app():
    """Initialise l'application web"""
    app = web.Application()
    
    # Configuration CORS
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Routes API
    app.router.add_get('/api/status', handle_status)
    app.router.add_get('/api/models', handle_models)
    app.router.add_post('/api/chat', handle_chat)
    
    # Route pour la page principale
    app.router.add_get('/', handle_index)
    
    # Ajouter CORS à toutes les routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    # Initialiser le proxy Ollama
    await ollama_proxy.start()
    
    return app

async def cleanup(app):
    """Nettoyage lors de l'arrêt du serveur"""
    await ollama_proxy.stop()

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Serveur Proxy Ollama Chatbot")
    parser.add_argument('--host', default='localhost', help='Adresse d\'écoute (défaut: localhost)')
    parser.add_argument('--port', type=int, default=8080, help='Port d\'écoute (défaut: 8080)')
    parser.add_argument('--ollama-url', default='http://localhost:11434', help='URL d\'Ollama (défaut: http://localhost:11434)')
    
    args = parser.parse_args()
    
    # Configuration du proxy Ollama
    global ollama_proxy
    ollama_proxy = OllamaProxy(args.ollama_url)
    
    # Création de l'application
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        app = loop.run_until_complete(init_app())
        
        # Configuration du cleanup
        app.on_cleanup.append(cleanup)
        
        print(f"🚀 Serveur Ollama Chatbot démarré")
        print(f"📍 URL: http://{args.host}:{args.port}")
        print(f"🤖 Ollama URL: {args.ollama_url}")
        print(f"📝 Interface: http://{args.host}:{args.port}/")
        print(f"🔧 API Status: http://{args.host}:{args.port}/api/status")
        print("\n💡 Assurez-vous qu'Ollama est démarré avec: ollama serve")
        print("💡 Pour installer un modèle: ollama pull llama2")
        
        web.run_app(app, host=args.host, port=args.port)
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
    finally:
        loop.close()

if __name__ == "__main__":
    main()

#!/bin/bash

# Script de gestion Docker pour Holbies Learning Hub
# Usage: ./docker-manager.sh [start|stop|restart|logs|status|clean]

set -e

COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="holbies"

case "$1" in
    start)
        echo "🚀 Démarrage de Holbies Learning Hub..."
        docker-compose -f $COMPOSE_FILE up -d --build
        echo "✅ Application démarrée!"
        echo "   Web (nginx): http://localhost:80"
        echo "   Web (direct): http://localhost:8000"
        echo "   Database: localhost:5432"
        ;;
    
    stop)
        echo "⏹️  Arrêt de Holbies Learning Hub..."
        docker-compose -f $COMPOSE_FILE down
        echo "✅ Application arrêtée!"
        ;;
    
    restart)
        echo "🔄 Redémarrage de Holbies Learning Hub..."
        docker-compose -f $COMPOSE_FILE down
        docker-compose -f $COMPOSE_FILE up -d --build
        echo "✅ Application redémarrée!"
        ;;
    
    logs)
        echo "📋 Logs de l'application (Ctrl+C pour arrêter):"
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
    
    status)
        echo "📊 État des services:"
        docker-compose -f $COMPOSE_FILE ps
        echo ""
        echo "🌐 Services disponibles:"
        if docker-compose -f $COMPOSE_FILE ps | grep -q "Up"; then
            echo "   ✅ Web (nginx): http://localhost:80"
            echo "   ✅ Web (direct): http://localhost:8000"
            echo "   ✅ Database: localhost:5432"
        else
            echo "   ❌ Services arrêtés"
        fi
        ;;
    
    clean)
        echo "🧹 Nettoyage complet..."
        docker-compose -f $COMPOSE_FILE down -v
        docker system prune -f
        echo "✅ Nettoyage terminé!"
        ;;
    
    shell)
        echo "🐚 Accès shell au conteneur web..."
        docker-compose -f $COMPOSE_FILE exec web /bin/bash
        ;;
    
    db)
        echo "🗄️  Accès à la base de données..."
        docker-compose -f $COMPOSE_FILE exec db psql -U holberton_user -d holberton_db
        ;;
    
    *)
        echo "Usage: $0 [start|stop|restart|logs|status|clean|shell|db]"
        echo ""
        echo "Commands:"
        echo "  start    - Démarre l'application"
        echo "  stop     - Arrête l'application"
        echo "  restart  - Redémarre l'application"
        echo "  logs     - Affiche les logs en temps réel"
        echo "  status   - Affiche l'état des services"
        echo "  clean    - Nettoie complètement les conteneurs et volumes"
        echo "  shell    - Accède au shell du conteneur web"
        echo "  db       - Accède à la base de données PostgreSQL"
        exit 1
        ;;
esac

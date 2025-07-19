/**
 * Admin Page JavaScript Functions
 * Gestion des utilisateurs et console admin
 */

// =============================================================================
// Fonctions de gestion des utilisateurs
// =============================================================================

async function toggleAdmin(userId) {
    if (confirm('Êtes-vous sûr de vouloir modifier les privilèges administrateur ?')) {
        try {
            const response = await fetch(`/admin/users/${userId}/toggle-admin`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Erreur lors de la modification');
            }
        } catch (error) {
            alert('Erreur réseau');
        }
    }
}

async function deleteUser(userId, username) {
    if (confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur "${username}" ?`)) {
        try {
            const response = await fetch(`/admin/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                document.getElementById(`user-${userId}`).remove();
                alert('Utilisateur supprimé avec succès');
            } else {
                alert('Erreur lors de la suppression');
            }
        } catch (error) {
            alert('Erreur réseau');
        }
    }
}

function editUser(userId) {
    // TODO: Implémenter la modification d'utilisateur
    alert('Fonctionnalité de modification à implémenter');
}

function exportData() {
    alert('Export des données en cours...');
    // TODO: Implémenter l'export
}

function systemCheck() {
    alert('Vérification système lancée...');
    // TODO: Implémenter la vérification
}

// =============================================================================
// Console terminal pour admin
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const terminalInput = document.getElementById('terminal-input');
    const terminalOutput = document.getElementById('terminal-output');

    if (terminalInput) {
        terminalInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                processAdminCommand(this.value);
                this.value = '';
            }
        });
    }

    function processAdminCommand(command) {
        // Ajouter la commande à l'historique
        addTerminalLine(`admin@matrix:~$ ${command}`, 'command');
        
        // Traiter la commande
        switch(command.toLowerCase().trim()) {
            case 'help':
                addTerminalLine('Commandes disponibles:', 'output');
                addTerminalLine('- users: Liste des utilisateurs', 'output');
                addTerminalLine('- stats: Statistiques système', 'output');
                addTerminalLine('- logs: Logs récents', 'output');
                addTerminalLine('- clear: Nettoyer la console', 'output');
                break;
            case 'users':
                addTerminalLine(`👥 ${document.querySelectorAll('tbody tr').length} utilisateurs actifs`, 'output');
                break;
            case 'stats':
                addTerminalLine('📊 Statistiques système:', 'output');
                addTerminalLine(`- Utilisateurs: ${document.querySelector('.highlight-card .stat-number').textContent}`, 'output');
                addTerminalLine(`- Quiz: ${document.querySelector('.success-card .stat-number').textContent}`, 'output');
                addTerminalLine(`- Admins: ${document.querySelector('.info-card .stat-number').textContent}`, 'output');
                break;
            case 'clear':
                terminalOutput.innerHTML = '';
                break;
            case 'matrix':
                addTerminalLine('🔴💊 Bienvenue dans la Matrice...', 'matrix');
                break;
            default:
                addTerminalLine(`Commande inconnue: ${command}`, 'error');
                addTerminalLine('Tapez "help" pour voir les commandes disponibles', 'output');
        }
    }

    function addTerminalLine(text, type = 'output') {
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        line.textContent = text;
        terminalOutput.appendChild(line);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
});

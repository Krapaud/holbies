// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // --- Animation de frappe (attente de la fonction universelle) ---
    function initLoginAnimation() {
        console.log('🔧 DEBUG: Initialisation animation login...');
        
        // Vérifier que l'élément existe
        const container = document.getElementById('code-animation-container');
        console.log('🔧 DEBUG: Container trouvé:', container);
        
        if (!container) {
            console.error('❌ Container #code-animation-container non trouvé !');
            return;
        }
        
        const codeElement = container.querySelector('code');
        console.log('🔧 DEBUG: Code element trouvé:', codeElement);
        
        if (!codeElement) {
            console.error('❌ Element code non trouvé dans le container !');
            return;
        }

        const loginCodeLines = [
          "// Système d'authentification HOLBIES",
          "class AuthenticationService {",
          "  constructor() {",
          "    this.database = new Database();",
          "    this.tokenService = new TokenService();",
          "    this.security = new SecurityManager();",
          "  }",
          "",
          "  async authenticate(username, password) {",
          "    console.log(`Tentative de connexion pour: ${username}`);",
          "    ",
          "    // Validation des entrées",
          "    if (!this.validateInput(username, password)) {",
          "      return { success: false, message: 'Données invalides' };",
          "    }",
          "",
          "    // Recherche utilisateur",
          "    const user = await this.database.findUser(username);",
          "    if (!user) {",
          "      console.warn('Utilisateur non trouvé');",
          "      return { success: false, message: 'Identifiants incorrects' };",
          "    }",
          "",
          "    // Vérification du mot de passe",
          "    const isValid = await this.security.verifyPassword(",
          "      password, ",
          "      user.hashedPassword",
          "    );",
          "",
          "    if (!isValid) {",
          "      console.warn('Mot de passe incorrect');",
          "      return { success: false, message: 'Identifiants incorrects' };",
          "    }",
          "",
          "    // Génération du token",
          "    const token = this.tokenService.generate({",
          "      userId: user.id,",
          "      username: user.username,",
          "      role: user.role,",
          "      timestamp: Date.now()",
          "    });",
          "",
          "    console.log('Authentification réussie!');",
          "    return { ",
          "      success: true, ",
          "      token: token,",
          "      user: { id: user.id, username: user.username }",
          "    };",
          "  }",
          "",
          "  validateInput(username, password) {",
          "    return username && password && ",
          "           username.length >= 3 && ",
          "           password.length >= 6;",
          "  }",
          "}",
          "",
          "// Initialisation du service d'authentification",
          "const authService = new AuthenticationService();",
          "",
          "// Simulation d'une connexion",
          "authService.authenticate('holbies_user', 'secure_password')",
          "  .then(result => {",
          "    if (result.success) {",
          "      console.log('Redirection vers le dashboard...');",
          "    } else {",
          "      console.error('Échec de la connexion:', result.message);",
          "    }",
          "  });"
        ];

        // Utiliser la nouvelle fonction universelle
        if (window.createAdaptiveTerminalAnimation) {
            console.log('✅ Fonction createAdaptiveTerminalAnimation trouvée !');
            const loginAnimation = window.createAdaptiveTerminalAnimation(
                'code-animation-container',
                loginCodeLines,
                {
                    typingSpeed: 30,
                    lineDelay: 300,
                    restartDelay: 5000,
                    scrollOffset: 15
                }
            );
            
            if (loginAnimation) {
                console.log('✅ Animation créée avec succès, démarrage...');
                loginAnimation.start();
            } else {
                console.error('❌ Échec de création de l\'animation');
            }
        } else {
            console.log('⏳ Attente du chargement de terminal-animation.js...');
            // Attendre que la fonction soit disponible
            setTimeout(initLoginAnimation, 100);
        }
    }

    // Démarrer l'animation
    try {
        console.log('🚀 Démarrage de l\'animation login...');
        initLoginAnimation();
    } catch (e) {
        console.error('💥 Erreur animation terminal login:', e);
    }});

async function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (window.holbiesApp) {
        window.holbiesApp.showLoading(submitBtn);
    }

    try {
        const response = await fetch('/api/auth/token', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token', data.access_token); // Pour compatibilité avec main.js
            
            // Récupérer les informations utilisateur et synchroniser la session
            const userResponse = await fetch('/api/users/me', {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`
                }
            });
            
            if (userResponse.ok) {
                const userData = await userResponse.json();
                
                // Synchroniser la session côté serveur
                await fetch('/api/users/sync-session', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${data.access_token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: userData.id,
                        username: userData.username
                    })
                });
            }
            
            if (window.holbiesApp) {
                window.holbiesApp.token = data.access_token;
                // Force update navigation after successful login
                setTimeout(() => {
                    window.holbiesApp.updateAuthLink();
                }, 100);
                if (window.holbiesApp.showMessage) {
                    window.holbiesApp.showMessage('Connexion réussie!', 'success');
                }
                if (window.holbiesApp.showWelcomeVideo) {
                    window.holbiesApp.showWelcomeVideo(() => {
                        window.location.href = '/dashboard';
                    });
                } else {
                    window.location.href = '/dashboard';
                }
            } else {
                window.location.href = '/dashboard';
            }
        } else {
            throw new Error(data.detail || 'Erreur de connexion');
        }
    } catch (error) {
        console.error('Login error:', error);
        if (window.holbiesApp && window.holbiesApp.showMessage) {
            window.holbiesApp.showMessage(error.message, 'error');
        }
    } finally {
        if (window.holbiesApp && window.holbiesApp.hideLoading) {
            window.holbiesApp.hideLoading(submitBtn);
        }
    }
}
// Script for register.html
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }


    // --- Animation de frappe (attente de la fonction universelle) ---
    function initRegisterAnimation() {
        console.log('🔧 DEBUG: Initialisation animation register...');
        
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

        const registerCodeLines = [
          "// Système d'inscription HOLBIES",
          "class UserRegistrationService {",
          "  constructor() {",
          "    this.database = new Database();",
          "    this.validator = new InputValidator();",
          "    this.encryption = new PasswordEncryption();",
          "    this.emailService = new EmailService();",
          "  }",
          "",
          "  async registerUser(userData) {",
          "    console.log('Début du processus d\\'inscription...');",
          "",
          "    // Validation des données",
          "    const validation = this.validator.validate(userData);",
          "    if (!validation.isValid) {",
          "      return { success: false, errors: validation.errors };",
          "    }",
          "",
          "    // Vérification unicité",
          "    const existingUser = await this.database.findByEmail(userData.email);",
          "    if (existingUser) {",
          "      return { success: false, message: 'Email déjà utilisé' };",
          "    }",
          "",
          "    const existingUsername = await this.database.findByUsername(",
          "      userData.username",
          "    );",
          "    if (existingUsername) {",
          "      return { success: false, message: 'Nom d\\'utilisateur pris' };",
          "    }",
          "",
          "    // Chiffrement du mot de passe",
          "    const hashedPassword = await this.encryption.hash(",
          "      userData.password",
          "    );",
          "",
          "    // Création de l'utilisateur",
          "    const newUser = {",
          "      username: userData.username,",
          "      email: userData.email,",
          "      password: hashedPassword,",
          "      createdAt: new Date().toISOString(),",
          "      isActive: true,",
          "      role: 'student'",
          "    };",
          "",
          "    try {",
          "      const userId = await this.database.createUser(newUser);",
          "      ",
          "      // Envoi email de bienvenue",
          "      await this.emailService.sendWelcomeEmail({",
          "        email: newUser.email,",
          "        username: newUser.username",
          "      });",
          "",
          "      console.log(`Utilisateur ${userId} créé avec succès!`);",
          "      return { ",
          "        success: true, ",
          "        userId: userId,",
          "        message: 'Inscription réussie!'",
          "      };",
          "    } catch (error) {",
          "      console.error('Erreur lors de la création:', error);",
          "      return { success: false, message: 'Erreur serveur' };",
          "    }",
          "  }",
          "}",
          "",
          "// Initialisation du service d'inscription",
          "const registrationService = new UserRegistrationService();",
          "",
          "// Simulation d'une inscription",
          "const newUserData = {",
          "  username: 'nouveau_holbies',",
          "  email: 'dev@holbies.com',",
          "  password: 'motdepassesecurise123'",
          "};",
          "",
          "registrationService.registerUser(newUserData)",
          "  .then(result => {",
          "    if (result.success) {",
          "      console.log('Redirection vers la page de connexion...');",
          "    } else {",
          "      console.error('Échec de l\\'inscription:', result.message);",
          "    }",
          "  });"
        ];

        // Utiliser la nouvelle fonction universelle
        if (window.createAdaptiveTerminalAnimation) {
            console.log('✅ Fonction createAdaptiveTerminalAnimation trouvée !');
            const registerAnimation = window.createAdaptiveTerminalAnimation(
                'code-animation-container',
                registerCodeLines,
                {
                    typingSpeed: 30,
                    lineDelay: 300,
                    restartDelay: 5000,
                    scrollOffset: 15
                }
            );
            
            if (registerAnimation) {
                console.log('✅ Animation créée avec succès, démarrage...');
                registerAnimation.start();
            } else {
                console.error('❌ Échec de création de l\'animation');
            }
        } else {
            console.log('⏳ Attente du chargement de terminal-animation.js...');
            // Attendre que la fonction soit disponible
            setTimeout(initRegisterAnimation, 100);
        }
    }

    // Démarrer l'animation
    try {
        console.log('🚀 Démarrage de l\'animation register...');
        initRegisterAnimation();
    } catch (e) {
        console.error('💥 Erreur animation terminal register:', e);
    }

    
});

async function handleRegister(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm-password');
    
    if (password !== confirmPassword) {
        if (window.holbiesApp && window.holbiesApp.showMessage) {
            window.holbiesApp.showMessage('Les mots de passe ne correspondent pas', 'error');
        }
        return;
    }

    if (window.holbiesApp && window.holbiesApp.showLoading) {
        window.holbiesApp.showLoading(submitBtn);
    }

    try {
        const userData = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        };

        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            if (window.holbiesApp && window.holbiesApp.showMessage) {
                window.holbiesApp.showMessage('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success');
            }
            
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            throw new Error(data.detail || 'Erreur d\'inscription');
        }
    } catch (error) {
        if (window.holbiesApp && window.holbiesApp.showMessage) {
            window.holbiesApp.showMessage(error.message, 'error');
        }
    } finally {
        if (window.holbiesApp && window.holbiesApp.hideLoading) {
            window.holbiesApp.hideLoading(submitBtn);
        }
    }
}
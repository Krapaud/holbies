// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // --- Animation de frappe (copie register.js) ---
    try {
        const codeContainer = document.getElementById('code-animation-container');
        if (!codeContainer) {
            return; // Ne rien faire si le conteneur n'est pas sur la page
        }

        const codeElement = codeContainer.querySelector('code');
        if (!codeElement) {
            return;
        }

        const codeLines = [
          "// Authentification de l'utilisateur",
          "async function authenticate(username, password) {",
          "  const user = await findUserByUsername(username);",
          "  if (!user) {",
          "    return { success: false, message: 'Utilisateur non trouvé' };",
          "  }",
          "  ",
          "  const isPasswordValid = await verifyPassword(password, user.hashedPassword);",
          "  if (!isPasswordValid) {",
          "    return { success: false, message: 'Mot de passe incorrect' };",
          "  }",
          "  ",
          "  const token = generateAuthToken(user.id);",
          "  return { success: true, token: token };",
          "}",
          "",
          "// Tentative de connexion...",
          "authenticate('utilisateur_holbies', 'mon_mot_de_passe_secret');"
        ];
        
        const cursorElement = document.createElement('span');
        cursorElement.classList.add('cursor');
        
        codeElement.innerHTML = ''; // Clear content initially
        codeElement.appendChild(cursorElement); // Append cursor first

        let currentContent = '';
        let lineIndex = 0;
        let charIndex = 0;

        function typeCode() {
            if (lineIndex >= codeLines.length) {
                setTimeout(() => {
                    lineIndex = 0;
                    charIndex = 0;
                    currentContent = '';
                    codeElement.textContent = '';
                    codeElement.appendChild(cursorElement);
                    // Force scroll to top - seulement le conteneur terminal
                    requestAnimationFrame(() => {
                        if (codeContainer) {
                            codeContainer.scrollTop = 0;
                        }
                    });
                    typeCode();
                }, 4000);
                return;
            }
    
            const currentLine = codeLines[lineIndex];
            if (charIndex < currentLine.length) {
                currentContent += currentLine[charIndex];
                codeElement.textContent = currentContent;
                codeElement.appendChild(cursorElement);
                charIndex++;
                
                // Scroll UNIQUEMENT dans le conteneur terminal, pas la page entière
                if (codeContainer && cursorElement) {
                    setTimeout(() => {
                        // Calculer la position du curseur dans le conteneur seulement
                        const containerRect = codeContainer.getBoundingClientRect();
                        const cursorRect = cursorElement.getBoundingClientRect();
                        
                        // Scroll seulement si le curseur sort du conteneur visible
                        if (cursorRect.bottom > containerRect.bottom) {
                            codeContainer.scrollTop += (cursorRect.bottom - containerRect.bottom + 10);
                        }
                    }, 10);
                }
                
                setTimeout(typeCode, 45);
            } else {
                currentContent += '\n';
                codeElement.textContent = currentContent;
                codeElement.appendChild(cursorElement);
                lineIndex++;
                charIndex = 0;
                
                // Scroll UNIQUEMENT dans le conteneur terminal, pas la page entière
                if (codeContainer && cursorElement) {
                    setTimeout(() => {
                        // Calculer la position du curseur dans le conteneur seulement
                        const containerRect = codeContainer.getBoundingClientRect();
                        const cursorRect = cursorElement.getBoundingClientRect();
                        
                        // Scroll seulement si le curseur sort du conteneur visible
                        if (cursorRect.bottom > containerRect.bottom) {
                            codeContainer.scrollTop += (cursorRect.bottom - containerRect.bottom + 10);
                        }
                    }, 10);
                }
                
                setTimeout(typeCode, 600);
            }
        }
    
        // Start the animation after a short delay
        setTimeout(typeCode, 1000);

    } catch (e) {
        // En cas d'erreur, on ne bloque pas le reste du site
    }

});

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
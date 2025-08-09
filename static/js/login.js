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
            console.log('typeCode function called');
            if (lineIndex >= codeLines.length) {
                setTimeout(() => {
                    lineIndex = 0;
                    charIndex = 0;
                    currentContent = ''; // Reset content
                    codeElement.textContent = ''; // Clear the displayed text
                    codeElement.appendChild(cursorElement); // Re-append cursor
                    codeContainer.scrollTop = 0; // Reset scroll to top
                    typeCode();
                }, 3000);
                return;
            }
    
            const currentLine = codeLines[lineIndex];
            if (charIndex < currentLine.length) {
                currentContent += currentLine[charIndex];
                codeElement.textContent = currentContent; // Update textContent
                codeElement.appendChild(cursorElement); // Keep cursor at the end
                charIndex++;
                // Auto-scroll to follow the cursor
                codeContainer.scrollTop = codeContainer.scrollHeight;
                setTimeout(typeCode, 40);
            } else {
                currentContent += '\n';
                codeElement.textContent = currentContent; // Update textContent with newline
                codeElement.appendChild(cursorElement); // Keep cursor at the end
                lineIndex++;
                charIndex = 0;
                // Ensure scroll follows the new line
                codeContainer.scrollTop = codeContainer.scrollHeight;
                setTimeout(typeCode, 500);
            }
        }
    
        typeCode();

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
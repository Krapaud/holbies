// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // --- Animation de frappe ---
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
          "import { createConnection } from 'mysql2/promise';",
          "",
          "async function attemptLogin(username, password) {",
          "  let connection;",
          "  try {",
          "    connection = await createConnection({",
          "      host: 'localhost',",
          "      user: username,",
          "      password: password,",
          "      database: 'holbies_db'",
          "    });",
          "    console.log(`Successfully connected as ${username}!`);",
          "    // Perform authentication query here",
          "    const [rows] = await connection.execute(",
          "      'SELECT id FROM users WHERE username = ? AND password = ?',",
          "      [username, password]",
          "    );",
          "    if (rows.length > 0) {",
          "      console.log('Authentication successful.');",
          "      return true;",
          "    } else {",
          "      console.log('Authentication failed: Invalid credentials.');",
          "      return false;",
          "    }",
          "  } catch (error) {",
          "    console.error('Database connection or query error:', error.message);",
          "    return false;",
          "  } finally {",
          "    if (connection) connection.end();",
          "  }",
          "}",
          "",
          "// Simulating a login attempt",
          "attemptLogin('user_holberton', 'password123');"
        ];
        
        const cursorElement = document.createElement('span');
        cursorElement.classList.add('cursor');
        
        let textNode = document.createTextNode('');
        codeElement.innerHTML = ''; // On vide l'élément
        codeElement.appendChild(textNode);
        codeElement.appendChild(cursorElement);

        let lineIndex = 0;
        let charIndex = 0;

        function typeCode() {
            if (lineIndex >= codeLines.length) {
                // Animation terminée, on redémarre
                setTimeout(() => {
                    lineIndex = 0;
                    charIndex = 0;
                    textNode.nodeValue = '';
                    typeCode();
                }, 3000); // Pause avant de redémarrer
                return;
            }
    
            const currentLine = codeLines[lineIndex];
            if (charIndex < currentLine.length) {
                textNode.nodeValue += currentLine[charIndex];
                charIndex++;
                setTimeout(typeCode, 40); // Vitesse de frappe
            } else {
                textNode.nodeValue += '\n';
                lineIndex++;
                charIndex = 0;
                setTimeout(typeCode, 500); // Pause entre les lignes
            }
        }
    
        typeCode();

    } catch (e) {
        // En cas d'erreur, on ne bloque pas le reste du site
        console.error("Erreur lors de l'initialisation de l'animation :", e);
    }
    // --- Fin de l'animation ---

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
            if (window.holbiesApp) {
                window.holbiesApp.token = data.access_token;
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
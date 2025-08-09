// Script for register.html
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }


    // --- Animation de frappe (copie login.js) ---
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
          "const db = require('./database');",
          "",
          "async function addUser(user) {",
          "  const query = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)';",
          "  const params = [user.username, user.email, user.password];",
          "  ",
          "  try {",
          "    await db.run(query, params);",
          "    console.log(`User ${user.username} added successfully.`);",
          "  } catch (error) {",
          "    console.error('Error adding user:', error);",
          "  }",
          "}",
          "",
          "addUser({",
          "  username: 'nouveau_developpeur',",
          "  email: 'dev@holbies.com',",
          "  password: 'motdepassesecurise'",
          "});"
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
                codeContainer.scrollTop = codeContainer.scrollHeight; // Auto-scroll
                setTimeout(typeCode, 40);
            } else {
                currentContent += "\n";
                codeElement.textContent = currentContent; // Update textContent with newline
                codeElement.appendChild(cursorElement); // Keep cursor at the end
                lineIndex++;
                charIndex = 0;
                codeContainer.scrollTop = codeContainer.scrollHeight; // Auto-scroll
                setTimeout(typeCode, 500);
            }
        }
    
        typeCode();

    } catch (e) {
        // En cas d'erreur, on ne bloque pas le reste du site
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
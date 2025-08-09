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
        
        let textNode = document.createTextNode('');
        codeElement.innerHTML = '';
        codeElement.appendChild(textNode);
        codeElement.appendChild(cursorElement);

        let lineIndex = 0;
        let charIndex = 0;

        function typeCode() {
            if (lineIndex >= codeLines.length) {
                setTimeout(() => {
                    lineIndex = 0;
                    charIndex = 0;
                    textNode.nodeValue = '';
                    typeCode();
                }, 3000);
                return;
            }
    
            const currentLine = codeLines[lineIndex];
            if (charIndex < currentLine.length) {
                textNode.nodeValue += currentLine[charIndex];
                charIndex++;
                setTimeout(typeCode, 40);
            } else {
                textNode.nodeValue += '\n';
                lineIndex++;
                charIndex = 0;
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
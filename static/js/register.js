// Script for register.html
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Initialize auth visual animation if present
    if (window.holbiesApp && document.querySelector('.auth-visual')) {
        window.holbiesApp.animateAuthVisual();
    }

    // Initialize password strength indicator
    if (window.holbiesApp && window.holbiesApp.addPasswordStrengthIndicator) {
        window.holbiesApp.addPasswordStrengthIndicator();
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
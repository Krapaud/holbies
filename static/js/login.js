// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Initialize auth visual animation if present
    if (window.holbiesApp && document.querySelector('.auth-visual')) {
        window.holbiesApp.animateAuthVisual();
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
            if (window.holbiesApp) {
                window.holbiesApp.token = data.access_token;
            }
            
            if (window.holbiesApp && window.holbiesApp.showMessage) {
                window.holbiesApp.showMessage('Connexion réussie!', 'success');
            }
            
            if (window.holbiesApp && window.holbiesApp.showWelcomeVideo) {
                window.holbiesApp.showWelcomeVideo(() => {
                    window.location.href = '/dashboard';
                });
            } else {
                window.location.href = '/dashboard';
            }
        } else {
            throw new Error(data.detail || 'Erreur de connexion');
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

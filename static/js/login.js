// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    console.log('loginForm element:', loginForm);
    if (loginForm) {
        console.log('Adding submit event listener to loginForm.');
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
            console.log('Login successful. Storing token and attempting redirection.');
            localStorage.setItem('access_token', data.access_token);
            if (window.holbiesApp) {
                window.holbiesApp.token = data.access_token;
            }
            
            if (window.holbiesApp && window.holbiesApp.showMessage) {
                window.holbiesApp.showMessage('Connexion réussie!', 'success');
            }
            
            if (window.holbiesApp && window.holbiesApp.showWelcomeVideo) {
                console.log('Calling showWelcomeVideo...');
                window.holbiesApp.showWelcomeVideo(() => {
                    console.log('showWelcomeVideo callback executed. Redirecting to /dashboard');
                    window.location.href = '/dashboard';
                });
            } else {
                console.log('showWelcomeVideo not available or not called. Redirecting directly to /dashboard');
                window.location.href = '/dashboard';
            }
        } else {
            console.error('Login failed. Response not OK:', data.detail);
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

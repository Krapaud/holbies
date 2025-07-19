// Authentication JavaScript
document.addEventListener('DOMContentLoaded', () => {
    setupAuthForms();
    animateAuthVisual();
});

function setupAuthForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Show loading
    window.holbiesApp.showLoading(submitBtn);

    try {
        const response = await fetch('/api/auth/token', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            window.holbiesApp.token = data.access_token;
            
            // Show success message
            window.holbiesApp.showMessage('Connexion réussie! Redirection...', 'success');
            
            // Redirect after delay
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } else {
            throw new Error(data.detail || 'Erreur de connexion');
        }
    } catch (error) {
        window.holbiesApp.showMessage(error.message, 'error');
    } finally {
        window.holbiesApp.hideLoading(submitBtn);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Validate passwords match
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm-password');
    
    if (password !== confirmPassword) {
        window.holbiesApp.showMessage('Les mots de passe ne correspondent pas', 'error');
        return;
    }

    // Show loading
    window.holbiesApp.showLoading(submitBtn);

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
            window.holbiesApp.showMessage('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success');
            
            // Redirect to login after delay
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            throw new Error(data.detail || 'Erreur d\'inscription');
        }
    } catch (error) {
        window.holbiesApp.showMessage(error.message, 'error');
    } finally {
        window.holbiesApp.hideLoading(submitBtn);
    }
}

function animateAuthVisual() {
    const codeStreams = document.querySelectorAll('.code-stream span');
    
    codeStreams.forEach((span, index) => {
        span.style.animationDelay = `${index * 0.2}s`;
        
        // Add random glitch effect
        setInterval(() => {
            if (Math.random() < 0.1) {
                span.style.animation = 'glitch 0.3s ease-in-out';
                setTimeout(() => {
                    span.style.animation = `matrixStream 0.5s forwards`;
                    span.style.animationDelay = `${index * 0.2}s`;
                }, 300);
            }
        }, 2000);
    });
}

// Form validation
function setupFormValidation() {
    const inputs = document.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearValidation);
    });
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Remove existing validation
    clearValidation(e);
    
    // Validate based on field type
    let isValid = true;
    let message = '';
    
    if (field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Adresse email invalide';
        }
    } else if (field.name === 'username') {
        if (value.length < 3) {
            isValid = false;
            message = 'Le nom d\'utilisateur doit faire au moins 3 caractères';
        }
    } else if (field.type === 'password') {
        if (value.length < 6) {
            isValid = false;
            message = 'Le mot de passe doit faire au moins 6 caractères';
        }
    }
    
    if (!isValid) {
        showFieldError(field, message);
    }
    
    return isValid;
}

function clearValidation(e) {
    const field = e.target;
    const errorElement = field.parentNode.querySelector('.field-error');
    
    if (errorElement) {
        errorElement.remove();
    }
    
    field.style.borderColor = 'var(--primary-green)';
}

function showFieldError(field, message) {
    field.style.borderColor = 'var(--danger-red)';
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.cssText = `
        color: var(--danger-red);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    `;
    
    field.parentNode.appendChild(errorElement);
}

// Initialize validation
setupFormValidation();

// Add password strength indicator
function addPasswordStrengthIndicator() {
    const passwordField = document.querySelector('input[name="password"]');
    if (!passwordField) return;
    
    const indicator = document.createElement('div');
    indicator.className = 'password-strength';
    indicator.innerHTML = `
        <div class="strength-bar">
            <div class="strength-fill"></div>
        </div>
        <div class="strength-text">Force du mot de passe</div>
    `;
    
    indicator.style.cssText = `
        margin-top: 0.5rem;
    `;
    
    const strengthBar = indicator.querySelector('.strength-fill');
    const strengthText = indicator.querySelector('.strength-text');
    
    passwordField.parentNode.appendChild(indicator);
    
    passwordField.addEventListener('input', (e) => {
        const password = e.target.value;
        const strength = calculatePasswordStrength(password);
        
        strengthBar.style.width = `${strength.percentage}%`;
        strengthBar.style.backgroundColor = strength.color;
        strengthText.textContent = strength.text;
    });
}

function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = 'Très faible';
    let color = 'var(--danger-red)';
    
    if (password.length >= 6) score += 20;
    if (password.length >= 10) score += 20;
    if (/[a-z]/.test(password)) score += 20;
    if (/[A-Z]/.test(password)) score += 20;
    if (/[0-9]/.test(password)) score += 10;
    if (/[^A-Za-z0-9]/.test(password)) score += 10;
    
    if (score >= 80) {
        feedback = 'Très fort';
        color = 'var(--success-green)';
    } else if (score >= 60) {
        feedback = 'Fort';
        color = 'var(--warning-yellow)';
    } else if (score >= 40) {
        feedback = 'Moyen';
        color = 'var(--warning-yellow)';
    } else if (score >= 20) {
        feedback = 'Faible';
        color = 'var(--danger-red)';
    }
    
    return {
        percentage: score,
        text: feedback,
        color: color
    };
}

// Initialize password strength indicator
setTimeout(addPasswordStrengthIndicator, 100);

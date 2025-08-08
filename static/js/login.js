// Script for login.html
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (window.holbiesApp && window.holbiesApp.showLoading) {
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
            
            showWelcomeVideo(() => {
                window.location.href = '/dashboard';
            });
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

function showWelcomeVideo(callback) {
    const waitForVideoModal = () => {
        if (window.videoModal) {
            const videoSources = [
                { url: '/static/video/welcome.mp4', type: 'video/mp4' },
                { url: '/static/video/welcome.webm', type: 'video/webm' },
                { url: '/static/video/welcome.ogv', type: 'video/ogg' }
            ];
            
            let foundVideo = false;
            let checkedSources = 0;
            
            const checkSource = (source) => {
                const testVideo = document.createElement('video');
                testVideo.onloadstart = () => {
                    if (!foundVideo) {
                        foundVideo = true;
                        window.videoModal.show(source.url);
                        
                        const modal = document.getElementById('video-modal');
                        if (modal) {
                            const originalClose = window.videoModal.close.bind(window.videoModal);
                            window.videoModal.close = function() {
                                originalClose();
                                if (callback) {
                                    setTimeout(callback, 500);
                                }
                                window.videoModal.close = originalClose;
                            };
                        }
                    }
                };
                testVideo.onerror = () => {
                    checkedSources++;
                    if (checkedSources >= videoSources.length && !foundVideo) {
                        if (window.showTestWelcomeVideo) {
                            foundVideo = true;
                            window.showTestWelcomeVideo().then(() => {
                                if (callback) {
                                    setTimeout(callback, 500);
                                }
                            });
                        } else {
                            if (callback) {
                                callback();
                            }
                        }
                    }
                };
                testVideo.src = source.url;
            };
            
            videoSources.forEach(checkSource);
            
        } else {
            setTimeout(waitForVideoModal, 100);
        }
    };
    
    waitForVideoModal();
}
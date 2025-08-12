// Profile page enhanced functionality
document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bars on load
    animateProgressBars();
    
    // Add hover effects to activity items
    enhanceActivityItems();
    
    // Add achievement badge animations
    animateAchievements();
    
    // Load real data if available
    loadProfileData();
});

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach((bar, index) => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-out';
            bar.style.width = targetWidth;
        }, index * 200);
    });
}

function enhanceActivityItems() {
    const activityItems = document.querySelectorAll('.activity-item');
    
    activityItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
}

function animateAchievements() {
    const badges = document.querySelectorAll('.achievement-badge');
    
    badges.forEach((badge, index) => {
        badge.style.opacity = '0';
        badge.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            badge.style.transition = 'all 0.3s ease';
            badge.style.opacity = '1';
            badge.style.transform = 'scale(1)';
        }, index * 150);
        
        // Add hover effect
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 4px 12px rgba(255, 215, 0, 0.5)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 2px 8px rgba(255, 215, 0, 0.3)';
        });
    });
}

function loadProfileData() {
    // Simulate loading real user data
    // In a real application, this would fetch from an API
    
    // Animate stat numbers counting up
    animateStatNumbers();
    
    // Add pulse effect to online indicator
    const avatar = document.querySelector('.profile-avatar');
    if (avatar) {
        const indicator = avatar.querySelector('::after');
        setInterval(() => {
            avatar.style.boxShadow = '0 8px 24px rgba(225, 0, 60, 0.5)';
            setTimeout(() => {
                avatar.style.boxShadow = '0 8px 24px rgba(225, 0, 60, 0.3)';
            }, 500);
        }, 2000);
    }
}

function animateStatNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        const isPercentage = finalValue.includes('%');
        const numericValue = parseInt(finalValue.replace('%', ''));
        
        if (!isNaN(numericValue)) {
            let currentValue = 0;
            const increment = Math.ceil(numericValue / 30);
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= numericValue) {
                    currentValue = numericValue;
                    clearInterval(timer);
                }
                
                stat.textContent = currentValue + (isPercentage ? '%' : '');
            }, 50);
        }
    });
}

// Add scroll reveal animation for cards
function revealOnScroll() {
    const cards = document.querySelectorAll('.profile-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// Initialize scroll reveal
revealOnScroll();

// Profile editing functionality (placeholder)
function initProfileEditing() {
    const editBtn = document.querySelector('.edit-profile-btn');
    
    if (editBtn) {
        editBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show a modal or redirect to edit page
            showEditProfileModal();
        });
    }
}

function showEditProfileModal() {
    // Placeholder for profile editing modal
    alert('Fonctionnalité de modification du profil à venir !');
}

// Initialize profile editing
initProfileEditing();

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close any open modals
        closeModals();
    }
});

function closeModals() {
    // Placeholder for closing modals
    console.log('Closing modals...');
}

// Add dynamic theme switching based on user preference
function initThemeToggle() {
    const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (userPrefersDark) {
        document.body.classList.add('dark-theme');
    }
}

// Initialize theme
initThemeToggle();

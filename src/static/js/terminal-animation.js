// 🔧 Animation Terminal Universelle - VERSION HARDCORE SANS SCROLLBAR
// Scroll automatique INVISIBLE - AUCUNE SCROLLBAR VISIBLE + HAUTEUR FORCÉE

function createAdaptiveTerminalAnimation(containerId, codeLines, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`❌ Container ${containerId} non trouvé !`);
        return null;
    }

    const preElement = container.querySelector('pre');
    if (!preElement) {
        console.error(`❌ Element pre non trouvé dans ${containerId} !`);
        return null;
    }

    const codeElement = preElement.querySelector('code');
    if (!codeElement) {
        console.error(`❌ Element code non trouvé dans ${containerId} !`);
        return null;
    }

    // 🔥 FORCER UNE HAUTEUR FIXE CALCULÉE (AUTH OU HERO)
    function forceContainerHeight() {
        try {
            const authVisual = container.closest('.auth-visual');
            const heroTerminal = container.closest('.hero-terminal');
            
            if (authVisual) {
                // CAS AUTH: Synchroniser avec .auth-card
                const authCard = document.querySelector('.auth-card');
                if (authCard) {
                    const cardHeight = authCard.clientHeight;
                    const visualPadding = parseInt(getComputedStyle(authVisual).paddingTop) * 2;
                    const targetHeight = cardHeight - visualPadding;
                    
                    console.log(`🔧 AUTH FORCE HEIGHT: Card=${cardHeight}px, Target=${targetHeight}px`);
                    
                    // FORCER la hauteur de .auth-visual d'abord
                    authVisual.style.height = `${cardHeight}px`;
                    authVisual.style.maxHeight = `${cardHeight}px`;
                    authVisual.style.minHeight = `${cardHeight}px`;
                    
                    // Puis forcer le container et le pre
                    container.style.height = `${targetHeight}px`;
                    container.style.maxHeight = `${targetHeight}px`;
                    container.style.minHeight = `${targetHeight}px`;
                    
                    preElement.style.height = `${targetHeight}px`;
                    preElement.style.maxHeight = `${targetHeight}px`;
                    preElement.style.minHeight = `${targetHeight}px`;
                    
                    console.log(`✅ AUTH Hauteurs forcées: auth-visual=${cardHeight}px, container=${targetHeight}px`);
                }
            } else if (heroTerminal) {
                // CAS HERO: Utiliser les styles CSS existants (pas de modification JS)
                console.log(`🔧 HERO: Utilisation des styles CSS existants pour hero-terminal`);
            }
        } catch (error) {
            console.error('❌ Erreur force height:', error);
        }
    }

    // Options par défaut
    const config = {
        typingSpeed: 35,
        lineDelay: 400,
        restartDelay: 4000,
        scrollOffset: 20,
        ...options
    };

    const cursorElement = document.createElement('span');
    cursorElement.classList.add('cursor');
    
    codeElement.innerHTML = '';
    codeElement.appendChild(cursorElement);

    let currentContent = '';
    let lineIndex = 0;
    let charIndex = 0;
    let isRunning = false;

    // NOUVEAU SYSTÈME DE SCROLL INVISIBLE
    function forceScrollToBottom() {
        if (!preElement) return;
        
        try {
            // Forcer le scroll vers le bas SANS scrollbar visible
            preElement.scrollTop = preElement.scrollHeight;
            
            // Debug
            console.log(`📜 SCROLL: scrollTop=${preElement.scrollTop}, scrollHeight=${preElement.scrollHeight}`);
        } catch (error) {
            console.error('❌ Erreur scroll:', error);
        }
    }

    // Scroll intelligent basé sur la hauteur du contenu
    function smartAutoScroll() {
        if (!preElement || !cursorElement) return;

        try {
            const preHeight = preElement.clientHeight;
            const contentHeight = preElement.scrollHeight;
            
            // Si le contenu dépasse la hauteur visible, scroller
            if (contentHeight > preHeight) {
                const cursorPosition = cursorElement.offsetTop;
                const visibleTop = preElement.scrollTop;
                const visibleBottom = visibleTop + preHeight;
                
                // Si le curseur sort du bas visible, scroller
                if (cursorPosition + config.scrollOffset > visibleBottom) {
                    preElement.scrollTop = Math.max(0, cursorPosition - preHeight + config.scrollOffset * 2);
                }
                
                console.log(`📜 Smart scroll: cursor=${cursorPosition}, visible=${visibleTop}-${visibleBottom}, content=${contentHeight}`);
            }
        } catch (error) {
            console.error('❌ Erreur smart scroll:', error);
        }
    }

    function typeCode() {
        if (!isRunning) return;

        try {
            // Redémarrer l'animation quand elle est terminée
            if (lineIndex >= codeLines.length) {
                setTimeout(() => {
                    if (!isRunning) return;
                    console.log('🔄 Redémarrage animation...');
                    lineIndex = 0;
                    charIndex = 0;
                    currentContent = '';
                    codeElement.textContent = '';
                    codeElement.appendChild(cursorElement);
                    // Reset scroll to top
                    preElement.scrollTop = 0;
                    typeCode();
                }, config.restartDelay);
                return;
            }

            const currentLine = codeLines[lineIndex];
            
            // Taper caractère par caractère
            if (charIndex < currentLine.length) {
                currentContent += currentLine[charIndex];
                codeElement.textContent = currentContent;
                codeElement.appendChild(cursorElement);
                charIndex++;
                
                // Scroll après chaque caractère
                setTimeout(() => {
                    smartAutoScroll();
                }, 10);
                
                setTimeout(typeCode, config.typingSpeed);
                
            } else {
                // Fin de ligne - passer à la suivante
                currentContent += '\n';
                codeElement.textContent = currentContent;
                codeElement.appendChild(cursorElement);
                lineIndex++;
                charIndex = 0;
                
                // Scroll après chaque ligne
                setTimeout(() => {
                    smartAutoScroll();
                }, 10);
                
                setTimeout(typeCode, config.lineDelay);
            }
        } catch (error) {
            console.error('💥 Erreur dans typeCode:', error);
            // Redémarrer en cas d'erreur
            setTimeout(() => {
                lineIndex = 0;
                charIndex = 0;
                currentContent = '';
                if (codeElement) {
                    codeElement.textContent = '';
                    codeElement.appendChild(cursorElement);
                }
                if (preElement) {
                    preElement.scrollTop = 0;
                }
                typeCode();
            }, 2000);
        }
    }

    // API publique
    return {
        start() {
            console.log(`✅ Démarrage animation pour ${containerId}...`);
            
            // 🔥 FORCER LA HAUTEUR AVANT DE COMMENCER
            setTimeout(() => {
                forceContainerHeight();
                isRunning = true;
                setTimeout(typeCode, 1000);
            }, 100);
        },
        stop() {
            console.log(`⏹️ Arrêt animation pour ${containerId}`);
            isRunning = false;
        },
        restart() {
            console.log(`🔄 Redémarrage animation pour ${containerId}...`);
            this.stop();
            lineIndex = 0;
            charIndex = 0;
            currentContent = '';
            codeElement.textContent = '';
            codeElement.appendChild(cursorElement);
            preElement.scrollTop = 0;
            forceContainerHeight(); // Re-forcer la hauteur
            this.start();
        }
    };
}

// Export pour utilisation dans les autres fichiers
if (typeof window !== 'undefined') {
    window.createAdaptiveTerminalAnimation = createAdaptiveTerminalAnimation;
    console.log('🚀 Terminal animation universelle chargée !');
}

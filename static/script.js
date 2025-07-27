// AI Chatbot JavaScript with Training Features
class AIChatbot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
        this.themeSelector = document.getElementById('themeSelector');
        this.trainingPanel = document.getElementById('trainingPanel');
        
        this.isTyping = false;
        this.messageCount = 0;
        this.lastUserMessage = '';
        this.lastBotResponse = '';
        this.trainingEnabled = false;
        
        this.initializeEventListeners();
        this.initializeThemes();
        this.initializeTraining();
    }
    
    initializeEventListeners() {
        // Send message on Enter key
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character counter
        this.messageInput.addEventListener('input', () => {
            const length = this.messageInput.value.length;
            this.charCount.textContent = length;
            
            // Change color based on character count
            if (length > 450) {
                this.charCount.style.color = '#e74c3c';
            } else if (length > 400) {
                this.charCount.style.color = '#f39c12';
            } else {
                this.charCount.style.color = '#7f8c8d';
            }
        });
        
        // Send button click
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Auto-resize input
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }
    
    initializeThemes() {
        // Load saved theme
        const savedTheme = localStorage.getItem('chatbot-theme') || 'default';
        this.applyTheme(savedTheme);
        
        // Theme selector events
        document.querySelectorAll('.theme-option').forEach(option => {
            option.addEventListener('click', () => {
                const theme = option.dataset.theme;
                this.applyTheme(theme);
                localStorage.setItem('chatbot-theme', theme);
                this.hideThemeSelector();
            });
        });
    }
    
    initializeTraining() {
        // Load training panel elements
        this.trainingStats = {
            conversationCount: document.getElementById('conversationCount'),
            feedbackCount: document.getElementById('feedbackCount'),
            averageRating: document.getElementById('averageRating'),
            mlModelStatus: document.getElementById('mlModelStatus')
        };
        
        // Refresh training stats on initialization
        this.refreshTrainingStats();
    }
    
    async refreshTrainingStats() {
        try {
            const response = await fetch('/training_report');
            if (response.ok) {
                const data = await response.json();
                
                // Access stats from the nested stats object
                const stats = data.stats || {};
                
                if (this.trainingStats.conversationCount) {
                    this.trainingStats.conversationCount.textContent = stats.total_conversations || 0;
                }
                if (this.trainingStats.feedbackCount) {
                    this.trainingStats.feedbackCount.textContent = stats.positive_feedback || 0;
                }
                if (this.trainingStats.averageRating) {
                    this.trainingStats.averageRating.textContent = stats.learning_rate || 'N/A';
                }
                if (this.trainingStats.mlModelStatus) {
                    const isModelTrained = stats.learned_patterns > 0;
                    this.trainingStats.mlModelStatus.textContent = isModelTrained 
                        ? 'Trained ✅' 
                        : 'Not Trained ❌';
                }
                
                this.trainingEnabled = data.available;
            }
        } catch (error) {
            console.warn('Training system not available:', error);
            this.trainingEnabled = false;
        }
    }
    
    applyTheme(themeName) {
        document.body.className = '';
        if (themeName !== 'default') {
            document.body.classList.add(`theme-${themeName}`);
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Store for training
        this.lastUserMessage = message;
        
        // Clear input
        this.messageInput.value = '';
        this.charCount.textContent = '0';
        this.messageInput.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Simulate thinking time for more natural feel
            await this.delay(1000 + Math.random() * 1000);
            
            // Hide typing indicator and show response
            this.hideTypingIndicator();
            this.addMessage(data.response, 'bot', data.timestamp);
            
            // Store for training
            this.lastBotResponse = data.response;
            this.trainingEnabled = data.training_enabled || false;
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage(
                "I'm sorry, I'm having trouble connecting right now. Please try again in a moment! 🔄",
                'bot'
            );
            console.error('Error:', error);
        }
    }
    
    addMessage(content, sender, timestamp = null) {
        this.messageCount++;
        
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `message-wrapper ${sender}-message`;
        
        const currentTime = timestamp || new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const avatarIcon = sender === 'bot' ? 'fas fa-robot' : 'fas fa-user';
        
        messageWrapper.innerHTML = `
            <div class="message-avatar">
                <i class="${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${this.formatMessage(content)}</p>
                    ${sender === 'bot' && this.messageCount <= 2 ? this.generateSuggestions() : ''}
                </div>
                <div class="message-time">${currentTime}</div>
                ${sender === 'bot' && this.trainingEnabled ? this.generateFeedbackButtons() : ''}
            </div>
        `;
        
        this.chatMessages.appendChild(messageWrapper);
        this.scrollToBottom();
        
        // Add entrance animation
        setTimeout(() => {
            messageWrapper.style.opacity = '1';
            messageWrapper.style.transform = 'translateY(0)';
        }, 50);
    }
    
    formatMessage(message) {
        // Simple formatting for better readability
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }
    
    generateFeedbackButtons() {
        return `
            <div class="message-feedback">
                <span>Was this helpful?</span>
                <div class="feedback-buttons">
                    <button class="feedback-btn positive" onclick="chatbot.sendFeedback(5)" title="Great response!">
                        👍
                    </button>
                    <button class="feedback-btn negative" onclick="chatbot.sendFeedback(1)" title="Poor response">
                        👎
                    </button>
                </div>
            </div>
        `;
    }
    
    async sendFeedback(rating) {
        if (!this.trainingEnabled || !this.lastUserMessage || !this.lastBotResponse) {
            return;
        }
        
        try {
            const response = await fetch('/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_input: this.lastUserMessage,
                    bot_response: this.lastBotResponse,
                    rating: rating,
                    feedback: rating >= 4 ? 'Positive feedback' : 'Needs improvement'
                })
            });
            
            const data = await response.json();
            if (data.success) {
                this.showTrainingNotification('Thanks for your feedback! 🎯');
                this.refreshTrainingStats();
            }
        } catch (error) {
            console.error('Error sending feedback:', error);
        }
    }
    
    showTrainingNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'training-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => document.body.removeChild(notification), 300);
        }, 3000);
    }
    
    generateSuggestions() {
        const suggestions = [
            "What's the weather like?",
            "Tell me a fun fact",
            "Help me with programming",
            "What can you do?",
            "Tell me about yourself"
        ];
        
        const randomSuggestions = suggestions
            .sort(() => Math.random() - 0.5)
            .slice(0, 3);
        
        return `
            <div class="message-suggestions">
                ${randomSuggestions.map(suggestion => 
                    `<button class="suggestion-btn" onclick="chatbot.sendSuggestion('${suggestion}')">${suggestion}</button>`
                ).join('')}
            </div>
        `;
    }
    
    sendSuggestion(suggestion) {
        this.messageInput.value = suggestion;
        this.sendMessage();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'block';
        this.sendButton.disabled = true;
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.sendButton.disabled = false;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    showThemeSelector() {
        this.themeSelector.style.display = 'grid';
        setTimeout(() => {
            this.themeSelector.style.opacity = '1';
            this.themeSelector.style.transform = 'translateY(0)';
        }, 10);
    }
    
    hideThemeSelector() {
        this.themeSelector.style.opacity = '0';
        this.themeSelector.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            this.themeSelector.style.display = 'none';
        }, 300);
    }
}

// Global functions
function sendSuggestion(suggestion) {
    if (window.chatbot) {
        window.chatbot.sendSuggestion(suggestion);
    }
}

function sendMessage() {
    if (window.chatbot) {
        window.chatbot.sendMessage();
    }
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        const chatMessages = document.getElementById('chatMessages');
        
        // Keep only the welcome message
        const welcomeMessage = chatMessages.querySelector('.message-wrapper');
        chatMessages.innerHTML = '';
        chatMessages.appendChild(welcomeMessage);
        
        // Reset message counter
        if (window.chatbot) {
            window.chatbot.messageCount = 0;
        }
        
        // Show success feedback
        const clearBtn = document.querySelector('.action-btn');
        clearBtn.classList.add('success-flash');
        setTimeout(() => {
            clearBtn.classList.remove('success-flash');
        }, 300);
    }
}

function toggleTheme() {
    const themeSelector = document.getElementById('themeSelector');
    if (themeSelector.style.display === 'none' || !themeSelector.style.display) {
        window.chatbot.showThemeSelector();
    } else {
        window.chatbot.hideThemeSelector();
    }
}

// Training Panel Functions
function showTrainingPanel() {
    const panel = document.getElementById('trainingPanel');
    panel.style.display = 'block';
    setTimeout(() => panel.classList.add('show'), 10);
    window.chatbot.refreshTrainingStats();
}

function hideTrainingPanel() {
    const panel = document.getElementById('trainingPanel');
    panel.classList.remove('show');
    setTimeout(() => panel.style.display = 'none', 300);
}

async function retrainModel() {
    const button = event.target;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Training...';
    
    try {
        const response = await fetch('/retrain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        if (data.success) {
            window.chatbot.showTrainingNotification('AI model retrained successfully! 🚀');
            window.chatbot.refreshTrainingStats();
        } else {
            window.chatbot.showTrainingNotification('⚠️ ' + data.message);
        }
    } catch (error) {
        window.chatbot.showTrainingNotification('❌ Training failed');
    } finally {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-cog"></i> Retrain AI Model';
    }
}

async function exportTraining() {
    try {
        const response = await fetch('/export_training');
        const data = await response.json();
        
        if (data.success) {
            window.chatbot.showTrainingNotification(`Training data exported to ${data.filename} 💾`);
        } else {
            window.chatbot.showTrainingNotification('❌ Export failed');
        }
    } catch (error) {
        window.chatbot.showTrainingNotification('❌ Export failed');
    }
}

function refreshStats() {
    window.chatbot.refreshTrainingStats();
    window.chatbot.showTrainingNotification('Stats refreshed! 📊');
}

async function teachAI() {
    const input = document.getElementById('teachInput').value.trim();
    const response = document.getElementById('teachResponse').value.trim();
    
    if (!input || !response) {
        window.chatbot.showTrainingNotification('Please fill in both fields ⚠️');
        return;
    }
    
    try {
        // Simulate adding to training data
        const feedbackResponse = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_input: input,
                bot_response: response,
                rating: 5,
                feedback: 'User taught response'
            })
        });
        
        if (feedbackResponse.ok) {
            window.chatbot.showTrainingNotification('AI-BD learned new response! 🎓');
            document.getElementById('teachInput').value = '';
            document.getElementById('teachResponse').value = '';
            window.chatbot.refreshTrainingStats();
        }
    } catch (error) {
        window.chatbot.showTrainingNotification('❌ Teaching failed');
    }
}

// Enhanced features
class EnhancedFeatures {
    constructor() {
        this.initializeAdvancedFeatures();
    }
    
    initializeAdvancedFeatures() {
        // Add keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K to focus input
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('messageInput').focus();
            }
            
            // Escape to hide theme selector
            if (e.key === 'Escape') {
                window.chatbot.hideThemeSelector();
            }
        });
        
        // Add click outside to hide theme selector
        document.addEventListener('click', (e) => {
            const themeSelector = document.getElementById('themeSelector');
            const themeButton = document.querySelector('.action-btn[onclick="toggleTheme()"]');
            
            if (!themeSelector.contains(e.target) && !themeButton.contains(e.target)) {
                window.chatbot.hideThemeSelector();
            }
        });
        
        // Add loading states
        this.addLoadingStates();
        
        // Add sound effects (optional)
        this.initializeSoundEffects();
    }
    
    addLoadingStates() {
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            document.body.classList.add('loading');
            return originalFetch.apply(this, args).finally(() => {
                document.body.classList.remove('loading');
            });
        };
    }
    
    initializeSoundEffects() {
        // Simple sound effects using Web Audio API
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Message sent sound
        this.createSound = (frequency, duration, type = 'sine') => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.value = frequency;
            oscillator.type = type;
            
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration);
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main chatbot
    window.chatbot = new AIChatbot();
    
    // Initialize enhanced features
    window.enhancedFeatures = new EnhancedFeatures();
    
    // Add welcome animation
    setTimeout(() => {
        const header = document.querySelector('.chat-header');
        header.style.transform = 'translateY(0)';
        header.style.opacity = '1';
    }, 100);
    
    // Focus input after load
    setTimeout(() => {
        document.getElementById('messageInput').focus();
    }, 500);
    
    console.log('🤖 AI Chatbot initialized successfully!');
    console.log('💡 Tip: Press Ctrl+K to focus the input field');
});

// Add some fun easter eggs
document.addEventListener('keydown', (e) => {
    // Konami code easter egg
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    if (!window.konamiSequence) window.konamiSequence = [];
    
    window.konamiSequence.push(e.keyCode);
    if (window.konamiSequence.length > konamiCode.length) {
        window.konamiSequence.shift();
    }
    
    if (window.konamiSequence.join(',') === konamiCode.join(',')) {
        // Easter egg activated!
        const particles = document.querySelectorAll('.floating-particle');
        particles.forEach(particle => {
            particle.style.background = '#ff6b6b';
            particle.style.animationDuration = '2s';
        });
        
        setTimeout(() => {
            particles.forEach(particle => {
                particle.style.background = '';
                particle.style.animationDuration = '';
            });
        }, 5000);
        
        window.konamiSequence = [];
    }
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perf = performance.getEntriesByType('navigation')[0];
            console.log(`⚡ Page loaded in ${Math.round(perf.loadEventEnd - perf.loadEventStart)}ms`);
        }, 0);
    });
}

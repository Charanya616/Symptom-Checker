class SymptomCheckerChatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.backendUrl = 'http://127.0.0.1:5000';
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.userInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send symptoms to backend
            const response = await fetch(`${this.backendUrl}/analyze-symptoms`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms: message })
            });
            
            if (!response.ok) {
                throw new Error('Server error');
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            // Add bot response
            this.addBotResponse(data);
            
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            console.error('Error:', error);
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // For user messages, just use text
        if (sender === 'user') {
            contentDiv.textContent = content;
        } else {
            // For bot messages, we'll build the content properly
            contentDiv.innerHTML = content;
        }
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addBotResponse(data) {
        let responseHTML = '';
        
        if (data.error) {
            responseHTML = `<div class="error-message">${data.error}</div>`;
        } else if (data.conditions && data.conditions.length > 0) {
            responseHTML += '<strong>Based on your symptoms, possible conditions include:</strong><br><br>';
            
            data.conditions.forEach(condition => {
                responseHTML += `
                    <div class="condition-item">
                        <div class="condition-name">${this.escapeHtml(condition.name)}</div>
                        <div class="condition-probability">Probability: ${(condition.probability * 100).toFixed(1)}%</div>
                    </div>
                `;
            });
            
            responseHTML += '<br>';
        } else {
            responseHTML = "I couldn't identify any specific conditions based on your symptoms. Please consult with a healthcare professional for accurate diagnosis.";
        }
        
        if (data.next_steps && data.next_steps.length > 0) {
            responseHTML += `
                <div class="next-steps">
                    <h4>💡 Recommended Next Steps:</h4>
                    <ul>
                        ${data.next_steps.map(step => `<li>${this.escapeHtml(step)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        this.addMessage(responseHTML, 'bot');
    }
    
    // Helper function to escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typingIndicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content typing-indicator';
        contentDiv.innerHTML = 'Analyzing symptoms<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>';
        
        typingDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    new SymptomCheckerChatbot();
});
/**
 * Chatbot AI Assistant
 * نظام المحادثة الذكي لمنصة ANDO.5
 */

class ChatbotAI {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.isOpen = false;
        this.messages = [];
        this.isLoading = false;
        this.init();
    }

    init() {
        // إنشاء عناصر الـ Chatbot
        this.createChatbotUI();
        this.attachEventListeners();
        this.loadSuggestions();
    }

    createChatbotUI() {
        // زر الفتح/الإغلاق
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'chatbot-toggle';
        toggleBtn.id = 'chatbotToggle';
        toggleBtn.innerHTML = '💬';
        toggleBtn.title = 'فتح المساعد الذكي';
        document.body.appendChild(toggleBtn);

        // حاوية الـ Chatbot
        const container = document.createElement('div');
        container.className = 'chatbot-container hidden';
        container.id = 'chatbotContainer';
        container.innerHTML = `
            <div class="chatbot-header">
                <span>🤖 مساعد ANDO.5 الذكي</span>
                <button class="chatbot-close" id="chatbotClose" title="إغلاق">✕</button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages"></div>
            <div class="chatbot-suggestions" id="chatbotSuggestions"></div>
            <div class="chatbot-input-area">
                <input 
                    type="text" 
                    class="chatbot-input" 
                    id="chatbotInput" 
                    placeholder="اكتب سؤالك..." 
                    aria-label="حقل الإدخال للمحادثة"
                >
                <button class="chatbot-send" id="chatbotSend" title="إرسال">📤</button>
            </div>
        `;
        document.body.appendChild(container);
    }

    attachEventListeners() {
        const toggle = document.getElementById('chatbotToggle');
        const close = document.getElementById('chatbotClose');
        const send = document.getElementById('chatbotSend');
        const input = document.getElementById('chatbotInput');

        toggle.addEventListener('click', () => this.toggleChatbot());
        close.addEventListener('click', () => this.toggleChatbot());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if(e.key === 'Enter' && !this.isLoading) {
                this.sendMessage();
            }
        });
    }

    toggleChatbot() {
        const container = document.getElementById('chatbotContainer');
        const toggle = document.getElementById('chatbotToggle');
        
        this.isOpen = !this.isOpen;

        if(this.isOpen) {
            container.classList.remove('hidden');
            toggle.classList.add('hidden');
            document.getElementById('chatbotInput').focus();
            
            // رسالة الترحيب
            if(this.messages.length === 0) {
                this.addMessage('السلام عليكم! 👋 أنا مساعدك الذكي في ANDO.5', 'ai', true);
                this.addMessage('يمكنني مساعدتك في اختيار لغة البرمجة المناسبة والإجابة على استفساراتك! 💻', 'ai', true);
            }
        } else {
            container.classList.add('hidden');
            toggle.classList.remove('hidden');
        }
    }

    async sendMessage() {
        if(this.isLoading) return;

        const input = document.getElementById('chatbotInput');
        const message = input.value.trim();

        if(!message) return;

        // إضافة رسالة المستخدم
        this.addMessage(message, 'user');
        input.value = '';

        // عرض مؤشر التحميل
        this.showTypingIndicator();
        this.isLoading = true;

        try {
            // إرسال الرسالة للـ API
            const response = await this.callAPI('/chat', {
                message: message
            });

            // إزالة مؤشر التحميل
            this.removeTypingIndicator();

            if(response.status === 'success') {
                // إضافة الرد الذكي
                this.addMessage(response.message, 'ai', true);

                // إذا كانت هناك بيانات إضافية (معلومات لغة)
                if(response.data) {
                    this.displayLanguageInfo(response.data);
                }

                // إذا كانت هناك اقتراحات
                if(response.suggestions) {
                    this.updateSuggestions(response.suggestions);
                }
            } else {
                this.addMessage('عذراً، حدث خطأ في المعالجة 😞', 'ai', true);
            }
        } catch(error) {
            console.error('Chatbot Error:', error);
            this.removeTypingIndicator();
            this.addMessage('عذراً، لا يمكنني الاتصال بالخادم الآن. حاول لاحقاً 🔌', 'ai', true);
        }

        this.isLoading = false;
    }

    addMessage(text, sender = 'ai', isHTML = false) {
        const messagesContainer = document.getElementById('chatbotMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        if(isHTML) {
            bubble.innerHTML = this.formatMessage(text);
        } else {
            bubble.textContent = text;
        }

        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);

        // التمرير إلى الأسفل
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // حفظ الرسالة
        this.messages.push({ text, sender, timestamp: new Date() });
    }

    formatMessage(text) {
        // تنسيق النص (تحويل الأسطر إلى HTML)
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/__(.*?)__/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbotMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if(indicator) indicator.remove();
    }

    displayLanguageInfo(data) {
        let infoText = `
        <strong>${data.description}</strong><br>
        📌 الاستخدامات: ${data.uses.join(', ')}<br>
        📊 الصعوبة: ${data.difficulty}<br>
        ⭐ الشهرة: ${data.popularity}
        `;
        
        if(data.resources) {
            infoText += '<br><strong>📚 الموارد:</strong><br>';
            data.resources.forEach(r => {
                infoText += `<a href="${r.url}" target="_blank">${r.name}</a><br>`;
            });
        }

        this.addMessage(infoText, 'ai', true);
    }

    async loadSuggestions() {
        try {
            const response = await this.callAPI('/suggestions');
            if(response.status === 'success') {
                this.updateSuggestions(response.suggestions);
            }
        } catch(error) {
            console.error('Error loading suggestions:', error);
        }
    }

    updateSuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('chatbotSuggestions');
        suggestionsContainer.innerHTML = '';

        suggestions.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.className = 'suggestion-btn';
            btn.textContent = suggestion;
            btn.onclick = () => {
                document.getElementById('chatbotInput').value = suggestion;
                this.sendMessage();
            };
            suggestionsContainer.appendChild(btn);
        });
    }

    async callAPI(endpoint, data = null) {
        const options = {
            method: data ? 'POST' : 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if(data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${this.apiUrl}${endpoint}`, options);
        
        if(!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();
    }

    // دالة عامة للحصول على التوصيات
    async getRecommendations(name, language) {
        try {
            const response = await this.callAPI('/recommend', {
                name: name,
                language: language
            });

            if(response.status === 'success') {
                const data = response.data;
                let message = `${data.greeting}\n${data.analysis}\n\n${data.recommendation}`;
                this.addMessage(message, 'ai', true);
            }
        } catch(error) {
            console.error('Error getting recommendations:', error);
        }
    }
}

// تهيئة الـ Chatbot عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // التأكد من أن الخادم متاح (يمكن إضافة محاولات متعددة)
    const chatbot = new ChatbotAI();
    
    // إضافة الـ Chatbot إلى النافذة العامة للوصول إليه من أي مكان
    window.chatbot = chatbot;
});

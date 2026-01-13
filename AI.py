"""
نظام الذكاء الاصطناعي لمنصة ANDO.5
AI System for ANDO.5 Platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

app = Flask(__name__)
CORS(app)

# قاعدة بيانات المعارف والردود الذكية
KNOWLEDGE_BASE = {
    "python": {
        "description": "لغة برمجة قوية وسهلة التعلم",
        "uses": ["تحليل البيانات", "الذكاء الاصطناعي", "تطوير الويب", "أتمتة المهام"],
        "resources": [
            {"name": "Python.org", "url": "https://python.org"},
            {"name": "Real Python", "url": "https://realpython.com"}
        ],
        "difficulty": "سهلة",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "javascript": {
        "description": "لغة الويب الأساسية",
        "uses": ["تطوير الواجهات الأمامية", "تطوير الخوادم", "تطبيقات الويب", "ألعاب الويب"],
        "resources": [
            {"name": "MDN Web Docs", "url": "https://mdn.org"},
            {"name": "JavaScript.info", "url": "https://javascript.info"}
        ],
        "difficulty": "متوسطة",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "cpp": {
        "description": "لغة برمجة عالية الأداء",
        "uses": ["تطوير الألعاب", "البرامج النظام", "التطبيقات عالية الأداء", "الروبوتات"],
        "resources": [
            {"name": "cplusplus.com", "url": "https://cplusplus.com"},
            {"name": "C++ Reference", "url": "https://en.cppreference.com"}
        ],
        "difficulty": "صعبة",
        "popularity": "⭐⭐⭐⭐"
    }
}

# نماذج الأسئلة الشائعة والإجابات
INTENTS = {
    "greeting": {
        "patterns": ["السلام عليكم", "صباح", "مساء", "أهلا", "hello", "hi"],
        "responses": [
            "وعليكم السلام! 👋 كيف يمكنني مساعدتك؟",
            "مرحباً بك! 😊 هل تريد معلومات عن لغات البرمجة؟",
            "أهلاً وسهلاً! 🎉 ما الذي تريد تعلمه؟"
        ]
    },
    "help": {
        "patterns": ["مساعدة", "ساعد", "احتاج", "help", "assist"],
        "responses": [
            "يمكنني مساعدتك في اختيار لغة برمجة مناسبة وتقديم موارد تعليمية! 📚",
            "أنا هنا لتقديم المشورة حول البرمجة والبدء في التعلم! 💻"
        ]
    },
    "language_info": {
        "patterns": ["ما هي", "معلومات", "أخبر", "حدث", "info"],
        "responses": [
            "اختر لغة من القائمة لمعرفة المزيد عنها! 🔍"
        ]
    },
    "recommendation": {
        "patterns": ["ايهما أفضل", "أيهما", "أنسب", "recommend", "أنصح"],
        "responses": [
            "يعتمد على هدفك! Python رائعة للمبتدئين، JavaScript للويب، C++ للأداء العالية 🎯"
        ]
    }
}

class AIAssistant:
    """مساعد ذكي للإجابة على الأسئلة"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
    
    def clean_text(self, text: str) -> str:
        """تنظيف النص من الرموز الخاصة"""
        text = text.strip().lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def extract_language(self, text: str) -> str:
        """استخراج اسم اللغة من النص"""
        text_lower = text.lower()
        for lang in KNOWLEDGE_BASE.keys():
            if lang in text_lower:
                return lang
        return None
    
    def calculate_similarity(self, text: str, pattern: str) -> float:
        """حساب درجة التشابه بين نصين (Similarity Score)"""
        text_words = set(self.clean_text(text).split())
        pattern_words = set(self.clean_text(pattern).split())
        
        if not pattern_words:
            return 0
        
        intersection = len(text_words.intersection(pattern_words))
        similarity = intersection / len(pattern_words)
        return similarity
    
    def find_best_intent(self, user_input: str) -> Tuple[str, float]:
        """البحث عن أفضل نية (Intent) تطابق مدخل المستخدم"""
        best_intent = None
        best_score = 0
        
        for intent, data in INTENTS.items():
            for pattern in data["patterns"]:
                score = self.calculate_similarity(user_input, pattern)
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        return best_intent, best_score
    
    def get_response(self, user_input: str) -> Dict:
        """الحصول على الرد الذكي للمستخدم"""
        intent, confidence = self.find_best_intent(user_input)
        
        response = {
            "status": "success",
            "confidence": confidence,
            "intent": intent
        }
        
        # التحقق من وجود لغة مذكورة
        language = self.extract_language(user_input)
        
        if language and confidence > 0.3:
            response["message"] = self.get_language_info(language)
            response["data"] = KNOWLEDGE_BASE[language]
        elif intent and confidence > 0.3:
            import random
            response["message"] = random.choice(INTENTS[intent]["responses"])
        else:
            response["message"] = "عذراً، لم أفهم سؤالك. جرب السؤال بطريقة أخرى! 🤔"
            response["suggestions"] = [
                "اسأل عن Python",
                "اسأل عن JavaScript",
                "اسأل عن C++",
                "طلب توصية"
            ]
        
        # حفظ في السجل
        self.conversation_history.append({
            "user": user_input,
            "assistant": response["message"],
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_language_info(self, language: str) -> str:
        """الحصول على معلومات عن اللغة"""
        if language in KNOWLEDGE_BASE:
            info = KNOWLEDGE_BASE[language]
            msg = f"🔹 **{language.upper()}**\n"
            msg += f"{info['description']}\n"
            msg += f"الصعوبة: {info['difficulty']}\n"
            msg += f"الشهرة: {info['popularity']}"
            return msg
        return "لم أجد معلومات عن هذه اللغة!"
    
    def get_recommendations(self, preferences: Dict) -> Dict:
        """توصيات ذكية بناءً على التفضيلات"""
        name = preferences.get("name", "الصديق")
        language = preferences.get("language", "")
        
        recommendation = {
            "greeting": f"مرحباً {name}! 👋",
            "analysis": "تحليل تفضيلاتك الشخصية... 🔍",
            "recommendation": ""
        }
        
        if language and language in KNOWLEDGE_BASE:
            lang_data = KNOWLEDGE_BASE[language]
            recommendation["recommendation"] = f"""
            اخترت {language} - اختيار رائع! 🎯
            
            {lang_data['description']}
            
            استخدامات: {', '.join(lang_data['uses'])}
            
            مستوى الصعوبة: {lang_data['difficulty']}
            
            الموارد الموصى بها:
            """ + "\n            ".join([f"- {r['name']}" for r in lang_data['resources']])
        else:
            recommendation["recommendation"] = """
            لم تختر لغة محددة حتى الآن! 
            كل اللغات مهمة وقيمة حسب الهدف:
            - Python: الأفضل للمبتدئين والعلوم
            - JavaScript: أساسي للويب
            - C++: للأداء العالية والنظم
            """
        
        return recommendation

# إنشاء instance من المساعد
ai_assistant = AIAssistant()

# ======================== API Routes ========================

@app.route('/api/health', methods=['GET'])
def health():
    """فحص صحة الخادم"""
    return jsonify({
        "status": "online",
        "message": "AI Server is running",
        "version": "1.0"
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """معالجة رسالة المحادثة"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "status": "error",
                "message": "الرسالة فارغة!"
            }), 400
        
        response = ai_assistant.get_response(user_message)
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"خطأ في المعالجة: {str(e)}"
        }), 500

@app.route('/api/language-info', methods=['POST'])
def language_info():
    """الحصول على معلومات عن لغة برمجة"""
    try:
        data = request.json
        language = data.get('language', '').lower()
        
        if language not in KNOWLEDGE_BASE:
            return jsonify({
                "status": "error",
                "message": "لغة غير موجودة!"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": KNOWLEDGE_BASE[language]
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """الحصول على توصيات ذكية"""
    try:
        data = request.json
        preferences = {
            "name": data.get('name', 'الصديق'),
            "language": data.get('language', '').lower()
        }
        
        recommendation = ai_assistant.get_recommendations(preferences)
        return jsonify({
            "status": "success",
            "data": recommendation
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    """الحصول على اقتراحات الأسئلة"""
    suggestions = [
        "ما هي Python؟",
        "ايهما أفضل Python أم JavaScript؟",
        "كيف أبدأ مع البرمجة؟",
        "معلومات عن C++",
        "ما أفضل لغة للمبتدئين؟"
    ]
    return jsonify({
        "status": "success",
        "suggestions": suggestions
    }), 200

@app.route('/api/history', methods=['GET'])
def history():
    """الحصول على سجل المحادثة"""
    return jsonify({
        "status": "success",
        "history": ai_assistant.conversation_history[-10:]  # آخر 10 رسائل
    }), 200

@app.errorhandler(404)
def not_found(error):
    """معالجة الطلبات غير الموجودة"""
    return jsonify({
        "status": "error",
        "message": "الموارد المطلوبة غير موجودة"
    }), 404

@app.errorhandler(500)
def server_error(error):
    """معالجة أخطاء الخادم"""
    return jsonify({
        "status": "error",
        "message": "خطأ في الخادم"
    }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 ANDO.5 AI Assistant Server")
    print("=" * 50)
    print("🚀 Server starting on http://localhost:5000")
    print("📚 Knowledge Base Loaded with 3 Programming Languages")
    print("=" * 50)
    
    # تشغيل الخادم
    app.run(debug=True, port=5000, host='0.0.0.0')

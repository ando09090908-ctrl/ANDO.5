"""
ملف الإعدادات للخادم الذكي
Configuration file for ANDO.5 AI Server
"""

# ===== Flask Settings =====
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
SECRET_KEY = 'your-secret-key-here'

# ===== CORS Settings =====
CORS_ORIGINS = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:5500',
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    '*'  # للتطوير فقط - استخدم origins محددة في الإنتاج
]

# ===== API Settings =====
API_VERSION = '1.0'
MAX_REQUEST_SIZE = 1024  # بالبايت
MAX_CONVERSATION_HISTORY = 50  # عدد الرسائل المحفوظة

# ===== Language Support =====
SUPPORTED_LANGUAGES = ['python', 'javascript', 'cpp']
DEFAULT_LANGUAGE = 'python'

# ===== AI Settings =====
MIN_CONFIDENCE_THRESHOLD = 0.3  # الحد الأدنى لثقة الإجابة
MAX_RESPONSE_LENGTH = 1000  # الحد الأقصى لطول الرسالة

# ===== Security Settings =====
ENABLE_RATE_LIMITING = False  # تفعيل تحديد السرعة
RATE_LIMIT_REQUESTS = 100  # عدد الطلبات
RATE_LIMIT_PERIOD = 60  # بالثواني

# ===== Logging Settings =====
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = 'ando5_ai.log'
ENABLE_LOGGING = True

# ===== Knowledge Base =====
KNOWLEDGE_BASE_FILE = 'knowledge.json'  # يمكن حفظ القاعدة في ملف

# ===== Production Settings =====
PRODUCTION = False  # غيّر إلى True في الإنتاج

# ===== عند التغيير إلى الإنتاج =====
if PRODUCTION:
    DEBUG = False
    CORS_ORIGINS = ['your-domain.com']  # استخدم نطاق واحد فقط
    ENABLE_RATE_LIMITING = True
    LOG_LEVEL = 'WARNING'

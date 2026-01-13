"""
ملف اختبار الـ API
API Testing Script for ANDO.5
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health():
    """اختبار صحة الخادم"""
    print("=" * 50)
    print("✅ اختبار: فحص الصحة (Health Check)")
    print("=" * 50)
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ خطأ: {e}")
    print()

def test_chat():
    """اختبار المحادثة"""
    print("=" * 50)
    print("✅ اختبار: المحادثة الذكية (Chat)")
    print("=" * 50)
    
    test_messages = [
        "السلام عليكم",
        "ما هي Python؟",
        "ايهما أفضل JavaScript أم Python؟"
    ]
    
    for message in test_messages:
        print(f"\n📝 الرسالة: {message}")
        try:
            response = requests.post(
                f'{BASE_URL}/chat',
                json={'message': message}
            )
            data = response.json()
            print(f"💬 الرد: {data.get('message')}")
            print(f"🎯 النية: {data.get('intent')}")
            print(f"📊 الثقة: {data.get('confidence', 0):.2%}")
        except Exception as e:
            print(f"❌ خطأ: {e}")

def test_language_info():
    """اختبار معلومات اللغة"""
    print("\n" + "=" * 50)
    print("✅ اختبار: معلومات اللغة (Language Info)")
    print("=" * 50)
    
    languages = ['python', 'javascript', 'cpp']
    
    for lang in languages:
        print(f"\n🔹 اللغة: {lang.upper()}")
        try:
            response = requests.post(
                f'{BASE_URL}/language-info',
                json={'language': lang}
            )
            data = response.json()
            if data.get('status') == 'success':
                lang_data = data.get('data', {})
                print(f"الوصف: {lang_data.get('description')}")
                print(f"الصعوبة: {lang_data.get('difficulty')}")
                print(f"الشهرة: {lang_data.get('popularity')}")
            else:
                print(f"❌ خطأ: {data.get('message')}")
        except Exception as e:
            print(f"❌ خطأ: {e}")

def test_recommendations():
    """اختبار التوصيات"""
    print("\n" + "=" * 50)
    print("✅ اختبار: التوصيات الذكية (Recommendations)")
    print("=" * 50)
    
    preferences = [
        {'name': 'أحمد', 'language': 'python'},
        {'name': 'فاطمة', 'language': 'javascript'},
        {'name': 'محمد', 'language': 'cpp'}
    ]
    
    for pref in preferences:
        print(f"\n👤 المستخدم: {pref['name']} | اللغة: {pref['language']}")
        try:
            response = requests.post(
                f'{BASE_URL}/recommend',
                json=pref
            )
            data = response.json()
            if data.get('status') == 'success':
                rec_data = data.get('data', {})
                print(f"التحية: {rec_data.get('greeting')}")
                print(f"التوصية: {rec_data.get('recommendation')[:100]}...")
            else:
                print(f"❌ خطأ: {data.get('message')}")
        except Exception as e:
            print(f"❌ خطأ: {e}")

def test_suggestions():
    """اختبار الاقتراحات"""
    print("\n" + "=" * 50)
    print("✅ اختبار: الاقتراحات (Suggestions)")
    print("=" * 50)
    try:
        response = requests.get(f'{BASE_URL}/suggestions')
        data = response.json()
        suggestions = data.get('suggestions', [])
        print(f"\n📋 الاقتراحات المتاحة:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def test_history():
    """اختبار السجل"""
    print("\n" + "=" * 50)
    print("✅ اختبار: سجل المحادثات (History)")
    print("=" * 50)
    try:
        response = requests.get(f'{BASE_URL}/history')
        data = response.json()
        history = data.get('history', [])
        print(f"\n📜 آخر {len(history)} رسالة:")
        for i, chat in enumerate(history[-3:], 1):
            print(f"\n  {i}. المستخدم: {chat.get('user')}")
            print(f"     الرد: {chat.get('assistant')[:50]}...")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("\n\n")
    print("🤖 " * 15)
    print("بدء اختبار API - ANDO.5 AI Server")
    print("🤖 " * 15)
    print("\n")
    
    try:
        test_health()
        test_chat()
        test_language_info()
        test_suggestions()
        test_recommendations()
        test_history()
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار العام: {e}")
        print("\n⚠️ تأكد من:")
        print("  1. الخادم يعمل: python AI.py")
        print("  2. المكتبات مثبتة: pip install -r requirements.txt")
        print("  3. البورت 5000 متاح")
    
    print("\n\n")
    print("✅ " * 15)
    print("انتهى الاختبار")
    print("✅ " * 15)

if __name__ == '__main__':
    run_all_tests()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشغل سريع لـ ANDO.5 AI
ANDO.5 AI Quick Launcher

استخدم هذا الملف لتشغيل الخادم والاختبارات بسهولة
"""

import os
import sys
import subprocess
import platform
import time

class Colors:
    """ألوان Terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """طباعة رأس البرنامج"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("=" * 60)
    print("🤖 ANDO.5 AI Learning Platform - Quick Launcher")
    print("منصة ANDO.5 التعليمية الذكية - مشغل سريع")
    print("=" * 60)
    print(f"{Colors.ENDC}\n")

def print_menu():
    """طباعة القائمة الرئيسية"""
    print(f"{Colors.BOLD}{Colors.YELLOW}🎯 اختر من الخيارات التالية:{Colors.ENDC}\n")
    print(f"  {Colors.GREEN}1{Colors.ENDC} - تشغيل الخادم (Run Server)")
    print(f"  {Colors.GREEN}2{Colors.ENDC} - اختبار الـ API (Test API)")
    print(f"  {Colors.GREEN}3{Colors.ENDC} - تثبيت المكتبات (Install Requirements)")
    print(f"  {Colors.GREEN}4{Colors.ENDC} - فتح المتصفح (Open Browser)")
    print(f"  {Colors.GREEN}5{Colors.ENDC} - عرض المعلومات (Show Info)")
    print(f"  {Colors.GREEN}0{Colors.ENDC} - خروج (Exit)\n")

def run_server():
    """تشغيل الخادم"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🚀 تشغيل الخادم...{Colors.ENDC}\n")
    try:
        subprocess.run([sys.executable, 'AI.py'])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⏸️ تم إيقاف الخادم{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ خطأ: {e}{Colors.ENDC}")

def test_api():
    """اختبار الـ API"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🧪 اختبار الـ API...{Colors.ENDC}\n")
    try:
        subprocess.run([sys.executable, 'test_api.py'])
    except Exception as e:
        print(f"{Colors.RED}❌ خطأ: {e}{Colors.ENDC}")

def install_requirements():
    """تثبيت المكتبات"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}📦 تثبيت المكتبات...{Colors.ENDC}\n")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print(f"\n{Colors.GREEN}✅ تم التثبيت بنجاح!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ خطأ: {e}{Colors.ENDC}")

def open_browser():
    """فتح المتصفح"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🌐 فتح المتصفح...{Colors.ENDC}\n")
    try:
        import webbrowser
        
        # محاولة فتح الملف المحلي
        file_path = os.path.abspath('index.html')
        file_url = f'file:///{file_path}' if platform.system() == 'Windows' else f'file://{file_path}'
        
        print(f"{Colors.CYAN}📄 فتح: {file_url}{Colors.ENDC}")
        webbrowser.open(file_url)
        
        print(f"{Colors.GREEN}✅ تم فتح المتصفح{Colors.ENDC}")
        print(f"{Colors.YELLOW}💡 تأكد من تشغيل الخادم: python AI.py{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}❌ خطأ: {e}{Colors.ENDC}")

def show_info():
    """عرض معلومات النظام"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}ℹ️ معلومات النظام{Colors.ENDC}\n")
    
    # معلومات Python
    print(f"{Colors.GREEN}Python:{Colors.ENDC}")
    print(f"  الإصدار: {sys.version.split()[0]}")
    print(f"  المسار: {sys.executable}\n")
    
    # معلومات النظام
    print(f"{Colors.GREEN}النظام:{Colors.ENDC}")
    print(f"  النوع: {platform.system()}")
    print(f"  الإصدار: {platform.release()}\n")
    
    # معلومات المشروع
    print(f"{Colors.GREEN}المشروع:{Colors.ENDC}")
    print(f"  الاسم: ANDO.5 AI Learning Platform")
    print(f"  الإصدار: 1.2 (beta) + AI")
    print(f"  الحالة: ✅ جاهز للاستخدام\n")
    
    # ملفات المشروع
    files = [
        'AI.py', 'chatbot.js', 'chatbot.css', 
        'script.js', 'style.css', 'index.html'
    ]
    
    print(f"{Colors.GREEN}الملفات الرئيسية:{Colors.ENDC}")
    for file in files:
        exists = "✅" if os.path.exists(file) else "❌"
        print(f"  {exists} {file}")
    
    print()

def main():
    """البرنامج الرئيسي"""
    while True:
        print_header()
        print_menu()
        
        choice = input(f"{Colors.BOLD}{Colors.YELLOW}اختر (0-5): {Colors.ENDC}").strip()
        
        if choice == '1':
            run_server()
        elif choice == '2':
            test_api()
        elif choice == '3':
            install_requirements()
        elif choice == '4':
            open_browser()
        elif choice == '5':
            show_info()
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 وداعاً!{Colors.ENDC}\n")
            break
        else:
            print(f"\n{Colors.RED}❌ خيار غير صحيح!{Colors.ENDC}")
        
        input(f"\n{Colors.YELLOW}اضغط Enter للمتابعة...{Colors.ENDC}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏸️ تم الإيقاف من قبل المستخدم{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطأ غير متوقع: {e}{Colors.ENDC}\n")

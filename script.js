// تحسينات الأمان والأداء
document.addEventListener('DOMContentLoaded', function() {
    const myForm = document.getElementById('myForm');
    const nameInput = document.getElementById('name');
    const languageSelect = document.getElementById('language');
    const submitBtn = document.getElementById('submitBtn');
    const nameError = document.getElementById('nameError');

    // دالة التحقق من صحة الإدخال (Input Validation)
    function validateName(name) {
        // التحقق من أن الاسم لا يحتوي على رموز ضارة
        const cleanName = name.trim();
        
        // منع XSS: عدم السماح برموز خاصة
        if(!/^[\u0600-\u06FF\s\-'a-zA-Z]+$/.test(cleanName)) {
            return {
                valid: false,
                message: 'الاسم يحتوي على أحرف غير مسموحة'
            };
        }
        
        if(cleanName.length < 2) {
            return {
                valid: false,
                message: 'الاسم يجب أن يكون أكثر من حرف واحد'
            };
        }
        
        if(cleanName.length > 50) {
            return {
                valid: false,
                message: 'الاسم طويل جداً (أقصى 50 حرف)'
            };
        }
        
        return { valid: true };
    }

    // دالة لإنشاء إشعار آمن بدلاً من alert
    function showNotification(message, type = 'success') {
        // منع XSS: استخدام textContent بدلاً من innerHTML
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // إزالة الإشعار بعد 3 ثواني
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // التعامل مع إرسال النموذج
    myForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // تعطيل الزر أثناء المعالجة (منع التكرار)
        submitBtn.disabled = true;
        submitBtn.textContent = 'جاري الإرسال...';
        
        const nameValue = nameInput.value;
        
        // التحقق من صحة الإدخال
        const validation = validateName(nameValue);
        
        if(!validation.valid) {
            nameError.textContent = validation.message;
            nameError.style.color = '#ef4444';
            showNotification(validation.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'إرسال';
            return;
        }
        
        // مسح رسالة الخطأ
        nameError.textContent = '';
        
        // تنظيف الإدخال (Sanitization)
        const cleanedName = nameValue.trim().replace(/[<>]/g, '');
        
        // محاكاة إرسال البيانات
        setTimeout(() => {
            showNotification(`تم تسجيل البيانات بنجاح(محاكاة) اهلا بك يا ${cleanedName}`, 'success');
            
            // تنظيف النموذج
            myForm.reset();
            nameError.textContent = '';
            
            // إعادة تفعيل الزر
            submitBtn.disabled = false;
            submitBtn.textContent = 'إرسال';
        }, 500);
    });

    // التحقق الفوري من الإدخال (Real-time Validation)
    nameInput.addEventListener('blur', function() {
        const validation = validateName(this.value);
        if(!validation.valid && this.value.length > 0) {
            nameError.textContent = validation.message;
            nameError.style.color = '#ef4444';
        } else {
            nameError.textContent = '';
        }
    });

    // تنظيف رسالة الخطأ عند البدء في الكتابة
    nameInput.addEventListener('input', function() {
        if(nameError.textContent) {
            nameError.textContent = '';
        }
    });

    // منع إعادة تحميل الصفحة عند الضغط على Enter في حقل آخر
    nameInput.addEventListener('keydown', function(e) {
        if(e.key === 'Enter') {
            e.preventDefault();
            myForm.dispatchEvent(new Event('submit'));
        }
    });

    // حماية ضد CSRF: إضافة token (في تطبيق حقيقي)
    // يمكن إضافة CSRF token هنا قبل إرسال البيانات للخادم

});

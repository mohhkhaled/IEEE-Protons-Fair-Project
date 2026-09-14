# School Website Backend (Phase 2) — Flask + MySQL

## هيكل المشروع
```
school_backend_mysql/
├── app.py            # نقطة تشغيل السيرفر
├── db.py             # الاتصال بـ MySQL
├── students.py        # كل الـ routes بتاعة الطلاب
├── teachers.py        # كل الـ routes بتاعة المدرسين
├── schema.sql         # سكريبت إنشاء الداتابيز والجداول
└── requirements.txt
```

## خطوات التشغيل

### 1) جهّز الداتابيز
افتح MySQL (Workbench أو terminal) وشغّل ملف `schema.sql` مرة واحدة:
```bash
mysql -u root -p < schema.sql
```
ده هيعمل الداتابيز `school_db` وجدولين: `students` و `teachers`.

### 2) عدّل بيانات الاتصال
افتح `db.py` وغيّر الـ `user` و `password` على حسب إعدادات MySQL عندك.

### 3) نزّل المكتبات
```bash
pip install -r requirements.txt
```

### 4) شغّل السيرفر
```bash
python app.py
```
السيرفر هيشتغل على: `http://127.0.0.1:5000`

## الـ Endpoints المتاحة

### Students
| Method | Endpoint | الوظيفة |
|--------|----------|---------|
| POST   | `/students/` | إضافة طالب جديد |
| GET    | `/students/` | عرض كل الطلاب |
| GET    | `/students/<id>` | عرض طالب معين |
| PUT    | `/students/<id>` | تعديل بيانات طالب |
| DELETE | `/students/<id>` | حذف طالب |

### Teachers
| Method | Endpoint | الوظيفة |
|--------|----------|---------|
| POST   | `/teachers/` | إضافة مدرس جديد |
| GET    | `/teachers/` | عرض كل المدرسين |
| GET    | `/teachers/<id>` | عرض مدرس معين |
| PUT    | `/teachers/<id>` | تعديل بيانات مدرس |
| DELETE | `/teachers/<id>` | حذف مدرس |

## تجربة مع Postman / curl

### إضافة طالب
```bash
curl -X POST http://127.0.0.1:5000/students/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Ahmed Ali", "email": "ahmed@school.com", "grade": "Grade 10", "phone": "01012345678"}'
```

### إضافة مدرس
```bash
curl -X POST http://127.0.0.1:5000/teachers/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Mona Hassan", "email": "mona@school.com", "department": "Math Department"}'
```

## ملاحظات
- الكود بيستخدم raw SQL queries مباشرة (parameterized queries عشان نتفادى SQL Injection) بدل ORM، بما إنكم طلبتوا Python API عادي.
- لما تجهزوا الـ Frontend في Phase 3، الـ API دي جاهزة تتستهلك مباشرة بـ fetch/axios.
- لو حبيتوا Authentication (تسجيل دخول بكلمة سر مشفّرة) أو ربط الطلاب بالمدرسين (جدول Enrollments مثلاً) قولّي وهضيفه.

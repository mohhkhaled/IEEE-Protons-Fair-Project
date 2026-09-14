import mysql.connector
from mysql.connector import Error


# غيّر البيانات دي على حسب إعدادات MySQL عندك
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "school_db",
}


def get_connection():
    """
    بتفتح اتصال جديد بالداتابيز.
    بنستخدم dictionary=True عشان النتائج ترجع كـ dict مباشرة (اسم العمود: القيمة)
    بدل ما ترجع tuples.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        raise

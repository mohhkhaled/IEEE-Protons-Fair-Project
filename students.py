from flask import Blueprint, request, jsonify
from db import get_connection
from mysql.connector import Error

students_bp = Blueprint("students", __name__, url_prefix="/students")


# ---------- إضافة طالب جديد ----------
@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json()

    required_fields = ["full_name", "email", "grade"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO students (full_name, email, grade, phone) VALUES (%s, %s, %s, %s)",
            (data["full_name"], data["email"], data["grade"], data.get("phone")),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "message": "Student created successfully"}), 201
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# ---------- عرض كل الطلاب ----------
@students_bp.route("/", methods=["GET"])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return jsonify(students), 200
    finally:
        cursor.close()
        conn.close()


# ---------- عرض طالب واحد ----------
@students_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student), 200
    finally:
        cursor.close()
        conn.close()


# ---------- تعديل بيانات طالب ----------
@students_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    allowed_fields = ["full_name", "email", "grade", "phone"]
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values()) + [student_id]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"UPDATE students SET {set_clause} WHERE id = %s", values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student updated successfully"}), 200
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# ---------- حذف طالب ----------
@students_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student deleted successfully"}), 200
    finally:
        cursor.close()
        conn.close()

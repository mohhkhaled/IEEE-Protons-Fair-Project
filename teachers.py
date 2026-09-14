from flask import Blueprint, request, jsonify
from db import get_connection
from mysql.connector import Error

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


# ---------- إضافة مدرس جديد ----------
@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    data = request.get_json()

    required_fields = ["full_name", "email"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO teachers (full_name, email, phone, department) VALUES (%s, %s, %s, %s)",
            (data["full_name"], data["email"], data.get("phone"), data.get("department")),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "message": "Teacher created successfully"}), 201
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# ---------- عرض كل المدرسين ----------
@teachers_bp.route("/", methods=["GET"])
def get_teachers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM teachers")
        teachers = cursor.fetchall()
        return jsonify(teachers), 200
    finally:
        cursor.close()
        conn.close()


# ---------- عرض مدرس واحد ----------
@teachers_bp.route("/<int:teacher_id>", methods=["GET"])
def get_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        teacher = cursor.fetchone()
        if not teacher:
            return jsonify({"error": "Teacher not found"}), 404
        return jsonify(teacher), 200
    finally:
        cursor.close()
        conn.close()


# ---------- تعديل بيانات مدرس ----------
@teachers_bp.route("/<int:teacher_id>", methods=["PUT"])
def update_teacher(teacher_id):
    data = request.get_json()

    allowed_fields = ["full_name", "email", "phone", "department"]
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values()) + [teacher_id]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"UPDATE teachers SET {set_clause} WHERE id = %s", values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Teacher not found"}), 404
        return jsonify({"message": "Teacher updated successfully"}), 200
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# ---------- حذف مدرس ----------
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Teacher not found"}), 404
        return jsonify({"message": "Teacher deleted successfully"}), 200
    finally:
        cursor.close()
        conn.close()

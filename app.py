from flask import Flask, jsonify
from students import students_bp
from teachers import teachers_bp

app = Flask(__name__)

app.register_blueprint(students_bp)
app.register_blueprint(teachers_bp)


@app.route("/")
def root():
    return jsonify({"message": "School Website API is running 🚀"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

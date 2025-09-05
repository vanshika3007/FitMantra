
from flask import Blueprint, request, jsonify
from chatbot import get_bot_response
from fitness_logic import get_fitness_plan
import sqlite3, os

main_routes = Blueprint("main_routes", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

@main_routes.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "FitMantra API"})

@main_routes.route("/chatbot", methods=["POST"])
def chatbot_response():
    payload = request.get_json(silent=True) or {}
    user_input = (payload.get("message") or "").strip()
    if not user_input:
        return jsonify({"response": "Please type a message."}), 400
    bot_reply = get_bot_response(user_input)
    return jsonify({"response": bot_reply})

@main_routes.route("/fitness-plan", methods=["GET"])
def fitness_plan():
    try:
        plan = get_fitness_plan()
        return jsonify(plan)
    except FileNotFoundError:
        return jsonify({"error": "Weekly_Workouts.csv not found."}), 404

@main_routes.route("/progress", methods=["POST"])
def save_progress():
    data = request.get_json(silent=True) or {}
    user = data.get("user")
    workout = data.get("workout")
    date = data.get("date")
    if not all([user, workout, date]):
        return jsonify({"error": "user, workout, date are required"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO progress (user, workout, date) VALUES (?, ?, ?)",
                   (user, workout, date))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@main_routes.route("/get-progress", methods=["GET"])
def get_progress():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user, workout, date FROM progress ORDER BY date DESC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    progress = [{"user": r[0], "workout": r[1], "date": r[2]} for r in rows]
    return jsonify(progress)

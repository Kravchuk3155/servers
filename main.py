from flask import Flask, request, jsonify
import jwt
import datetime
import time
from models import init_db, seed_exercises, add_user, get_user, get_exercises_by_level, get_motivational_message

app = Flask(__name__)

SECRET_KEY = "your_secret_key"


def create_token(user_id, username, level):
    payload = {
        "sub": user_id,
        "username": username,
        "level": level,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Токен закінчився"}
    except jwt.InvalidTokenError:
        return {"error": "Невірний токен"}


@app.route('/')
def index():
    return "Ласкаво просимо до Fitness App!"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    level = data.get('level')

    if not username or not password or not level:
        return jsonify({"error": "Всі поля обов'язкові"}), 400

    result = add_user(username, password, level)
    if result:
        return jsonify({"message": "Користувача зареєстровано"}), 201
    else:
        return jsonify({"error": "Користувач з таким іменем вже існує"}), 409


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user(username, password)
    if user:
        token = create_token(user[0], user[1], user[3])
        return jsonify({"message": "Вхід успішний", "token": token})
    else:
        return jsonify({"error": "Неправильний логін або пароль"}), 401


@app.route('/exercises/<level>', methods=['GET'])
def exercises_level(level):
    exercises = get_exercises_by_level(level)

    if exercises:
        return jsonify({"exercises": exercises})
    else:
        return jsonify({"error": "Немає вправ для цього рівня"}), 404


@app.route('/start-workout', methods=['POST'])
def start_workout():
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({"error": "Токен не знайдено"}), 400

        user_data = verify_token(token)
        if "error" in user_data:
            return jsonify(user_data), 401

        user_level = user_data.get("level")
        exercises = get_exercises_by_level(user_level)
        if not exercises:
            return jsonify({"error": "Немає вправ для вашого рівня."}), 400

        workout_details = []

        for exercise in exercises:
            workout_details.append(f"Починаємо вправу: {exercise['name']}")

            time.sleep(exercise['duration'])
            workout_details.append(f"Вправа {exercise['name']} завершена.")
            workout_details.append("15 секунд відпочинку.")
            time.sleep(15)

        motivational_message = get_motivational_message()
        workout_details.append(f"Мотиваційне повідомлення: {motivational_message}")

        return jsonify({"workout_details": workout_details})

    except Exception as e:
        print(f"Помилка: {str(e)}")
        return jsonify({"error": "Сталася помилка на сервері"}), 500


if __name__ == '__main__':
    init_db()
    seed_exercises()
    app.run(debug=True)
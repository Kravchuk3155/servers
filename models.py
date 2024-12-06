import sqlite3
import random


DB_NAME = "fitness_app.db"

motivational_messages = [
    "Відмінно! Продовжуй у тому ж дусі, ти на правильному шляху!",
    "Чудово виконано! Ти на крок ближче до своєї мети!",
    "Ти молодець! Кожен крок наближає тебе до успіху!",
    "Браво! Ти виконав вправу, залишайся таким же сильним!",
    "Прекрасно! Ти зробив великий крок до досягнення своїх цілей!",
    "Не зупиняйся! Ти стаєш сильнішим з кожною вправою!"
]


def get_motivational_message():
    return random.choice(motivational_messages)


def test_db_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        print("Підключення успішне!")
        conn.close()
    except sqlite3.Error as e:
        print(f"Помилка підключення до бази даних: {e}")


test_db_connection()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, level TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS exercises
                 (id INTEGER PRIMARY KEY, name TEXT, level TEXT, duration INTEGER)''')
    conn.commit()
    conn.close()


def add_user(username, password, level):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        return False
    c.execute("INSERT INTO users (username, password, level) VALUES (?, ?, ?)", (username, password, level))
    conn.commit()
    conn.close()
    return True


def get_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user


def seed_exercises():
    exercises = [
        ("Присідання", "Виконайте 10 присідань", 30, "початківець"),
        ("Віджимання", "Виконайте 10 віджимань", 40, "початківець"),
        ("Стрибки на місці", "Виконайте 20 стрибків на місці", 20, "початківець"),
        ("Планка", "Утримуйте планку 20 секунд", 20, "початківець"),
        ("Біг на місці", "Біг на місці 1 хвилину", 60, "початківець"),
        ("Скручування", "10 повторень скручування для пресу", 40, "початківець"),
        ("Махи ногами", "Виконайте 10 махів ногами", 30, "початківець"),
        ("Випади", "10 повторень випадів", 40, "початківець"),
        ("Кругові рухи руками", "Кругові рухи руками 1 хвилину", 60, "початківець"),
        ("Нахили вперед", "10 нахилів вперед", 20, "початківець"),
        ("Присідання", "Виконайте 20 присідань", 60, "прокачаний"),
        ("Віджимання", "Виконайте 20 віджимань", 60, "прокачаний"),
        ("Стрибки на місці", "Виконайте 30 стрибків на місці", 30, "прокачаний"),
        ("Планка", "Утримуйте планку 40 секунд", 40, "прокачаний"),
        ("Біг на місці", "Біг на місці 2 хвилини", 120, "прокачаний"),
        ("Скручування", "15 повторень скручування для пресу", 50, "прокачаний"),
        ("Махи ногами", "Виконайте 15 махів ногами", 40, "прокачаний"),
        ("Випади", "15 повторень випадів", 60, "прокачаний"),
        ("Кругові рухи руками", "Кругові рухи руками 2 хвилини", 120, "прокачаний"),
        ("Нахили вперед", "15 нахилів вперед", 30, "прокачаний"),
        ("Присідання", "Виконайте 30 присідань", 90, "майстер"),
        ("Віджимання", "Виконайте 30 віджимань", 90, "майстер"),
        ("Стрибки на місці", "Виконайте 50 стрибків на місці", 60, "майстер"),
        ("Планка", "Утримуйте планку 60 секунд", 60, "майстер"),
        ("Біг на місці", "Біг на місці 3 хвилини", 180, "майстер"),
        ("Скручування", "20 повторень скручування для пресу", 60, "майстер"),
        ("Махи ногами", "Виконайте 20 махів ногами", 50, "майстер"),
        ("Випади", "20 повторень випадів", 90, "майстер"),
        ("Кругові рухи руками", "Кругові рухи руками 3 хвилини", 180, "майстер"),
        ("Нахили вперед", "20 нахилів вперед", 40, "майстер"),
    ]
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            for name, description, duration, level in exercises:
                cursor.execute('SELECT 1 FROM exercises WHERE name = ? AND level = ?', (name, level))
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO exercises (name, description, duration, level) VALUES (?, ?, ?, ?)',
                                   (name, description, duration, level))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Помилка при додаванні вправ: {e}")


def get_exercises_by_level(level):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE level=?", (level,))
    exercises = c.fetchall()
    conn.close()
    return exercises

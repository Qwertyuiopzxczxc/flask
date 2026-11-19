"""
Flask + MySQL: авторизация
Требования:
1. Схема и таблица users (id, user_name, user_password)
2. Класс Database (pymysql.connect, cursor, закрытие)
3. Метод get_user(username) -> запись или None
4. Проверка в route login: получить данные через Database, сверить пароль,
   обработать ошибки, сделать редирект
"""

import os
from flask import Flask, render_template, request, redirect, url_for, make_response

try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:
    raise ImportError("Установите pymysql: pip install pymysql")


# ==================== Конфигурация БД ====================
# Измените под свои настройки MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # ваш пользователь MySQL
    "password": "",          # ваш пароль MySQL
    "database": "flask_auth",
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
    "autocommit": True,
}


# ==================== Класс Database ====================
class Database:
    """Инкапсуляция работы с MySQL."""

    def __init__(self, config=None):
        self.config = config or DB_CONFIG
        self.connection = None
        self.cursor = None

    def connect(self):
        """Инициализация подключения через pymysql.connect(...)."""
        if self.connection is None or not self.connection.open:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
        return self

    def close(self):
        """Закрытие соединения."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_user(self, username):
        """
        Метод получения данных.
        Возвращает запись из users или None.
        """
        try:
            self.connect()
            self.cursor.execute(
                "SELECT id, user_name, user_password FROM users WHERE user_name = %s",
                (username,),
            )
            user = self.cursor.fetchone()
            return user  # dict или None
        except Exception as e:
            print(f"[Database] Ошибка get_user: {e}")
            return None
        finally:
            self.close()

    def create_user(self, username, password):
        """Дополнительный метод для регистрации (не требуется заданием)."""
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                (username, password),
            )
            return True
        except pymysql.err.IntegrityError:
            # UNIQUE violation
            return False
        except Exception as e:
            print(f"[Database] Ошибка create_user: {e}")
            return False
        finally:
            self.close()


# ==================== Flask-приложение ====================
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Простая in-memory сессия: token -> username
sessions = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Если уже авторизован — показываем страницу с именем
    token = request.cookies.get("auth_token")
    if token and token in sessions:
        return render_template("login.html", username=sessions[token])

    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                return render_template(
                    "login.html",
                    message="Заполните все поля!",
                )

            # --- Пункт 4 задания: проверка через Database ---
            db = Database()
            user = db.get_user(username)

            if user is None:
                return render_template(
                    "login.html",
                    message="Неверное имя пользователя или пароль!",
                )

            # Сверяем пароль (в реальном проекте — хеш!)
            if user["user_password"] != password:
                return render_template(
                    "login.html",
                    message="Неверное имя пользователя или пароль!",
                )

            # Успех: создаём токен и редирект
            token = os.urandom(32).hex()
            sessions[token] = user["user_name"]

            response = make_response(redirect(url_for("login")))
            response.set_cookie(
                "auth_token",
                token,
                httponly=True,
                samesite="Lax",
                max_age=3600 * 24,  # 1 день
            )
            return response

        except Exception as e:
            print(f"[login] Ошибка: {e}")
            return render_template(
                "login.html",
                message="Произошла ошибка при авторизации!",
            )

    # GET
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not password:
            return render_template(
                "register.html",
                message="Заполните все поля!",
                error=True,
            )
        if password != confirm:
            return render_template(
                "register.html",
                message="Пароли не совпадают!",
                error=True,
            )

        db = Database()
        ok = db.create_user(username, password)
        if ok:
            return render_template(
                "register.html",
                message="Регистрация успешна! Теперь можно войти.",
            )
        else:
            return render_template(
                "register.html",
                message="Пользователь уже существует или ошибка БД.",
                error=True,
            )

    return render_template("register.html")


@app.route("/logout")
def logout():
    token = request.cookies.get("auth_token")
    if token and token in sessions:
        del sessions[token]

    response = make_response(redirect(url_for("index")))
    response.delete_cookie("auth_token")
    return response


# ==================== SQL для создания схемы (выполнить один раз) ====================
"""
-- Выполните в MySQL:

CREATE DATABASE IF NOT EXISTS flask_auth;
USE flask_auth;

CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_name     VARCHAR(64)  NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL
);

INSERT INTO users (user_name, user_password)
VALUES ('Vladimir Putin', '123456789');
"""


if __name__ == "__main__":
    # Для локального запуска раскомментируйте:
    # from threading import Timer
    # import webbrowser
    # Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask, request, render_template, session, redirect, url_for
from database import Database

app = Flask(__name__)
app.secret_key = "change-me"          # обязательно для session

db = Database()                       # подключение к MySQL


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registr.html")

    # POST
    name = request.form.get("username", "").strip()
    pwd  = request.form.get("password", "").strip()

    # 1. Проверка на пустые поля
    if not name or not pwd:
        return render_template("registr.html", error="Заполните все поля")

    # 2. Проверка, что имя ещё не занято
    if db.get_user(name):
        return render_template("registr.html", error="Имя уже занято")

    try:
        # 3. Создаём пользователя
        db.create_user(name, pwd)
    except Exception as e:
        return render_template("registr.html", error=f"Ошибка БД: {e}")

    # 4. Успех → сохраняем в session и отдаём profile
    session["username"] = name
    return render_template("profile.html", username=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    # можно оставить старую логику или упростить
    if request.method == "GET":
        return render_template("login.html")
    # ... (по желанию)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

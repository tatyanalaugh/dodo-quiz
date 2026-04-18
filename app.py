# app.py — главный файл Flask-приложения
# Здесь описана вся логика викторины: загрузка вопросов, переход между ними и подсчёт результата.

import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

# Создаём приложение Flask.
app = Flask(__name__)

# Секретный ключ нужен для работы session (временного хранилища между страницами).
# В продакшене лучше брать его из переменной окружения, а не хранить в коде.
app.secret_key = os.environ.get("SECRET_KEY", "dodo-pizza-quiz-secret-key")


def load_questions():
    """Читает вопросы из JSON-файла и возвращает их списком."""
    path = os.path.join(os.path.dirname(__file__), "data", "questions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    """Главная страница с названием игры и кнопкой «Начать игру»."""
    # Сбрасываем прогресс, если пользователь вернулся на главную.
    session.clear()
    return render_template("index.html")


@app.route("/start")
def start():
    """Инициализируем новую игру: обнуляем счётчик правильных ответов
    и ставим индекс текущего вопроса на 0."""
    session["current"] = 0   # номер текущего вопроса (с нуля)
    session["score"] = 0     # сколько правильных ответов набрано
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Показывает вопросы по одному и обрабатывает ответы пользователя."""
    questions = load_questions()

    # Если сессии нет (например, открыли /quiz напрямую) — отправляем на главную.
    if "current" not in session:
        return redirect(url_for("index"))

    # Когда пользователь нажал кнопку ответа — приходит POST-запрос.
    if request.method == "POST":
        # Получаем индекс выбранного варианта ответа из формы.
        selected = int(request.form.get("answer", -1))
        current_index = session["current"]
        correct_index = questions[current_index]["correct"]

        # Если ответ правильный — увеличиваем счётчик.
        if selected == correct_index:
            session["score"] = session.get("score", 0) + 1

        # Переходим к следующему вопросу.
        session["current"] = current_index + 1

        # Если вопросы закончились — показываем результат.
        if session["current"] >= len(questions):
            return redirect(url_for("result"))

        return redirect(url_for("quiz"))

    # GET-запрос: просто показываем текущий вопрос.
    current_index = session["current"]
    question = questions[current_index]

    return render_template(
        "quiz.html",
        question=question,
        question_number=current_index + 1,
        total=len(questions),
    )


@app.route("/result")
def result():
    """Показывает итоговый результат: сколько правильных из всего."""
    questions = load_questions()
    score = session.get("score", 0)
    total = len(questions)

    # После показа результата очищаем сессию.
    session.clear()

    return render_template("result.html", score=score, total=total)


# Запуск локального сервера.
# В продакшене (например, на Render) запускает Gunicorn, а не этот блок.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

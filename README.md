# 🍕 Додо Викторина

Простая игра-викторина на Flask, подсвечивающая любопытные факты из датасета Додо Пиццы.
Оформлена в фирменном стиле Додо: оранжевый акцент, закруглённый шрифт, белый фон.

## Структура проекта

```
dodo-quiz/
├── app.py                 # главный файл Flask
├── requirements.txt       # зависимости
├── Procfile               # команда запуска для Render
├── .gitignore
├── data/
│   └── questions.json     # вопросы викторины
├── static/
│   ├── css/
│   │   └── style.css      # все стили
│   └── img/               # сюда класть картинки / графики
└── templates/
    ├── base.html          # базовый шаблон
    ├── index.html         # главная
    ├── quiz.html          # страница вопроса
    └── result.html        # результат
```

## Установка и запуск локально

```bash
# 1. Клонируй репозиторий
git clone <адрес-репозитория>
cd dodo-quiz

# 2. Создай виртуальное окружение
python -m venv venv

# 3. Активируй его
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Установи зависимости
pip install -r requirements.txt

# 5. Запусти приложение
python app.py
```

Открой в браузере: **http://localhost:5000**

## Деплой на Render

1. Залей проект на GitHub.
2. На [render.com](https://render.com) → **New → Web Service** → подключи репозиторий.
3. Настройки:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Нажми **Create Web Service**. Через пару минут сервис будет доступен по публичному URL.

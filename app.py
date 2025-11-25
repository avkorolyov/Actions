"""REST API на Flask с базовыми эндпоинтами для проверки контейнера."""

import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешить CORS для всех origins

# Конфигурация приложения
APP_NAME = "my-flask-app"
APP_VERSION = "1.0.0"

ENDPOINTS = {
    "/": "Описание сервиса и список эндпоинтов",
    "/health": "Проверка готовности контейнера",
    "/info": "Метаданные о приложении",
    "/env": "Сводка ключевых переменных окружения",
    "/multiply/<a>/<b>": "Умножение двух чисел",
    "/divide/<a>/<b>": "Деление двух чисел",
}


@app.route("/")
def root():
    """Главная страница со списком эндпоинтов."""
    return jsonify({
        "message": "Минимальная конфигурация приложения работает",
        "endpoints": ENDPOINTS,
    })


@app.route("/health")
def health():
    """Проверка здоровья приложения."""
    return jsonify({
        "status": "ok",
        "details": "Контейнер отвечает на запросы",
    })


@app.route("/info")
def info():
    """Метаданные о приложении."""
    return jsonify({
        "app": APP_NAME,
        "version": APP_VERSION,
        "port": os.environ.get("PORT", "5001"),
    })


@app.route("/env")
def env():
    """Сводка ключевых переменных окружения."""
    return jsonify({
        "env": {
            "PORT": os.environ.get("PORT", "5001"),
            "HOSTNAME": os.environ.get("HOSTNAME", "unknown"),
        }
    })


@app.route("/multiply/<a>/<b>")
def multiply(a, b):
    """Умножение двух чисел."""
    try:
        num_a = float(a)
        num_b = float(b)
    except ValueError:
        return jsonify({"error": "Параметры должны быть числами."}), 400
    
    return jsonify({
        "operation": "multiply",
        "a": num_a,
        "b": num_b,
        "result": num_a * num_b,
    })


@app.route("/divide/<a>/<b>")
def divide(a, b):
    """Деление двух чисел."""
    try:
        num_a = float(a)
        num_b = float(b)
    except ValueError:
        return jsonify({"error": "Параметры должны быть числами."}), 400
    
    if num_b == 0:
        return jsonify({"error": "Деление на ноль запрещено."}), 400
    
    return jsonify({
        "operation": "divide",
        "a": num_a,
        "b": num_b,
        "result": num_a / num_b,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    print(f"Запуск Flask-сервера на порту {port}", flush=True)
    app.run(host="0.0.0.0", port=port)

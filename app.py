import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    """Минимальный HTTP-обработчик с базовыми эндпоинтами для проверки контейнера."""

    ENDPOINTS = {
        "/": "Описание сервиса и список эндпоинтов",
        "/health": "Проверка готовности контейнера",
        "/info": "Метаданные о приложении",
        "/env": "Сводка ключевых переменных окружения",
        "/multiply/<a>/<b>": "Умножение двух чисел",
        "/divide/<a>/<b>": "Деление двух чисел",
    }

    def do_GET(self):
        """Маршрутизация GET-запросов по поддерживаемым эндпоинтам."""
        path = self.path.split("?", 1)[0]

        if path == "/":
            self._json_response(
                200,
                {
                    "message": "Минимальная конфигурация приложения работает",
                    "endpoints": self.ENDPOINTS,
                },
            )
        elif path == "/health":
            self._json_response(
                200,
                {
                    "status": "ok",
                    "details": "Контейнер отвечает на запросы",
                },
            )
        elif path == "/info":
            self._json_response(
                200,
                {
                    "app": "my-flask-app",
                    "version": "1.0.0",
                    "port": self._port_env(),
                },
            )
        elif path == "/env":
            self._json_response(
                200,
                {
                    "env": {
                        "PORT": self._port_env(),
                        "HOSTNAME": os.environ.get("HOSTNAME", "unknown"),
                    }
                },
            )
        elif path.startswith("/multiply"):
            self._math_response(path, "multiply")
        elif path.startswith("/divide"):
            self._math_response(path, "divide")
        else:
            self._json_response(
                404,
                {
                    "error": "Эндпоинт не найден",
                    "available": list(self.ENDPOINTS.keys()),
                },
            )

    def _json_response(self, status: int, payload: dict) -> None:
        """Формирование JSON-ответа с нужным статусом."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _port_env() -> str:
        """Получение порта из окружения с дефолтом 5001."""
        return os.environ.get("PORT", "5001")

    def _math_response(self, path: str, operation: str) -> None:
        """Обработка арифметических запросов /multiply/<a>/<b> и /divide/<a>/<b>."""
        parts = path.strip("/").split("/")

        if len(parts) != 3:
            self._json_response(
                400,
                {
                    "error": "Некорректный путь. Используйте /multiply/<a>/<b> или /divide/<a>/<b>",
                },
            )
            return

        try:
            a = float(parts[1])
            b = float(parts[2])
        except ValueError:
            self._json_response(
                400,
                {"error": "Параметры должны быть числами."},
            )
            return

        if operation == "divide":
            if b == 0:
                self._json_response(
                    400,
                    {"error": "Деление на ноль запрещено."},
                )
                return
            result = a / b
        else:
            result = a * b

        self._json_response(
            200,
            {
                "operation": operation,
                "a": a,
                "b": b,
                "result": result,
            },
        )


def main():
    port = int(os.environ.get("PORT", "5001"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Запуск тестового HTTP-сервера контейнера на порту {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()


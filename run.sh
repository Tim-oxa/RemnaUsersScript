#!/bin/bash
set -e

VENV_DIR=$(mktemp -d)
TEMP_FILE="main.py"

cleanup() {
    echo "Очистка временных файлов..."
    deactivate 2>/dev/null || true
    rm -rf "$VENV_DIR"
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

echo "Подготовка окружения..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "Установка зависимостей..."
pip install -r https://raw.githubusercontent.com/Tim-oxa/RemnaUsersScript/main/requirements.txt

echo "Скачивание скрипта..."
curl -sSL https://raw.githubusercontent.com/Tim-oxa/RemnaUsersScript/main/main.py -o "$TEMP_FILE"

echo "Запуск..."
python "$TEMP_FILE" < /dev/tty > /dev/tty

echo "Обновление завершено!"

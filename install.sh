#!/bin/bash

USERNAME=$(whoami)
GROUP=$(id -gn)

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

# Установка Python 3, если он не установлен
if ! command -v python3 &> /dev/null; then
    echo "Установка Python 3..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

# Установка pip, если он не установлен
if ! command -v pip3 &> /dev/null; then
    echo "Установка pip..."
    sudo apt-get install -y python3-pip
fi

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

# Установка python3-venv для создания виртуального окружения
if ! dpkg -l | grep -qw python3-venv; then
    echo "Установка пакета python3-venv..."
    sudo apt-get install -y python3-venv
fi

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Установка зависимостей Python..."
cd /home/$USERNAME/Synthia_TXID_Bot

# Создание виртуального окружения, если оно еще не создано
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip3 install -r requirements.txt

# Деактивация виртуального окружения
deactivate

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

# Запрос токена у пользователя
read -p "Введите токен Telegram бота: " TELEBOT_TOKEN
echo "TELEBOT_TOKEN=$TELEBOT_TOKEN" > .env
echo "BOT_NAME=@synthia_txid_bot" >> .env
echo "TARGET_CHAT=-4075650689" >> .env

unset TELEBOT_TOKEN

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

# Создание и настройка systemd-сервиса
sudo bash -c "cat <<EOF > /etc/systemd/system/synthia.service
[Unit]
Description=Synthia Python Project
After=network.target

[Service]
User=$USERNAME
Group=$GROUP
WorkingDirectory=/home/$USERNAME/synthia_txid_bot
ExecStart=/home/$USERNAME/synthia_txid_bot/venv/bin/python3 /home/$USERNAME/synthia_txid_bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Перезагрузка systemd..."
sudo systemctl daemon-reload

echo "Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Запуск и настройка автозапуска сервиса..."
sudo systemctl enable synthia
sudo systemctl start synthia

echo "Установка завершена. Проект Synthia настроен как systemd-сервис."
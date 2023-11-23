#!/bin/bash

USERNAME=$(whoami)
GROUP=$(id -gn)

echo "Установка Python 3..."
if ! command -v python3 &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3
fi

echo "Готово. Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Установка pip..."
if ! command -v pip3 &> /dev/null; then
    sudo apt-get install -y python3-pip
fi

echo "Готово. Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Установка пакета python3-venv..."
if ! dpkg -l | grep -qw python3-venv; then
    sudo apt-get install -y python3-venv
fi

echo "Готово. Нажмите любую клавишу для продолжения..."
read -n 1 -s

echo "Установка зависимостей Python..."
cd /home/$USERNAME/synthia_txid_bot

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip3 install -r requirements.txt
deactivate

echo "Готово. Нажмите любую клавишу для продолжения..."
read -n 1 -s

read -p "Введите токен Telegram бота: " TELEBOT_TOKEN

echo "TELEBOT_TOKEN=$TELEBOT_TOKEN" > .env
echo "BOT_NAME=@synthia_txid_bot" >> .env
echo "TARGET_CHAT=-4075650689" >> .env

unset TELEBOT_TOKEN

echo "Готово. Нажмите любую клавишу для продолжения..."
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

echo "Перезагрузка systemd..."
sudo systemctl daemon-reload

echo "Запуск и настройка автозапуска сервиса..."
sudo systemctl enable synthia
sudo systemctl start synthia

echo "Установка завершена. Проект Synthia настроен как systemd-сервис."
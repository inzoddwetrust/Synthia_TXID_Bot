#!/bin/bash

# Проверить наличие Python 3
if ! command -v python3 &> /dev/null; then
    echo "Установка Python 3..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Проверить наличие pip
if ! command -v pip &> /dev/null; then
    echo "Установка pip..."
    sudo apt-get install -y python3-pip
fi

# Установка зависимостей Python (перейти в рабочий каталог проекта)
echo "Установка зависимостей Python..."
cd /home/$USER/Synthia_TXID_Bot
pip install -r requirements.txt

# Установка проекта как systemd-сервиса

# Создать файл unit-сервиса (например, synthia.service)
cat <<EOF > /etc/systemd/system/synthia.service
[Unit]
Description=Synthia Python Project

[Service]
ExecStart=/usr/bin/python3 /home/$USER/Synthia_TXID_Bot/main.py
WorkingDirectory=/home/$USER/Synthia_TXID_Bot
Restart=always
User=$USER
Group=$GROUP

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузить systemd для применения изменений
echo "Перезагрузка systemd..."
systemctl daemon-reload

# Запустить сервис и включить его в автозапуск
echo "Запуск и настройка автозапуска сервиса..."
systemctl start synthia
systemctl enable synthia

# Завершение скрипта с сообщением об успешной установке
echo "Установка завершена. Проект Synthia настроен как systemd-сервис."

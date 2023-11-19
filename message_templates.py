# -*- coding: utf-8 -*-


def create_transaction_details_message(transaction_info):
    return (
            f"🔁 Отправитель: {transaction_info['from_address']}\n"
            f"🎯 Получатель: {transaction_info['to_address']}\n"
            f"💲 Сумма: {transaction_info['amount']} USDT\n"
            f"💸 Комиссия: {transaction_info['fee']} USDT\n"
            f"🕒 Время транзакции: {transaction_info['timestamp']}\n"
            f"📌 Статус: {transaction_info['status']}\n"
            f"👤 Клиент: {transaction_info['client']}\n"
            f"💰 Дилер: {transaction_info['dealer']}\n"
            f"🚘 Автомобиль: {transaction_info['car']}\n"
            f"💵 Назначение платежа: {transaction_info['reason']}\n"
            f"💬 Комментарий: {transaction_info['comment']}\n\n"
            )


def create_superstring_message(superstring):
    return (
        f"А вот и Суперстрока! (просто кликни на нее и вставь в таблицу):\n\n"
        f"<code>●|{superstring['client']}|{superstring['dealer']}|●|●|{superstring['car']}|●|●|●|●|●|●|●|●|●|●|{superstring['reason']}|{superstring['timestamp']}|●|{float(superstring['amount'])+float(superstring['fee'])}|●|●|●|{superstring['link']}</code>"
    )
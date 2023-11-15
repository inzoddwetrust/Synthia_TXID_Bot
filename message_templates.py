def create_transaction_details_message(transaction_info):
    return (f"From Address: {transaction_info['from_address']}\n"
            f"To Address: {transaction_info['to_address']}\n"
            f"Amount: {transaction_info['amount']} USDT\n"
            f"Fee: {transaction_info['fee']} USDT\n"
            f"Timestamp: {transaction_info['timestamp']}\n"
            f"Status: {transaction_info['status']}\n"
            f"Клиент: {transaction_info['client']}\n"
            f"Дилер: {transaction_info['dealer']}\n"
            f"Автомобиль: {transaction_info['car']}\n"
            f"Назначение платежа: {transaction_info['reason']}\n"
            f"Комментарий: {transaction_info['comment']}\n\n"
            )


def create_superstring_message(superstring):
    return (
        f"А вот и Суперстрока!\n\n"
        f"<code>{car_params['full_name']}|●|●|{car_params['year']}|{car_params['body']}|{car_params['fuel']}|{car_params['gear']}|{car_params['material']}|{car_params['hp']}|{car_params['litre']}|{car_params['drive']}|●|●|{car_params['price']}|{car_params['link']}|{car_data['dongchendi_url']}</code>"
    )

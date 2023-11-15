import message_templates as mt
import requests
from datetime import datetime


def get_tron_transaction_details(tx_hash):
    api_url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx_hash}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        json_data = response.json()

        # Извлекаем необходимую информацию из JSON и создаем словарь
        transaction_info = {
            'from_address': json_data.get('ownerAddress', 'Not available'),
            'to_address': json_data.get('toAddress', 'Not available'),
            'amount': int(json_data.get('trc20TransferInfo', [{}])[0].get('amount_str', 'Not available'))/1000000,
            'fee': 2.0,
            'timestamp': datetime.fromtimestamp(json_data.get('timestamp', 0) / 1000.0).strftime(
                '%Y-%m-%d %H:%M:%S') if 'timestamp' in json_data else 'Not available',
            'status': json_data.get('contractRet', 'Not available'),
            'client': None,
            'dealer': None,
            'car': None,
            'reason': None,
            'comment': None
        }

        # Используем функцию шаблона для создания сообщения
        result = mt.create_transaction_details_message(transaction_info)

        return result, transaction_info

    except requests.RequestException as e:
        print(e)
        return "An error occurred while fetching the transaction details."

import re
import telebot
from telebot import types
from processing import get_tron_transaction_details
import uuid
import message_templates as mt

bot = telebot.TeleBot('6951849445:AAG9qk70t3HAZr83xtKJJskHmxBeEX8aE6s')

tron_pattern = r'\b([0-9a-fA-F]{64})\b'
temp_storage = {}
superstring = {}


@bot.message_handler(func=lambda message: re.search(tron_pattern, message.text))
def message_with_link(message):
    tron_data = re.findall(tron_pattern, message.text)[0]

    if tron_data:
        unique_id = str(uuid.uuid4())
        temp_storage[unique_id] = tron_data
        print(temp_storage)

        markup = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton('Yes, save it!', callback_data=f'save:{unique_id}')
        no_button = types.InlineKeyboardButton('No, thanks.', callback_data='ignore')
        markup.add(yes_button, no_button)
        bot.reply_to(message, 'Do you want to save this Tron transaction?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save:'))
def handle_save_callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    unique_id = call.data.split(':')[1]

    # Check if the unique_id exists in temp_storage
    if unique_id in temp_storage:
        tron_data = temp_storage[unique_id]

        try:
            prefix = f"Вот что мы получили:\n\n"
            response, transaction_info = get_tron_transaction_details(tron_data)
            superstring[user_id] = transaction_info
            postfix = (f"У нас не все данные, давай заполним остальные?"
                       f"\n(можно писать кратко, потом заполним нормально)"
                       )
            bot.send_message(chat_id, prefix+response+postfix)

            msg = bot.send_message(user_id, "👤 Кто клиент транзакции?")
            bot.register_next_step_handler(msg, client_step)

        except Exception as e:
            bot.answer_callback_query(call.id,
                                      "I can't send you the data. Please make sure you have started a chat with me.")
            print(e)  # For debugging purposes
    else:
        bot.answer_callback_query(call.id, "The data you are trying to save is no longer available.")


def client_step(message):
    try:
        superstring[message.from_user.id]["client"] = message.text
        msg = bot.reply_to(message, '💰 А кто дилер?')
        bot.register_next_step_handler(msg, dealer_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!')


def dealer_step(message):
    try:
        superstring[message.from_user.id]["dealer"] = message.text
        msg = bot.reply_to(message, '🚘 Какой автомобиль?')
        bot.register_next_step_handler(msg, car_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!')


def car_step(message):
    try:
        superstring[message.from_user.id]["car"] = message.text
        msg = bot.reply_to(message, '💵 И назначение платежа?')
        bot.register_next_step_handler(msg, reason_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!')


def reason_step(message):
    try:
        superstring[message.from_user.id]["reason"] = message.text
        print(superstring)

        prefix = f"Проверяем:\n\n"
        bot.send_message(message.chat.id, prefix + mt.create_transaction_details_message(superstring[message.from_user.id]))

        # msg = bot.reply_to(message, '💵 И назначение платежа?')
        # bot.register_next_step_handler(msg, dealer_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!')


@bot.callback_query_handler(func=lambda call: call.data == 'do_not_save')
def handle_do_not_save_callback_query(call):
    bot.answer_callback_query(call.id, text="You chose not to save the link.")


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()

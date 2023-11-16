import re
import telebot
from telebot import types
from processing import get_tron_transaction_details
import uuid
import message_templates as mt

bot = telebot.TeleBot('6951849445:AAG9qk70t3HAZr83xtKJJskHmxBeEX8aE6s')
bot_name = '@synthia_txid_bot'
target_chat = '-1001940414840'

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
        yes_button = types.InlineKeyboardButton('Ага, давай!', callback_data=f'save:{unique_id}')
        no_button = types.InlineKeyboardButton('Нет, не надо.', callback_data='do_not_save')
        markup.add(yes_button, no_button)
        bot.reply_to(message, 'Похоже, это новая транзакция! Сохраним?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save:'))
def handle_save_callback_query(call):
    user_name = call.from_user.username
    user_id = call.from_user.id
    unique_id = call.data.split(':')[1]

    if unique_id in temp_storage:
        tron_data = temp_storage[unique_id]

        try:
            # bot.send_message(call.message.chat.id, f'Хорошо, {call.from_user.first_name}.\n\n'
            #                                        f'Tогда продолжим в личке, пойдем в {bot_name}')
            prefix = f"Итак, у нас новая транзакция:\n\n"
            response, transaction_info = get_tron_transaction_details(tron_data)
            superstring[user_id] = transaction_info
            postfix = (f"Здесь не все данные, давай заполним остальные?"
                       f"\n(можно писать кратко, потом заполним нормально)"
                       )
            bot.send_message(user_id, prefix + response + postfix)

            msg = bot.send_message(user_id, "👤 Кто клиент транзакции?")
            bot.register_next_step_handler(msg, client_step)

        except Exception as e:
            bot.send_message(call.message.chat.id,
                             f"К сожалению, я не могу тебе ничего послать, пока ты не начнешь со мной диалог...\n"
                             f"Ты впервые общаешься со мной, и у мена нет разрешения писать тебе первой.\n\n"
                             f"Зайди в {bot_name} и нажми мне START, а потом вернись сюда.")
            print(e)  # For debugging purposes

        else:
            bot.send_message(call.message.chat.id, f'Хорошо, {call.from_user.first_name}.\n\n'
                                                   f'Tогда продолжим в личке, пойдем в {bot_name}')

    else:
        bot.answer_callback_query(call.id, "Слушай, это очень старая транза, запости ее сюда еще раз.")


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
        msg = bot.reply_to(message, '💬 А комментарий надо?')
        bot.register_next_step_handler(msg, final_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!')


def final_step(message):
    try:
        superstring[message.from_user.id]["comment"] = message.text

        markup = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton('Да, отправляем!', callback_data=f'send:{message.from_user.id}')
        no_button = types.InlineKeyboardButton('Нет', callback_data='ignore')
        markup.add(yes_button, no_button)

        prefix = f"Проверяем:\n\n"
        response = mt.create_transaction_details_message(superstring[message.from_user.id])
        postfix = f"\n Все верно? Передаем в ANTCAR-FINANCE?"
        bot.send_message(message.chat.id, prefix + response + postfix, reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'ooops!')


@bot.callback_query_handler(func=lambda call: call.data == 'do_not_save')
def handle_do_not_save_callback_query(call):
    bot.answer_callback_query(call.id, text="Мы не сохраняем эту транзакцию.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('send:'))
def send_to_acounter(call):
    bot.answer_callback_query(call.id, text="Sending")
    print(f"WE ARE HERE!\n {superstring}")

    prefix = f"@{call.from_user.username} запостил в одном из чатов транзакцию, связанную с AntCar:\n\n"
    response = mt.create_transaction_details_message(superstring[call.from_user.id])
    postfix = f"\n А тут Суперстрока"
    bot.send_message(target_chat, prefix + response + postfix)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ignore'))
def dont_send_to_acounter(call):
    bot.answer_callback_query(call.id, 'Вы отменили операцию.')
    bot.send_message(call.message.chat.id, 'Ну ладно тогда. Но если передумаешь, тогда нажми "Отправить"')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()

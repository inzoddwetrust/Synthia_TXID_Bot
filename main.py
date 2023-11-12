import re
import telebot
from telebot import types

bot = telebot.TeleBot('6951849445:AAG9qk70t3HAZr83xtKJJskHmxBeEX8aE6s')

tron_pattern = r'\b([0-9a-fA-F]{64})\b'
temp_storage = {}


@bot.message_handler(func=lambda message: re.search(tron_pattern, message.text))
def message_with_link(message):
    tron_data = re.findall(tron_pattern, message.text)[0]
    print(tron_data)

    if tron_data:
        # We'll store a tuple of URLs and TXIDs with a unique ID
        unique_id = str(hash(frozenset(tron_data)))  # A simple unique identifier
        temp_storage[unique_id] = tron_data
        print(temp_storage)

        # Send confirmation message with inline keyboard
        markup = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton('Yes, save it!', callback_data=f'save:{unique_id}')
        no_button = types.InlineKeyboardButton('No, thanks.', callback_data='ignore')
        markup.add(yes_button, no_button)
        bot.reply_to(message, 'Do you want to save this Tron transaction?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save:'))
def handle_save_callback_query(call):
    unique_id = call.data.split(':')[1]

    # Check if the unique_id exists in temp_storage
    if unique_id in temp_storage:
        tron_data = temp_storage[unique_id]

        # Send the saved Tron data to the user's private chat
        try:
            response_message = f"Here are the Tron transaction details you wanted to save:\n " \
                               f"https://apilist.tronscanapi.com/api/transaction-info?hash={tron_data} \n "
            bot.send_message(call.from_user.id, response_message)
            del temp_storage[unique_id]  # Clean up after sending
        except Exception as e:
            # Inform the user if the bot cannot send them the message
            bot.answer_callback_query(call.id,
                                      "I can't send you the data. Please make sure you have started a chat with me.")
            print(e)  # For debugging purposes
    else:
        # Inform the user that the data is no longer available
        bot.answer_callback_query(call.id, "The data you are trying to save is no longer available.")

    # This call should be outside the 'if' block to ensure it's always executed.
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'do_not_save')
def handle_do_not_save_callback_query(call):
    bot.answer_callback_query(call.id, text="You chose not to save the link.")


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()

import re
import telebot
from telebot import types


# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
bot = telebot.TeleBot('6951849445:AAG9qk70t3HAZr83xtKJJskHmxBeEX8aE6s')

# Regular expression to match URLs
url_regex = r'(https?://\S+|www\.\S+)'


@bot.message_handler(func=lambda message: re.search(url_regex, message.text))
def message_with_link(message):
    # Display an inline keyboard in the group chat itself
    markup = types.InlineKeyboardMarkup()
    urls = re.findall(url_regex, message.text)
    if urls:  # If any URL is found
        # Serialize the user ID and the first URL into a string that can be passed in the callback data
        callback_data = f"save_link:{message.message_id}:{message.from_user.id}:{urls[0]}"
        if len(callback_data.encode('utf-8')) > 64:  # Telegram allows up to 64 bytes for callback data
            bot.reply_to(message, 'Error: The link is too long to handle.')
            return

        yes_button = types.InlineKeyboardButton('Yes, save it!', callback_data=callback_data)
        no_button = types.InlineKeyboardButton('No, thanks.', callback_data='do_not_save')
        markup.add(yes_button, no_button)
        bot.reply_to(message, 'Do you want to save this link?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save_link'))
def handle_save_link_callback_query(call):
    # Extracting the message ID, user ID, and URL from the callback data
    action, message_id, from_user_id, url = call.data.split(':', 3)
    message_id = int(message_id)
    from_user_id = int(from_user_id)

    try:
        # Send only the extracted URL to the user's private chat
        bot.send_message(from_user_id, f"Here's the link you wanted to save: {url}")
    except Exception as e:
        bot.reply_to(call.message,
                     'I cannot send you the link unless you start a conversation with me. Please message me directly '
                     'first.')
        print(e)  # For debugging purposes, you might want to log the exception somewhere instead of printing it

    bot.answer_callback_query(call.id, text="You chose to save the link.")


@bot.callback_query_handler(func=lambda call: call.data == 'do_not_save')
def handle_do_not_save_callback_query(call):
    bot.answer_callback_query(call.id, text="You chose not to save the link.")


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
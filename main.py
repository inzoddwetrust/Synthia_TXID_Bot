import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Replace 'YOUR_TELEGRAM_CHAT_ID' with your chat ID where you want to receive the forwarded messages
MY_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'


# Handler for messages
@bot.message_handler(func=lambda message: True)
def check_message(message):
    # Check if the message contains a URL by looking for 'http' or 'www' in the text
    if 'http' in message.text or 'www' in message.text:
        # Forward the message to the specified chat ID
        bot.forward_message(MY_CHAT_ID, message.chat.id, message.message_id)


# Polling
bot.polling(none_stop=True)

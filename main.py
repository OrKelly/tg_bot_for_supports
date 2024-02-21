import os

import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('token'))


@bot.message_handler(content_types=['text'])
def test(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)

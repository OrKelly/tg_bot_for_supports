import telebot

bot = telebot.TeleBot('7074789076:AAFf8zgZ89vmLm1IgNcg8CAh7yLsqxIU2zs')

from telebot import types

@bot.message_handler(content_types=['text'])
def test(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
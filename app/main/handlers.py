from telebot import TeleBot
from telebot.types import Message

from app.main.keyboard import main_keyboard


def init_handlers(bot: TeleBot):
    @bot.message_handler(regexp='Обратно')
    @bot.message_handler(commands=['start'])
    def startup(message: Message):
        text = 'Привет, я бот помощник для работников поддержки Т-Банка. Давайте начнём? Выберите интересующую вас ' \
               'функцию'
        bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

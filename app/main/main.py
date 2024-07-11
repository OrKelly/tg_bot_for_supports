import os

from dotenv import load_dotenv
from telebot import TeleBot
from telegram_client import TelegramClient

from app.calc.handlers import init_handlers as calc_handlers
from app.main.handlers import init_handlers as main_handlers
from app.qa.handlers import init_handlers as qa_handlers

load_dotenv()
token = os.getenv('TOKEN')
url = os.getenv('URL')
admin_chat = os.getenv('ADMIN_CHAT_ID')
logger = TelegramClient(token=token, url=url)
bot = TeleBot(token)

main_handlers(bot)
qa_handlers(bot)
calc_handlers(bot)


while True:
    try:
        bot.polling()
    except Exception as e:
        message = f'Произошла ошибка! {e.__class__}:{e}'
        print(message)
        logger.post(method='sendMessage', params={'chat_id': admin_chat,
                                                  'text': message})

from telebot import TeleBot

from app.calc.scrapy import Scrapy


def init_handlers(bot: TeleBot):
    @bot.message_handler(regexp='Калькулятор зарплаты')
    def salary_calc(message):
        bot.register_next_step_handler(message, calc_user_salary)
        bot.send_message(message.chat.id,
                         'Пришлите мне email, чтоб я мог посчитать зарплату! Если потребуется помощь, пиши'
                         ' /help_salary_calc')

    def calc_user_salary(message):
        if message.content_type == 'document':
            scrapy = Scrapy(bot=bot, message=message)
            salary, pre_salary = scrapy.get_salary()
            text = (f'Готово! Смотрите, как много вы заработали:\n\n'
                    f'Предоплата: {round(pre_salary, 2)}\n\nЗарплата: {round(salary, 2)}')
            bot.send_message(message.chat.id, text)
        elif message.text == '/help_salary_calc':
            bot.register_next_step_handler(message, calc_help)
        else:
            bot.send_message(message.chat.id, 'Мне нужен файл, чтобы считать его содержимое! Повторите попытку')

    @bot.message_handler(commands=['help_salary_calc'])
    def calc_help(message):
        text = ('Привет! На связи калькулятор зарплаты!\n'
                'Я создан для того, чтобы считать вашу зарплату еще до выхода сверки.\n'
                'Для начала подсчета пришлите скачанный email со сверкой, и пришлите мне его сюда. '
                'Ниже ссылка, как его скачать:\n'
                'https://www.unisender.com/ru/blog/kak-sohranit-pisma-iz-gmail-yandex-i-outlook-na-kompyuter/\n'
                'Удачного иcпользования!')
        bot.send_message(message.chat.id, text)

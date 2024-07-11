from telebot import TeleBot

from app.qa.dao import QaDAO
from app.qa.keyboard import (delete_marks_keyboard, delete_one_mark_keyboard,
                             qa_main_keyboard)
from app.qa.utils import validate_marks


def init_handlers(bot: TeleBot):
    @bot.message_handler(regexp='Оценки|Назад к оценкам')
    def marks_main(message):
        text = 'Выберите интересующую вас опцию:'
        bot.send_message(message.chat.id, text, reply_markup=qa_main_keyboard())

    @bot.message_handler(regexp='Добавить оценку')
    def marks_add_handler(message):
        text = (
            'Введите оценку. Вы можете ввести одну или несколько оценок, но для этого отделите их запятой (пример: 0,'
            '100, 100)')
        bot.register_next_step_handler(message, add_mark_func)
        bot.send_message(message.chat.id, text)

    @bot.message_handler(regexp='Посчитать средний балл')
    def marks_stat(message):
        bot.send_message(message.chat.id, 'Одну минутку, я уже считаю вашу статистику!')
        marks_avg = QaDAO.get_stat(message.chat.id)
        all_marks = QaDAO.select_all_filter({'user': message.chat.id})
        if not marks_avg['avg']:
            bot.send_message(message.chat.id, 'У вас еще нет оценок! Посчитать балл не получится!',
                             reply_markup=qa_main_keyboard())
        else:
            marks = '\n'.join([f'Оценка: {str(mark["mark"])}' for mark in all_marks])
            text = f'''Статистика:\n\nВаши оценки:\n{marks}\n\nСредний балл - {int(marks_avg["avg"])}'''
            bot.send_message(message.chat.id, text, reply_markup=qa_main_keyboard())

    @bot.message_handler(regexp='Прогноз среднего балла')
    def mark_predict(message):
        bot.register_next_step_handler(message, predict_mark_func)
        bot.send_message(message.chat.id, 'Введите средний балл, который вы хотите видеть')

    @bot.message_handler(regexp='Удаление оценок')
    def delete_marks_func(message):
        bot.send_message(message.chat.id, 'Выберите опцию:', reply_markup=delete_marks_keyboard())

    @bot.message_handler(regexp='Удалить одну')
    def delete_one_mark(message):
        bot.register_next_step_handler(message, delete_one_mark_func)
        bot.send_message(message.chat.id, 'Выберите оценку:', reply_markup=delete_one_mark_keyboard(message.chat.id))

    @bot.message_handler(regexp='Удалить все')
    def delete_all_marks(message):
        QaDAO.delete_all_user_marks(message.chat.id)
        bot.send_message(message.chat.id, 'Все оценки были удалены!', reply_markup=delete_marks_keyboard())

    def add_mark_func(message):
        text = []
        added = 0
        marks = message.text.split(',')
        if len(marks) > 1:
            for mark in marks:
                mark = mark.strip()
                if validate_marks(mark):
                    added += 1
                    QaDAO.add({'mark': mark, 'user': message.chat.id})
                else:
                    text.append(f'Оценка {mark} не прошла проверку! Она должна быть целым числом от 0 до 100')
        elif len(marks) == 1:
            if validate_marks(marks[0]):
                added += 1
                QaDAO.add({'mark': marks[0], 'user': message.chat.id})
            else:
                text.append(f'Оценка {marks[0]} не прошла проверку! Она должна быть целым числом от 0 до 100')
        else:
            text.append('Вы не ввели оценку')
        if added == len(marks):
            text = 'Все оценки были добавлены'
        elif len(text) != len(marks):
            text.append('Остальные оценки прошли проверку')
        bot.send_message(message.chat.id, text if isinstance(text, str) else '.\n'.join(text))

    def delete_one_mark_func(message):
        if message.text != 'Назад к оценкам':
            id = message.text.split()[0].strip()
            QaDAO.delete(id=id)
            bot.send_message(message.chat.id, 'Оценка была удалена!', reply_markup=delete_marks_keyboard())
        else:
            bot.send_message(message.chat.id, 'Окей, возвращаемся!', reply_markup=qa_main_keyboard())

    def predict_mark_func(message):
        stat = message.text
        count = 0
        if not validate_marks(stat):
            bot.register_next_step_handler(message, predict_mark_func)
            bot.send_message(message.chat.id, 'Введите целое число от 1 до 100')
        else:
            marks = QaDAO.get_mark_count_and_sum(message.chat.id)
            marks_avg = marks['avg']
            marks_sum = marks['sum']
            marks_count = marks['count']
            if marks_avg >= int(stat):
                bot.register_next_step_handler(message, predict_mark_func)
                bot.send_message(message.chat.id, f'Балл {stat} меньше либо равен {marks_avg}. Попробуй еще раз!')
            else:
                if marks_sum % 100 != 0 and int(stat) == 100:
                    bot.send_message(message.chat.id,
                                     'Получить оценку 100 уже не выйдет! Её невозможно получить если вы'
                                     'получили хоть раз балл ниже 100')
                else:
                    while int(stat) > marks_avg and count < 15:
                        count += 1
                        marks_sum += 100
                        marks_count += 1
                        marks_avg = marks_sum / marks_count
                    if marks_avg < int(stat):
                        bot.send_message(message.chat.id,
                                         f'Для получения такого балла требуется запредельное кол-во оценок!'
                                         f' Получить такой балл невозможно, так-как потребуются десятки '
                                         f'100 подряд')
                    else:
                        bot.send_message(message.chat.id,
                                         f'Для получения балла {stat} вам нужно набрать {count} оценок 100. '
                                         f'В таком случае ваш балл будет равен {marks_avg}')
from telebot import types

from app.qa.dao import QaDAO


def qa_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_mark = types.KeyboardButton('Добавить оценку')
    get_mark_stat = types.KeyboardButton('Посчитать средний балл')
    delete_marks = types.KeyboardButton('Удаление оценок')
    get_predict = types.KeyboardButton('Прогноз среднего балла')
    cancel = types.KeyboardButton('Обратно')
    markup.add(add_mark, get_mark_stat, delete_marks, get_predict, cancel)
    return markup


def delete_marks_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    one = types.KeyboardButton('Удалить одну оценку')
    all = types.KeyboardButton('Удалить все')
    cancel = types.KeyboardButton('Назад к оценкам')
    markup.add(one, all, cancel)
    return markup


def delete_one_mark_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    marks = QaDAO.get_user_marks(user_id)
    for mark in marks:
        markup.row(f'{mark["id"]} - {mark["mark"]}')
    markup.row('Назад к оценкам')
    return markup


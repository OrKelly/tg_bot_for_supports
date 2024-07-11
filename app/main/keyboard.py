from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup()
    marks = types.KeyboardButton("Оценки")
    salary_calc = types.KeyboardButton('Калькулятор зарплаты')
    markup.add(marks, salary_calc)
    return markup
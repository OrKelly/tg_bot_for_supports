import os
from typing import Union

from bs4 import BeautifulSoup, Tag
from telebot import TeleBot
from telebot.types import Message

from app.calc.constants import kpis
from app.calc.kpi import KPICalc
from app.settings.config import BASE_DIR


class Scrapy:
    FILE_DIR = os.path.join(BASE_DIR, 'media')

    def __init__(self, message: Message, bot: TeleBot):
        self.message = message
        self.bot = bot

    def get_salary(self):
        main_table = self.parse_main_table()
        coeff = dict()
        self.parse_kpis(main_table, coeff)
        self.parse_decads(main_table, coeff)
        salary = self.calc_salary(coeff)
        return salary

    def calc_salary(self, coeff: dict) -> tuple[float | int, float | int]:
        total_qa_coeff = self.get_total_qa_coeff(coeff)
        total_speed_coeff = self.get_total_speed_coeff(coeff)
        total_mins = self.get_total_mins(coeff)
        salary = total_mins * ((total_qa_coeff * 0.6 * coeff['ko']) + (total_speed_coeff * 0.4))
        pre_salary = total_mins * (total_qa_coeff * 0.6)/2
        return salary, pre_salary

    @staticmethod
    def get_total_qa_coeff(coeff: dict) -> Union[int, float]:
        total_qa_coeff = (coeff['qa'] * 0.5) + (coeff['transfers'] * 0.14) + (coeff['csat'] * 0.36)
        return total_qa_coeff

    @staticmethod
    def get_total_speed_coeff(coeff):
        total_speed_coeff = (coeff['effictiveness'] * 0.3) + (coeff['decad'] * 0.3) + (coeff['total_comm'] * 0.4)
        return total_speed_coeff

    @staticmethod
    def get_total_mins(coeff):
        total_mins = coeff['eff_time_per_2_to_17'] + coeff['eff_time_per_17_to_2'] + coeff['eff_time_vacations']
        return total_mins

    @classmethod
    def check_or_create_media_root(cls):
        if not os.path.exists(cls.FILE_DIR):
            os.mkdir(cls.FILE_DIR)

    def download_user_file(self):
        self.check_or_create_media_root()
        file_info = self.bot.get_file(self.message.document.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        with open(os.path.join(self.FILE_DIR, self.message.document.file_name), 'wb') as new_file:
            new_file.write(downloaded_file)
        self.bot.send_message(self.message.chat.id, 'Файл скачан, начинаю его обработку! '
                                                    'Пожалуйста, подождите, это может занять пару минут!')

    def parse_main_table(self):
        self.download_user_file()
        file = os.path.join(self.FILE_DIR, self.message.document.file_name)
        with open(file, encoding='utf-8') as doc:
            src = doc.read()
        parser = BeautifulSoup(src, 'lxml')
        main_table = parser.find('table', attrs={'border': 1, 'cellspacing': 0, 'cellpadding': 0})
        return main_table

    @staticmethod
    def parse_kpis(main_table: Tag, coeff: dict):
        kpi_table = main_table.find('table', attrs={'border': 0, 'cellspacing': 0, 'cellpadding': 0})
        kpi_list = kpi_table.find_all('tr')
        for kpi in kpi_list:
            kpi_text = kpi.text.replace('\n', '').split(':')
            if len(kpi_text) == 2:
                kpi_name, kpi_value = [value for value in kpi_text if value and kpi.text]
                if kpi_name in kpis.keys():
                    kpi_name = kpis.get(kpi_name)
                    coeff[kpi_name] = KPICalc(kpi=kpi_name, value=kpi_value).get_kpi_salary()

    @staticmethod
    def parse_decads(main_table: Tag, coeff: dict):
        decads_table = main_table.find('div', attrs={'align': 'center'}).find('table')
        decads = decads_table.find_all('tr')
        min_decad = 100
        for decad in decads:
            decad_percent = [value for value in decad.text.split('\n') if value][-1]
            try:
                decad_percent = float(decad_percent.replace(',', '.'))
                if decad_percent < min_decad and decad_percent != 0:
                    min_decad = decad_percent
            except ValueError:
                continue
        coeff['decad'] = KPICalc(kpi='decad', value=min_decad).get_kpi_salary()

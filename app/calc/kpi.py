import re
from typing import Union


class KPICalc:

    def __init__(self, kpi: str, value: Union[str, int, float]):
        self.kpi = kpi
        self.value = self.normalize_value(value)

    def get_kpi_salary(self):
        salary = self.get_kpi_value()
        return salary

    @property
    def get_kpi_value(self):
        kpi_method = f'_get_{self.kpi}'
        if hasattr(self, kpi_method):
            return getattr(self, kpi_method)
        raise AttributeError(f'Атрибут {kpi_method} не определен в классе KPI')

    @staticmethod
    def normalize_value(value: str) -> Union[int, float]:
        if isinstance(value, (int, float)):
            return value
        if re.fullmatch(r'\d+[.,]\d+.?', value):
            if re.fullmatch(r'\d+[.,]\d+%', value):
                return float(value.replace(',', '.').replace('%', ''))
            return float(value.replace(',', '.'))
        elif re.fullmatch(r'\d+/\d+', value):
            return int(value.split('/')[0])
        return int(value) if '-' not in value else 0

    def _get_eff_time_per_2_to_17(self) -> Union[int, float]:
        return self.value * 1.9

    def _get_eff_time_per_17_to_2(self) -> Union[int, float]:
        return self.value * 2

    def _get_eff_time_vacations(self):
        return self.value * 2

    def _get_total_comm(self):
        if 1000 <= self.value <= 1049:
            return 0.5
        elif 1050 <= self.value <= 1099:
            return 1.5
        elif 1100 <= self.value <= 1249:
            return 3
        elif 1250 <= self.value <= 1299:
            return 4
        elif self.value >= 1300:
            return 6
        return 0.5

    def _get_transfers(self):
        if self.value >= 21:
            return 0.5
        elif 18 <= self.value <= 20.99:
            return 1.5
        elif 15 <= self.value <= 17.99:
            return 3
        elif 11 <= self.value <= 14.99:
            return 4
        elif self.value < 11:
            return 6
        return 0.5

    def _get_effictiveness(self):
        if self.value < 7:
            return 0.5
        elif 7 <= self.value <= 8.99:
            return 1.5
        elif 9 <= self.value <= 10.99:
            return 3
        elif 11 <= self.value <= 12.99:
            return 4
        elif self.value >= 13:
            return 6
        return 0.5

    def _get_qa(self):
        if self.value < 70:
            return 0.5
        elif 70 <= self.value <= 84.99:
            return 1.5
        elif 85 <= self.value <= 94.99:
            return 3
        elif 95 <= self.value <= 99.99:
            return 4
        elif self.value == 100:
            return 6
        return 0.5

    def _get_csat(self):
        if self.value < 3.2:
            return 0.5
        elif 3.2 <= self.value <= 3.49:
            return 1.5
        elif 3.5 <= self.value <= 3.69:
            return 3
        elif 3.7 <= self.value <= 4.09:
            return 4
        elif self.value >= 4.1:
            return 6
        return 0.5

    def _get_ukp(self):
        return self.value * 600

    def _get_decad(self):
        if self.value < 15:
            return 0.5
        elif 15 <= self.value <= 19.99:
            return 1.5
        elif 20 <= self.value <= 29.99:
            return 3
        elif 30 <= self.value <= 34.99:
            return 4
        elif self.value >= 35:
            return 6
        return 0.5

    def _get_ko(self):
        if self.value == 0:
            return 1
        elif self.value == 1:
            return 0.2
        elif self.value == 2:
            return 0.4
        elif self.value >= 3:
            return 0.6
        return 1

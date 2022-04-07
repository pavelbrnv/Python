from dateutil.relativedelta import relativedelta
from datetime import date


def round_finance(value):
    return round(value, 2)


class PayInfo:
    def __init__(self, pay_date, pay_amount, deposit_total_amount):
        self.__pay_date = pay_date
        self.__pay_amount = pay_amount
        self.__deposit_total_amount = deposit_total_amount

    def get_pay_date(self):
        return self.__pay_date

    def get_pay_amount(self):
        return self.__pay_amount

    def get_deposit_total_amount(self):
        return self.__deposit_total_amount


class Deposit:
    def __init__(self, amount: float, percent_per_year: float, deposit_date: date):
        self.__amount = amount
        self.__percent_per_year = percent_per_year / 100
        self.__deposit_date = deposit_date

    def get_total_amount(self, term_in_months: int):
        percent_per_month = self.__percent_per_year / 12
        total_amount = self.__amount
        for month_index in range(term_in_months):
            pay_amount = round_finance(total_amount * percent_per_month)
            total_amount = round_finance(total_amount + pay_amount)
        return total_amount

    def get_total_profit(self, term_in_months: int):
        total_amount = self.get_total_amount(term_in_months)
        total_profit = total_amount - self.__amount
        return round_finance(total_profit)

    def get_pays(self, term_in_months: int, month_additional_refill: float = 0):
        percent_per_month = self.__percent_per_year / 12
        total_amount = self.__amount
        pay_date = self.__deposit_date
        pays = []
        for month_index in range(term_in_months):
            pay_date += relativedelta(months=1)
            pay_amount = round_finance(total_amount * percent_per_month)
            total_amount = round_finance(total_amount + pay_amount + month_additional_refill)
            pay = PayInfo(pay_date, pay_amount, total_amount)
            pays.append(pay)
        return pays

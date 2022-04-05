from dateutil.relativedelta import relativedelta
import calendar
from datetime import date


def round_finance(value):
    return round(value, 2)


def get_year_days_number(year):
    if calendar.isleap(year):
        return 366
    else:
        return 365


class EarlyFee:
    def __init__(self, fee_date: date, fee_amount):
        self.__fee_date = fee_date
        self.__fee_amount = fee_amount

    def get_fee_date(self):
        return self.__fee_date

    def get_fee_amount(self):
        return self.__fee_amount


class FeeInfo:
    def __init__(self, fee_date, fee_amount, debt_part, percent_part, debt_total_remainder):
        self.__fee_date = fee_date
        self.__fee_amount = fee_amount
        self.__debt_part = debt_part
        self.__percent_part = percent_part
        self.__debt_total_remainder = debt_total_remainder

    def get_fee_date(self):
        return self.__fee_date

    def get_fee_amount(self):
        return self.__fee_amount

    def get_debt_part(self):
        return self.__debt_part

    def get_percent_part(self):
        return self.__percent_part

    def get_debt_total_remainder(self):
        return self.__debt_total_remainder


class Loan:
    def __init__(self, amount, percent_per_year, term_in_months, loan_date):
        self.__amount = amount
        self.__percent_per_year = percent_per_year / 100
        self.__term_in_months = term_in_months
        self.__loan_date = loan_date
        self.__early_fees = []

    def get_month_fee(self):
        percent_per_month = self.__percent_per_year / 12
        accumulated_ratio = pow(1 + percent_per_month, self.__term_in_months)
        month_fee = (accumulated_ratio * percent_per_month) / (accumulated_ratio - 1) * self.__amount
        return round_finance(month_fee)

    def get_total_payment(self):
        total_payment = self.get_month_fee() * self.__term_in_months
        return round_finance(total_payment)

    def get_total_overpayment(self):
        total_payment = self.get_total_payment() - self.__amount
        return round_finance(total_payment)

    def get_annuity_fees(self):
        month_fee = self.get_month_fee()
        debt_remainder = self.__amount
        previous_fee_date = self.__loan_date

        fees = []
        for month_index in range(self.__term_in_months):
            fee_date = previous_fee_date + relativedelta(months=1)
            fee_delta = fee_date - previous_fee_date
            previous_fee_date = fee_date
            percent_ratio = self.__percent_per_year * fee_delta.days / get_year_days_number(fee_date.year)
            percent_amount = round_finance(percent_ratio * debt_remainder)
            debt_amount = round_finance(month_fee - percent_amount)
            debt_remainder = round_finance(debt_remainder - debt_amount)
            fee = FeeInfo(fee_date, month_fee, debt_amount, percent_amount, debt_remainder)
            fees.append(fee)
        return fees

    def add_early_fee(self, fee_date: date, fee_amount):
        early_fee = EarlyFee(fee_date, fee_amount)
        self.__early_fees.append(early_fee)

    def add_periodical_early_fees(self, first_fee_date: date, fee_amount, periods_delta: relativedelta, periods_number):
        fee_date = first_fee_date
        for i in range(periods_number):
            self.add_early_fee(fee_date, fee_amount)
            fee_date += periods_delta

    def get_annuity_daily_fees(self):
        month_fee = self.get_month_fee()
        debt_remainder = self.__amount
        previous_fee_date = self.__loan_date

        early_fees = sorted(self.__early_fees, key=lambda x: x.get_fee_date())
        early_fee_index = 0

        fees = []
        for month_index in range(1, self.__term_in_months + 1):
            if debt_remainder <= 0:
                break

            fee_date = previous_fee_date + relativedelta(months=1)
            fee_delta = fee_date - previous_fee_date

            percent_ratio = 0
            for day_index in range(1, fee_delta.days + 1):
                current_day = previous_fee_date + relativedelta(days=day_index)
                percent_ratio += self.__percent_per_year * 1 / get_year_days_number(current_day.year)

                while early_fee_index < len(early_fees) and early_fees[early_fee_index].get_fee_date() <= current_day:
                    early_fee = early_fees[early_fee_index]
                    if early_fee.get_fee_date() == current_day:
                        fee_amount = early_fee.get_fee_amount()
                        percent_amount = round_finance(percent_ratio * debt_remainder)
                        if fee_amount >= percent_amount:
                            debt_amount = round_finance(fee_amount - percent_amount)
                            debt_remainder = round_finance(debt_remainder - debt_amount)

                            if debt_remainder <= 0:
                                fee_amount = round_finance(fee_amount + debt_remainder)
                                debt_amount = round_finance(debt_amount + debt_remainder)
                                debt_remainder = 0

                            fee = FeeInfo(current_day, fee_amount, debt_amount, percent_amount, debt_remainder)
                            fees.append(fee)

                            percent_ratio = 0
                    early_fee_index += 1

            previous_fee_date = fee_date

            if debt_remainder <= 0:
                break

            percent_amount = round_finance(percent_ratio * debt_remainder)
            debt_amount = round_finance(month_fee - percent_amount)
            debt_remainder = round_finance(debt_remainder - debt_amount)

            if debt_remainder <= 0 or month_index == self.__term_in_months:
                month_fee = round_finance(month_fee + debt_remainder)
                debt_amount = round_finance(debt_amount + debt_remainder)
                debt_remainder = 0

            fee = FeeInfo(fee_date, month_fee, debt_amount, percent_amount, debt_remainder)
            fees.append(fee)
        return fees

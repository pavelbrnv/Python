from dateutil.relativedelta import relativedelta
import calendar


def round_finance(value):
    return round(value, 2)


def get_year_days_number(year):
    if calendar.isleap(year):
        return 366
    else:
        return 365


class FeeInfo:
    def __init__(self, index, fee_date, fee_amount, debt_part, percent_part, debt_total_remainder):
        self.__index = index
        self.__fee_date = fee_date
        self.__fee_amount = fee_amount
        self.__debt_part = debt_part
        self.__percent_part = percent_part
        self.__debt_total_remainder = debt_total_remainder

    def get_index(self):
        return self.__index

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
            fee = FeeInfo(month_index + 1, fee_date, month_fee, debt_amount, percent_amount, debt_remainder)
            fees.append(fee)
        return fees

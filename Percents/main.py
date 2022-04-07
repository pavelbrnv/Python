from datetime import date
from dateutil.relativedelta import relativedelta
import annuity
import deposit


def print_fee(fee: annuity.FeeInfo):
    print(
        fee.get_fee_date(),
        fee.get_fee_amount(),
        fee.get_percent_part(),
        fee.get_debt_part(),
        fee.get_debt_total_remainder()
    )


def print_all_fees(fees: list[annuity.FeeInfo]):
    index = 1
    total_fees = 0
    for fee in fees:
        print(
            index,
            fee.get_fee_date(),
            fee.get_fee_amount(),
            fee.get_percent_part(),
            fee.get_debt_part(),
            fee.get_debt_total_remainder()
        )
        total_fees += fee.get_fee_amount()
        index += 1
    print("---", "TOTAL FEES:", total_fees, "---")


def print_pay(pay: deposit.PayInfo):
    print(
        pay.get_pay_date(),
        pay.get_pay_amount(),
        pay.get_deposit_total_amount()
    )


def print_all_pays(pays: list[deposit.PayInfo]):
    index = 1
    total_pays = 0
    for pay in pays:
        print(
            index,
            pay.get_pay_date(),
            pay.get_pay_amount(),
            pay.get_deposit_total_amount()
        )
        total_pays += pay.get_pay_amount()
        index += 1
    total_refill = pays[-1].get_deposit_total_amount() - total_pays
    print("---", "TOTAL PAYS:", total_pays, "---", "TOTAL REFILL:", total_refill, "---")


def find_opti(fees: list[annuity.FeeInfo], pays: list[deposit.PayInfo]):
    fee_i = 0
    pay_i = 0

    while fees[fee_i].get_debt_total_remainder() > pays[pay_i].get_deposit_total_amount():
        if fees[fee_i].get_fee_date() <= pays[pay_i].get_pay_date():
            fee_i += 1
            if fee_i == len(fees):
                break
        else:
            pay_i += 1
            if pay_i == len(pays):
                break

    if fee_i == len(fees) or pay_i == len(pays):
        print('Sorry :( It is not your day')
    else:
        print_fee(fees[fee_i])
        print_pay(pays[pay_i])


loan = annuity.Loan(
    amount=6422721,
    percent_per_year=6.1,
    term_in_months=223,
    loan_date=date(2022, 4, 7)
)
# loan = annuity.Loan(
#     amount=6000000,
#     percent_per_year=6.1,
#     term_in_months=198,
#     loan_date=date(2022, 4, 7)
# )
# loan.add_periodical_early_fees(
#     first_fee_date=date(2022, 4, 15),
#     fee_amount=150000,
#     periods_delta=relativedelta(months=1),
#     periods_number=240
# )

deposit = deposit.Deposit(
    amount=500000,
    percent_per_year=12,
    deposit_date=date(2022, 4, 7)
)

loan_fees = loan.get_annuity_daily_fees()
deposit_pays = deposit.get_pays(term_in_months=60, month_additional_refill=150000)

find_opti(loan_fees, deposit_pays)

print()

print_all_fees(loan_fees)
#print_all_pays(deposit_pays)

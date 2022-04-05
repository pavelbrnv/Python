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
    print("---", "TOTAL FEES: ", total_fees, "---")


def print_pay(pay: deposit.PayInfo):
    print(
        pay.get_index(),
        pay.get_pay_date(),
        pay.get_pay_amount(),
        pay.get_pays_total_amount(),
        pay.get_deposit_total_amount()
    )


loan1 = annuity.Loan(
    amount=6422721,
    percent_per_year=6.1,
    term_in_months=223,
    loan_date=date(2022, 3, 19)
)
loan1.add_periodical_early_fees(
    first_fee_date=date(2022, 4, 15),
    fee_amount=100000,
    periods_delta=relativedelta(months=1),
    periods_number=240
)

deposit = deposit.Deposit(
    amount=50000,
    percent_per_year=21,
    deposit_date=date(2022, 4, 5)
)

loan_fees = loan1.get_annuity_daily_fees()
print_all_fees(loan_fees)

# deposit_pays = deposit.get_pays(term_in_months=3)

# for pay in deposit_pays:
#     print_pay(pay)

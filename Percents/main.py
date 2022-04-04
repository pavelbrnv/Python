from datetime import date
import annuity
import deposit


def print_fee(fee):
    print(
        fee.get_index(),
        fee.get_fee_date(),
        fee.get_fee_amount(),
        fee.get_percent_part(),
        fee.get_debt_part(),
        fee.get_debt_total_remainder()
    )


def print_pay(pay):
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
early_fee1 = annuity.EarlyFee(
    fee_date=date(2024, 3, 5),
    fee_amount=1000000
)
early_fee2 = annuity.EarlyFee(
    fee_date=date(2026, 5, 18),
    fee_amount=500000
)
loan1.add_early_fee(early_fee1)
loan1.add_early_fee(early_fee2)

deposit = deposit.Deposit(
    amount=2000000,
    percent_per_year=12,
    deposit_date=date(2022, 3, 19)
)

period = 36

loan1_pays = loan1.get_annuity_fees()
loan2_pays = loan1.get_annuity_daily_fees()

# for pay in loan1_pays:
#     print_fee(pay)

print()

for pay in loan2_pays:
    print_fee(pay)

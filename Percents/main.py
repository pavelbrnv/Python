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
loan2 = annuity.Loan(
    amount=6122721,
    percent_per_year=6.1,
    term_in_months=223,
    loan_date=date(2022, 3, 19)
)

deposit = deposit.Deposit(
    amount=300000,
    percent_per_year=20,
    deposit_date=date(2022, 3, 19)
)

loan1_pays = loan1.get_annuity_fees()
loan2_pays = loan2.get_annuity_fees()
deposit_fees = deposit.get_pays(4)

dd = loan1_pays[3].get_debt_total_remainder() - loan2_pays[3].get_debt_total_remainder()

print_fee(loan1_pays[3])
print_fee(loan2_pays[3])
print(dd)
print_pay(deposit_fees[3])




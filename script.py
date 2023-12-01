# Testing AceBank Class in src/AceBank
import logging
logging.basicConfig(filename='script.log', encoding='utf-8', level=logging.DEBUG)

from src.AceBank import AceBank

if __name__ == '__main__':
    # initiate AceBank with customer id 234
    ab = AceBank()
    # setup account for customer 234
    ab.create_account(account_number='0808', balance=1000.00, customer_id=234)
    # deposit money for account 0808
    ab.deposit_fund('0808', 500.00, 'usdollars', 234)

    # withdraw from account 0808
    ab.withdraw_funds('0808', 100.00, 'caddollars', 234)

    # get balance from account 0808
    balance = ab.get_balance('0808', 234)
    logging.info(f"Balance of account 0808 after last transaction is {balance}")

    # initiate AceBank with customer id 756
    ab = AceBank()
    # setup accounts for customer 756
    ab.create_account(account_number='0903', balance=100.00, customer_id=756)
    ab.create_account(account_number='0875', balance=6000.00, customer_id=756)

    # withdraw from account 0875
    ab.withdraw_funds('0875', 700.00, 'usdollars', 756)
    # deposit fund to 0903
    ab.deposit_fund('0903', 2500.00, 'euros', 756)

    # transfer fund from 0875 to 0903
    ab.transfer_funds('0875', '0903', 1100.00, 756, 756)

    # get balance from account 0808
    balance_0875 = ab.get_balance('0875', 756)
    balance_0903 = ab.get_balance('0903', 756)
    logging.info(f"Balance of account 0875 after last transaction is {balance_0875}")
    logging.info(f"Balance of account 0903 after last transaction is {balance_0903}")

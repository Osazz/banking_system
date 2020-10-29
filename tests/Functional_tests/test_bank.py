"""
This is a functional test of the scenarios A and B
"""
import pytest
from AceBank import AceBank


@pytest.fixture
def setup_case_a():
    ab = AceBank()
    # setup account for customer 234
    ab.create_account(account_number='0808', balance=1000.00, customer_id=234)
    return ab


@pytest.fixture
def setup_case_b():
    ab = AceBank()
    # setup account for customer 756
    ab.create_account(account_number='0903', balance=100.00, customer_id=756)
    ab.create_account(account_number='0875', balance=6000.00, customer_id=756)
    return ab


class TestCases(object):

    def test_case_a(self, setup_case_a):
        # deposit money for account 0808
        setup_case_a.deposit_fund('0808', 500.00, 'usdollars', 234)

        # withdraw from account 0808
        setup_case_a.withdraw_funds('0808', 100.00, 'caddollars', 234)

        # get balance from account 0808
        balance = setup_case_a.get_balance('0808', 234)
        print(f"Balance of account 0808 after last transaction is {balance}")
        assert balance == 1650.00

    def test_case_b(self, setup_case_b):
        # withdraw from account 0875
        setup_case_b.withdraw_funds('0875', 700.00, 'usdollars', 756)
        # deposit fund to 0903
        setup_case_b.deposit_fund('0903', 2500.00, 'euros', 756)

        # transfer fund from 0875 to 0903
        setup_case_b.transfer_funds('0903', '0875', 1100.00, 756, 756)

        # get balance from account 0808
        balance_0875 = setup_case_b.get_balance('0875', 756)
        balance_0903 = setup_case_b.get_balance('0903', 756)
        print(f"Balance of account 0875 after last transaction is "
              f"{balance_0875}")
        print(f"Balance of account 0903 after last transaction is "
              f"{balance_0903}")
        assert balance_0875 == 3850.0
        assert balance_0903 == 6200.0


if __name__ == '__main__':
    pytest.main()

"""
Unit test for AceBank class and all the functions in it
"""
import pytest
from AceBank import AceBank, validate_balance, validate_variable,\
    currency_converter

ACCEPTED_CURRENCY = ['usdollars', 'euros', 'caddollars']


@pytest.fixture
def mock_bank():
    account_details = [
        {'account_number': '8012', 'balance': 1000.00, 'customer_id': 250},
        {'account_number': '7095', 'balance': 32500.95, 'customer_id': 250},
        {'account_number': '4000', 'balance': 350.10, 'customer_id': 650}
    ]

    ab = AceBank()
    ab.account_details = account_details
    return ab


class TestAceBank(object):

    def test_create_account(self, ace_bank):
        """
        This test creates an account function
        """
        ace_bank.create_account('0912', '10000')
        count, account = ace_bank.validate_account('0912')
        assert count == 0
        assert account['account_number'] == '0912'
        assert account['balance'] == 10000.0
        assert account['customer_id'] == 50

    def test_get_balance(self, ace_bank):
        # test no account
        with pytest.raises(ValueError) as noaccount:
            ace_bank.get_balance('1010')
        assert "Account number 1010 does not exist" in str(noaccount.value)

        # do proper testing to get balance
        ace_bank.create_account('08912', '10000.0')
        acct_balance = ace_bank.get_balance('08912')
        assert acct_balance == 10000.0

    def test_deposit_fund(self, mock_bank):
        # test deposit fund by using us dollars
        assert mock_bank.account_details[0]['balance'] == 1000.00
        mock_bank.deposit_fund('8012', 200.00, 'usdollars')
        assert mock_bank.account_details[0]['balance'] == 1300.00

        # test deposit fund using euros
        assert mock_bank.account_details[0]['balance'] == 1300.00
        mock_bank.deposit_fund('8012', 200.00, 'euros')
        assert mock_bank.account_details[0]['balance'] == 1700.00

        # test deposit fund using cad
        assert mock_bank.account_details[0]['balance'] == 1700.00
        mock_bank.deposit_fund('8012', 200.00, 'caddollars')
        assert mock_bank.account_details[0]['balance'] == 1900.00

    def test_withdraw_funds(self, mock_bank):
        # test deposit fund using euros
        assert mock_bank.account_details[0]['balance'] == 1000.00
        mock_bank.withdraw_funds('8012', 200.00, 'euros')
        assert mock_bank.account_details[0]['balance'] == 600.00

        # test deposit fund by using us dollars
        assert mock_bank.account_details[2]['balance'] == 350.10
        mock_bank.withdraw_funds('4000', 200.00, 'usdollars')
        assert mock_bank.account_details[2]['balance'] == 50.10

        # test deposit fund by using us dollars
        assert mock_bank.account_details[1]['balance'] == 32500.95
        mock_bank.withdraw_funds('7095', 2593.75, 'caddollars')
        assert mock_bank.account_details[1]['balance'] == 29907.20

    def test_transfer_fund(self, mock_bank):
        # confirm how much was in each account before transfer
        assert mock_bank.account_details[1]['balance'] == 32500.95
        assert mock_bank.account_details[0]['balance'] == 1000.00
        # make transfer
        mock_bank.transfer_funds('7095', '8012', 2000.00)
        # confirm changes
        assert mock_bank.account_details[1]['balance'] == 30500.95
        assert mock_bank.account_details[0]['balance'] == 3000.00

    def test_validate_account(self, mock_bank):
        # test account that dosnt exist
        assert not mock_bank.validate_account('1010')

        # test account that exist
        assert mock_bank.validate_account('4000')

        # test variables returned by validate_account
        counter, account = mock_bank.validate_account('4000')
        assert counter == 2
        assert account['account_number'] == '4000'
        assert account['balance'] == 350.10
        assert account['customer_id'] == 650

    def test_get_biggest_id(self, mock_bank):
        # test next id generated
        assert AceBank().get_biggest_id() == 50

        # test id generated when no bank account exist
        assert mock_bank.get_biggest_id() == 700

    def test_validate_balance(self):
        # test when account_balance is greater than amount
        assert validate_balance(1000, 400)

        # test when account_balance is equal amount
        assert validate_balance(400, 400)

        # test when account_balance is less than amount
        with pytest.raises(ValueError) as lowbalance:
            validate_balance(300, 400)
        assert "Account balance of 300 is currently lesser than 400" in \
               str(lowbalance.value)

    @pytest.mark.parametrize('account_number, amount, currency, '
                             'outgoing_account_number',
                             [(200.00, 200, 1, 854.2),
                              (200, 'error', 'cad', 2)])
    def test_validate_variable(self, account_number, amount, currency,
                               outgoing_account_number):

        # test when account_number
        with pytest.raises(ValueError) as wrongvariable:
            validate_variable(account_number=account_number)
        assert f"Account number {account_number} must be string" \
               in str(wrongvariable.value)

        # test when amount
        with pytest.raises(ValueError) as wrongvariable:
            validate_variable(amount=amount)
        assert f"Amount must be of type float" in str(wrongvariable.value)

        # test when currency
        with pytest.raises(ValueError) as wrongvariable:
            validate_variable(currency=currency)
        assert f"Currency {currency} is not recognized. Should be one of " \
               f"{ACCEPTED_CURRENCY}" in str(wrongvariable.value)

        # test when outgoing_account_number
        with pytest.raises(ValueError) as wrongvariable:
            validate_variable(outgoing_account_number=outgoing_account_number)
        assert f"Account number {outgoing_account_number} must be string" \
               in str(wrongvariable.value)

    def test_currency_converter(self):
        # test converting us dollars to cad
        assert currency_converter(100, 'usdollars') == 150

        # test converting euros to cad
        assert currency_converter(100, 'euros') == 200


if __name__ == '__main__':
    pytest.main()

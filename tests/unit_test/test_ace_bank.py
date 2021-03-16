"""
Unit test for AceBank class and all the functions in it
"""
import pytest
from src.AceBank import AceBank

ACCEPTED_CURRENCY = ['usdollars', 'euros', 'caddollars']


@pytest.fixture
def mock_bank():
    account_details = {
        250: {
            '8012': {
                'balance': 1000.00
            },
            '7095': {
                'balance': 32500.95
            }
        },
        650: {
            '4000': {
                'balance': 350.10
            }
        }
    }

    ab = AceBank()
    ab.account_details = account_details
    return ab


class TestAceBank(object):

    def test_create_account(self, ace_bank):
        """
        This test creates an account function
        """
        ace_bank.create_account('0912', '10000', 50)
        ace_bank.validate_account('0912', 50)
        assert ace_bank.account_details == {50: {"0912": {'balance': 10000}}}
        assert ace_bank.account_details[50] == {"0912": {'balance': 10000}}
        assert ace_bank.account_details[50]['0912'] == {'balance': 10000}

    def test_get_balance(self, ace_bank):
        # test no account
        with pytest.raises(ValueError) as noaccount:
            ace_bank.get_balance('1010', 50)
        assert "Account does not exist" in str(noaccount.value)

        # do proper testing to get balance
        ace_bank.create_account('08912', '10000.0', 50)
        acct_balance = ace_bank.get_balance('08912', 50)
        assert acct_balance == 10000.0

    def test_deposit_fund(self, mock_bank):
        # test deposit fund by using us dollars
        assert mock_bank.account_details[250]['8012']['balance'] == 1000.00
        mock_bank.deposit_fund('8012', 200.00, 'usdollars', 250)
        assert mock_bank.account_details[250]['8012']['balance'] == 1300.00

        # test deposit fund using euros
        assert mock_bank.account_details[250]['8012']['balance'] == 1300.00
        mock_bank.deposit_fund('8012', 200.00, 'euros', 250)
        assert mock_bank.account_details[250]['8012']['balance'] == 1700.00

        # test deposit fund using cad
        assert mock_bank.account_details[250]['8012']['balance'] == 1700.00
        mock_bank.deposit_fund('8012', 200.00, 'caddollars', 250)
        assert mock_bank.account_details[250]['8012']['balance'] == 1900.00

    def test_withdraw_funds(self, mock_bank):
        # test deposit fund using euros
        assert mock_bank.account_details[250]['8012']['balance'] == 1000.00
        mock_bank.withdraw_funds('8012', 200.00, 'euros', 250)
        assert mock_bank.account_details[250]['8012']['balance'] == 600.00

        # test deposit fund by using us dollars
        assert mock_bank.account_details[650]['4000']['balance'] == 350.10
        mock_bank.withdraw_funds('4000', 200.00, 'usdollars', 650)
        assert mock_bank.account_details[650]['4000']['balance'] == 50.10

        # test deposit fund by using us dollars
        assert mock_bank.account_details[250]['7095']['balance'] == 32500.95
        mock_bank.withdraw_funds('7095', 2593.75, 'caddollars', 250)
        assert mock_bank.account_details[250]['7095']['balance'] == 29907.20

    def test_transfer_fund(self, mock_bank):
        # confirm how much was in each account before transfer
        assert mock_bank.account_details[250]['7095']['balance'] == 32500.95
        assert mock_bank.account_details[250]['8012']['balance'] == 1000.00
        # make transfer
        mock_bank.transfer_funds('8012', '7095', 2000.00, 250, 250)
        # confirm changes
        assert mock_bank.account_details[250]['7095']['balance'] == 30500.95
        assert mock_bank.account_details[250]['8012']['balance'] == 3000.00

    def test_validate_account(self, mock_bank):
        # test account that dosnt exist
        with pytest.raises(ValueError) as va:
            mock_bank.validate_account('1010', 250)
        assert "Account does not exist" in str(va.value)

        # test account that exist
        mock_bank.validate_account('4000', 650)

    def test_validate_balance(self):
        # test when account_balance is greater than amount
        AceBank().validate_balance(1000, 400)

        # test when account_balance is equal amount
        AceBank().validate_balance(400, 400)

        # test when account_balance is less than amount
        with pytest.raises(ValueError) as lowbalance:
            AceBank().validate_balance(300, 400)
        assert "Account balance of 300 is currently lesser than 400" in \
               str(lowbalance.value)

    @pytest.mark.parametrize('account_number, amount, currency, '
                             'outgoing_acct_num',
                             [(200.00, 200, 1, 854.2),
                              (200, 'error', 'cad', 2)])
    def test_validate_variable(self, account_number, amount, currency,
                               outgoing_acct_num):
        ac = AceBank()
        # test when account_number
        with pytest.raises(ValueError) as wrongvariable:
            ac.validate_variable(account_number=account_number)
        assert f"Account number {account_number} must be string" \
               in str(wrongvariable.value)

        # test when amount
        with pytest.raises(ValueError) as wrongvariable:
            ac.validate_variable(amount=amount)
        assert f"Amount must be of type float" in str(wrongvariable.value)

        # test when currency
        with pytest.raises(ValueError) as wrongvariable:
            ac.validate_variable(currency=currency)
        assert f"Currency {currency} is not recognized. Should be one of " \
               f"{ACCEPTED_CURRENCY}" in str(wrongvariable.value)

        # test when outgoing_account_number
        with pytest.raises(ValueError) as wrongvariable:
            ac.validate_variable(outgoing_account_number=outgoing_acct_num)
        assert f"Account number {outgoing_acct_num} must be string" \
               in str(wrongvariable.value)

    def test_currency_converter(self):
        ac = AceBank()
        # test converting us dollars to cad
        assert ac.currency_converter(100, 'usdollars') == 150

        # test converting euros to cad
        assert ac.currency_converter(100, 'euros') == 200


if __name__ == '__main__':
    pytest.main()

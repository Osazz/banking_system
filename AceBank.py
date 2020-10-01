ACCEPTED_CURRENCY = ['usdollars', 'euros', 'caddollars']


class AceBank(object):
    def __init__(self, customer_id=None):
        # keeping account info in a list
        self.account_details = []

        self.customer_id = customer_id
        if not self.customer_id:
            self.customer_id = self.get_biggest_id()

    def create_account(self, account_number, balance):
        # This creates new customer account and add info to account details
        # todo: confirm that account number is int and balance is int or float
        if self.validate_account(account_number):
            raise ValueError(f"Account number {account_number} already exist ")
        self.account_details.append({'account_number': account_number,
                                     'balance': float(balance),
                                     'customer_id': int(self.customer_id)})

    def get_balance(self, account_number):
        if not self.validate_account(account_number):
            raise ValueError(f"Account number {account_number} does not exist")
        for account in self.account_details:
            if account_number == account['account_number']:
                return account['balance']

    def deposit_fund(self, account_number, amount, currency):
        validate_variable(currency=currency)
        amount = currency_converter(amount, currency)
        account_location, account = self.validate_account(account_number)
        self.account_details[account_location]['balance'] = \
            account['balance'] + amount

    def withdraw_funds(self, account_number, amount, currency):
        validate_variable(account_number=account_number, amount=amount,
                          currency=currency)
        account_location, account = self.validate_account(account_number)
        amount = currency_converter(amount, currency)
        self.account_details[account_location]['balance'] = \
            round(account['balance'] - amount, 2)

    def transfer_funds(self, account_number, outgoing_account_number, amount):
        validate_variable(account_number=account_number, amount=amount,
                          outgoing_account_number=outgoing_account_number)
        sender_account_location, sender_account = \
            self.validate_account(account_number)
        receiver_account_location, receiver_account = \
            self.validate_account(outgoing_account_number)
        validate_balance(sender_account['balance'], amount)

        # remove amount from sender's account
        self.account_details[sender_account_location]['balance'] = \
            sender_account['balance'] - amount

        # send amount to new account
        self.account_details[receiver_account_location]['balance'] = \
            receiver_account['balance'] + amount

    def validate_account(self, account_number):
        # this validates that an account exist or not
        # if account exist returns account information
        # if account dose not exist return false
        for counter, account in enumerate(self.account_details):
            if account_number == account['account_number']:
                return counter, account
        return False

    def get_biggest_id(self):
        # this returns the largest number for customer id plus 50
        current_ids = []
        for account in self.account_details:
            current_ids.append(account['customer_id'])
        if current_ids:
            return sorted(current_ids)[-1] + 50
        return 50


def validate_balance(account_balance, amount):
    if account_balance >= amount:
        return True
    raise ValueError(f"Account balance of {account_balance} is "
                     f"currently lesser than {amount}")


def validate_variable(account_number=None, amount=None, currency=None,
                      outgoing_account_number=None):
    if account_number and not isinstance(account_number, str):
        raise ValueError(f"Account number {account_number} must be string")
    if amount and not isinstance(amount, float):
        raise ValueError(f"Amount must be of type float")
    if currency and currency not in ACCEPTED_CURRENCY:
        raise ValueError(f"Currency {currency} is not recognized. Should be"
                         f" one of {ACCEPTED_CURRENCY}")
    if outgoing_account_number and not isinstance(outgoing_account_number,
                                                  str):
        raise ValueError(f"Account number {outgoing_account_number}"
                         f" must be string")


def currency_converter(amount, currency):
    if currency.lower() == 'usdollars':
        amount = float(amount * 1.50)

    if currency.lower() == 'euros':
        amount = float(amount * 2.00)
    return amount


if __name__ == '__main__':
    # initiate AceBank with customer id 234
    ab = AceBank(customer_id=234)
    # setup account for customer 234
    ab.create_account(account_number='0808', balance=1000.00)
    # deposit money for account 0808
    ab.deposit_fund('0808', 500.00, 'usdollars')

    # withdraw from account 0808
    ab.withdraw_funds('0808', 100.00, 'caddollars')

    # get balance from account 0808
    balance = ab.get_balance('0808')
    print(f"Balance of account 0808 after last transaction is {balance}")

    # initiate AceBank with customer id 756
    ab = AceBank(customer_id=756)
    # setup accounts for customer 756
    ab.create_account(account_number='0903', balance=100.00)
    ab.create_account(account_number='0875', balance=6000.00)

    # withdraw from account 0875
    ab.withdraw_funds('0875', 700.00, 'usdollars')
    # deposit fund to 0903
    ab.deposit_fund('0903', 2500.00, 'euros')

    # transfer fund from 0875 to 0903
    ab.transfer_funds('0875', '0903', 1100.00)

    # get balance from account 0808
    balance_0875 = ab.get_balance('0875')
    balance_0903 = ab.get_balance('0903')
    print(f"Balance of account 0875 after last transaction is {balance_0875}")
    print(f"Balance of account 0903 after last transaction is {balance_0903}")

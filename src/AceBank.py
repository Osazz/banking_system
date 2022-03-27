# Account simulation

import os
import sys
import logging
import collections

ACCEPTED_CURRENCY = ['usdollars', 'euros', 'caddollars']

logging.basicConfig(
    filename="artifactory.logs",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %p",
)


class AceBank(object):
    def __init__(self):
        # keeping account info in a list
        self.account_details = collections.defaultdict(dict)
        self.log = logging.getLogger(os.path.basename(sys.argv[0]))

    def create_account(self, account_number, balance, customer_id):
        # This creates new customer account and add info to account details
        try:
            if self.validate_account(account_number, customer_id):
                raise Exception(f"Account does not exist")
        except ValueError:
            self.log.warning(F"We expect account should not exist so cont.")
        self.account_details[customer_id][account_number] = \
            {'balance': float(balance)}

    def get_balance(self, account_number, customer_id):
        self.validate_account(account_number, customer_id)
        current_acct = self.account_details[customer_id][account_number]
        return current_acct['balance']

    def deposit_fund(self, account_number, amount, currency, customer_id):
        self.validate_variable(currency=currency)
        amount = self.currency_converter(amount, currency)
        self.validate_account(account_number, customer_id)
        self.account_details[customer_id][account_number]['balance'] = \
            self.account_details[customer_id][account_number]['balance'] \
            + amount

    def withdraw_funds(self, account_number, amount, currency, customer_id):
        self.validate_variable(account_number=account_number, amount=amount,
                               currency=currency)
        self.validate_account(account_number, customer_id)
        amount = self.currency_converter(amount, currency)
        self.account_details[customer_id][account_number]['balance'] = \
            round(self.account_details[customer_id][account_number]
                  ['balance'] - amount, 2)

    def transfer_funds(self, receivers_account_number, senders_account_number,
                       amount, receivers_customer_id, senders_customer_id):
        self.validate_variable(account_number=receivers_account_number,
                               amount=amount,
                               outgoing_account_number=senders_account_number)
        self.validate_account(senders_account_number, senders_customer_id)
        self.validate_account(receivers_account_number, receivers_customer_id)
        self.validate_balance(self.account_details[senders_customer_id]
                              [senders_account_number]['balance'], amount)

        # remove amount from sender's account
        self.account_details[senders_customer_id][senders_account_number]['balance'] = \
            self.account_details[senders_customer_id][senders_account_number]['balance'] \
            - amount

        # send amount to new account
        self.account_details[receivers_customer_id][receivers_account_number]['balance'] = \
            self.account_details[receivers_customer_id][receivers_account_number]['balance']\
            + amount

    def validate_account(self, account_number, customer_id):
        # this validates that an account exist or not
        # if account exist returns account information
        # if account dose not exist return false
        try:
            if self.account_details[customer_id][account_number]:
                self.log.info("Account exists")
        except KeyError:
            raise ValueError(f"Account does not exist")

    @staticmethod
    def validate_balance(account_balance, amount):
        if account_balance < amount:
            raise ValueError(f"Account balance of {account_balance} is "
                             f"currently lesser than {amount}")

    @staticmethod
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

    @staticmethod
    def currency_converter(amount, currency):
        if currency.lower() == 'usdollars':
            amount = float(amount * 1.50)

        if currency.lower() == 'euros':
            amount = float(amount * 2.00)
        return amount

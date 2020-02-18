from bankr.errors.not_found import BankNotFoundError
from bankr.models.account import Account
from bankr.models.bank import Bank
from peewee import fn

from back.bankr.models.transaction import Transaction


def get_accounts(bank=None, name=None, db_user=None):
    accounts = Account.select()
    if name is not None:
        accounts = accounts.where(Account.label.contains(name))

    if db_user is not None:
        accounts = accounts.where(Account.user == db_user)

    if bank is not None:
        db_bank = Bank.get_or_none(name=bank)
        if db_bank is None:
            raise BankNotFoundError(bank)

        accounts = accounts.where(Account.bank == db_bank)

    return accounts


def get_accounts_types(bank=None, db_user=None):
    accounts_types = Account.select(fn.Distinct(Account.label.strip(Account.account_id)))

    if db_user is not None:
        accounts_types = accounts_types.where(Account.user == db_user)

    if bank is not None:
        db_bank = Bank.get_or_none(name=bank)
        if db_bank is None:
            raise BankNotFoundError(bank)

        accounts_types = accounts_types.where(Account.bank == db_bank)

    return [account.strip("()") for account in accounts_types]


def get_transactions_by_account_type(account_type, bank=None, db_user=None):
    transactions = (Transaction.select()
                    .join(Account)
                    .where(Account.label.contains(account_type)))
    if db_user is not None:
        transactions = transactions.where(Account.user == db_user)

    if bank is not None:
        db_bank = Bank.get_or_none(name=bank)
        if db_bank is None:
            raise BankNotFoundError(bank)

        transactions = transactions.where(Account.bank == db_bank)

    return transactions
def get_accounts_transactions_by_types(bank=None, db_user=None):
    accounts_types = get_accounts_types(bank, db_user)
    transactions_by_types = []
    for account in accounts_types:
        p = {account: get_account_type_transactions(account, bank, db_user)}
        transactions_by_types.append(p)
    return transactions_by_types

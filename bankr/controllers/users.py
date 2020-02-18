import json

from bankr.errors.not_found import UserNotFoundError, BankNotFoundError
from bankr.models.user import User
from peewee import fn

from back.bankr.errors.not_found import BankNotFoundError, AccountNotFoundError
from back.bankr.models.account import Account
from back.bankr.models.bank import Bank
from back.bankr.models.transaction import Transaction


def get_user(user_name=None):
    users = User.select(User.username)
    print(user_name)
    print(users)
    if user_name is not None:
        users = users.where(User.username == user_name)
        print(users)
        if users is None:
            raise UserNotFoundError(user_name)

    return [user.get_small_data() for user in users]


def get_user_accounts(user_name, bank=None):
    db_user = User.get_or_none(username=user_name)
    if db_user is None:
        raise UserNotFoundError(user_name)
    else:
        accounts = Account.select().where(Account.user == db_user.id)
        print(accounts)
        if bank is not None:
            db_bank = Bank.get_or_none(name=bank)
            if db_bank is None:
                raise BankNotFoundError(bank)
            else:
                accounts = accounts.where(Account.bank == db_bank.id)
        return [account.get_small_data() for account in accounts]


def get_user_budget(user_name, bank=None):
    accounts = get_user_accounts(user_name, bank)
    return {"budget": sum([account["balance"] for account in accounts])}


def get_user_transactions(user_name, bank=None, account=None, limits=None):
    db_user = User.get_or_none(username=user_name)
    if db_user is None:
        raise UserNotFoundError(user_name)
    else:
        transactions = (Transaction.select()
                        .join(Account)
                        .join(User, on=(User.id == Account.user_id))
                        .where(User.username == user_name)
                        .order_by(Transaction.date))
        if bank is not None:
            db_bank = Bank.get_or_none(name=bank)
            if db_bank is None:
                raise BankNotFoundError(bank)
            else:
                transactions = transactions.where(Account.bank.id == db_bank.id)
        if account is not None:
            db_account = Account.select().where(Account.label.contains(account))
            if len(db_account) == 0:
                raise AccountNotFoundError
            else:
                transactions = transactions.where(Account.label.contains(account))
        if limits is not None:
            transactions = transactions.limit(limits)
        return [transaction.get_small_data() for transaction in transactions]

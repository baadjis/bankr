from bankr.errors.not_found import BankNotFoundError
from bankr.models.account import Account
from bankr.models.bank import Bank
from peewee import fn

from back.bankr.models.transaction import Transaction
from back.bankr.models.user import User


def get_banks(bank_name=None):
    banks = Bank.select()
    if bank_name is not None:
        db_bank = Bank.get_or_none(name=bank_name)
        if db_bank is None:
            raise BankNotFoundError(bank_name)
        else:
            return [db_bank.get_small_data()]
    return [bank.get_small_data() for bank in banks]


def get_bank_accounts(bank_name=None):
    banks = get_banks(bank_name)
    if banks:
        if bank_name is not None:
            account= Account.select().where(Account.bank.name == bank_name)
            return account.get_small_data()
        else:
            accounts = []
            for bank in banks:
                this_bank=get_banks(bank["name"])[0]
                account_selected=Account.select().where(Account.bank== this_bank["id"])
                print(account_selected)
                p = {bank["name"]: [account.get_small_data() for account in account_selected]}
                accounts.append(p)
            return accounts


def get_bank_users(bank_name=None):
    nb_users = (User.select(fn.count(fn.Distinct(User.id)) , Bank.name)
                .join(Account,on=(User.id==Account.user_id))
                .join(Bank)
                .group_by(Bank)
                )

    if bank_name is not None:
        db_bank = Bank.get_or_none(name=bank_name)
        if db_bank is None:
            raise BankNotFoundError(bank_name)
        else:
            nb_users = nb_users.where(Bank.name == bank_name)
            print(nb_users)

    return [{"name":nb_user.account.bank.name,"number of users":nb_user.count}for nb_user in nb_users]


def get_bank_transactions(bank_name=None):
    transactions = (Transaction.select(fn.COUNT(fn.Distinct(Transaction.id)), fn.sum(Transaction.amount),Bank.name)
                    .join(Account,on=(Transaction.account_id == Account.id))
                    .join(Bank)
                    .group_by(Bank.name))
    if bank_name is not None:
        db_bank = Bank.get_or_none(name=bank_name)
        if db_bank is None:
            raise BankNotFoundError(bank_name)
        else:
            transactions = transactions.where(Bank.name == bank_name)
    return [{"name":transaction.account.bank.name,"number of transactions":transaction.count,"total amount":transaction.sum} for transaction in transactions]

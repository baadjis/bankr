from weboob.capabilities.bank import CapBank
from weboob.core import Weboob

from bankr.core import logger
from bankr.models.account import Account
from bankr.models.bank import Bank
from bankr.models.transaction import Transaction
from . import celery


@celery.task

def retrieve_accounts(bank_name):
    w = Weboob()
    w.load_backends(caps=(CapBank,))
    bank_backend = w.get_backend(bank_name)
    if bank_backend:
        bank = Bank.get_or_create(name = bank_name)
        accounts = bank_backend.iter_accounts()
        for account in accounts:
            logger.info(f'[Accounts] Retrieving account {account.label} - {account.balance} from {bank_name}')

            db_account = Account.get_or_none(bank=bank[0], account_id=account.id)
            if db_account is None:
                db_account = Account.create(bank=bank[0], account_id=account.id, user=1, label=account.label,
                                            balance=account.balance)
            else:
                db_account.label = account.label
                db_account.balance = account.balance
                db_account.save()
            transactions=bank_backend.iter_history(account)
            for transaction in transactions:
                db_transanction=Transaction.get_or_create(account=db_account.id,label=transaction.label,category=transaction.category,amount=transaction.amount,date=transaction.date)

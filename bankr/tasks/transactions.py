from weboob.capabilities.bank import CapBank
from weboob.core import Weboob

from bankr.core import logger
from bankr.models.account import Account
from bankr.models.transactions import Transaction

from bankr.models.bank import Bank
from . import celery
def retrieve_transactions(bank_id):

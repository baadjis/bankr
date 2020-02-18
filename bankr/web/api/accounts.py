from flask import request
from flask_restful import Resource

from back.bankr.controllers.accounts import get_transactions_by_account_type, get_accounts_types,get_accounts


class Accounts(Resource):
    def get(self):
        bank = request.args.get('bank',None)
        name=request.args.get('name',None)
        types=request.args.get('types',False)
        accounts_transactions_by_types=request.args.get('bytypes',False)
        account_type=request.args.get('account_type',None)
        if not (accounts_transactions_by_types or types):
            accounts = [account.get_small_data() for account in get_accounts(bank,name)]
            return accounts
        elif types:
            accoun_types=get_accounts_types(bank)
            return accoun_types
        elif accounts_transactions_by_types:
            transactions_by_types=get_transactions_by_account_type(account_type,bank)
            return transactions_by_types



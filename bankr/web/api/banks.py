from flask import request
from flask_restful import Resource

from back.bankr.controllers.banks import get_bank_accounts,get_banks,get_bank_transactions,get_bank_users


class Banks(Resource):
    def get(self):
        bank=request.args.get('bank',None)
        query=request.args.get('query',None)
        if query=='accounts':
            return get_bank_accounts(bank)
        if query=='nb_users':
            return get_bank_users(bank)
        if query=='transactions':
            return get_bank_transactions(bank)
        return get_banks(bank)


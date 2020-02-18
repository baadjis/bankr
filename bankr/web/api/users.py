from flask import request
from flask_restful import Resource

from back.bankr.controllers.users import get_user_accounts,get_user,get_user_budget,get_user_transactions


class Users(Resource):
    def get(self):
        user_name = request.args.get('user')
        print(str(user_name))
        query=request.args.get('query')
        print(query)
        bank = request.args.get('bank')
        print(bank)
        if query=='accounts':
            return get_user_accounts(user_name,bank)
        if query== 'budget':
            return get_user_budget(user_name,bank)
        if query=='transactions':
            limit=request.args.get('limit',10)
            account=request.args.get('account')
            return get_user_transactions(user_name,bank,account,limit)
        return get_user(user_name)

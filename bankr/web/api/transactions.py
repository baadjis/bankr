from flask import request
from flask_restful import Resource
from datetime import datetime

from back.bankr.controllers.transactions import get_transactions


class Transactions(Resource):
    def get(self):
        query=request.args.get('query',None)
        date_since=request.args.get('since',None)
        since=datetime.date(date_since) if date_since else date_since
        limit=request.args.get('limit',10)
        transactions=get_transactions(query,since,limit)
        return transactions

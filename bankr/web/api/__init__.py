
from flask import Blueprint
from flask_restful import Api

from bankr.core import db
from .accounts import Accounts
from .transactions import Transactions
from .tasks import SyncWeboob
from .users import Users
from .banks import Banks
from .. import app

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_request
def before_request():
    db.connect(reuse_if_open=True)
    pass


@api_bp.teardown_request
def after_request(exception=None):
    db.close()


api.add_resource(Accounts, '/accounts')
api.add_resource(Transactions, '/transactions')
api.add_resource(Users,'/users')
api.add_resource(Banks,'/banks')

api.add_resource(SyncWeboob, '/syncweboob')


app.register_blueprint(api_bp, url_prefix="/api/v1")

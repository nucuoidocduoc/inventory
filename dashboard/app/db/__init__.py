from app.common.utils import hash_string
from app.db.mongo import Mongo
from app.db.mongo.documents.account import Account
from appsettings import MONGO_CONNECTION_STRING


def do_connect_databases():
    mongo = Mongo(MONGO_CONNECTION_STRING)
    mongo.connect()
    seed_data()

def seed_data():
    admin_account = Account.objects(email="admin").first()
    if admin_account is None:
        admin_account = Account(
            email='admin', hash_password=hash_string('Admin@123'+'admin'))
        admin_account.save()
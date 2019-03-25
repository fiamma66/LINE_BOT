
"""
放入資料庫密碼
"""


class MongoBase:
    username = "root"
    password = "PASSWORD"
    authSource = "res"
    authMechanism = 'SCRAM-SHA-256'


class MyAccount:
    account = "USERNAME"
    passwd = "PASSWORD"
    host = "RDS_HOST"
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


engine = os.environ.get('INSTA_DB_ENGINE', 'default')
user = os.environ.get('INSTA_DB_USER', 'default')
password = os.environ.get('INSTA_DB_PASSWORD', 'default')
host = os.environ.get('INSTA_DB_HOST', 'default')
port = os.environ.get('INSTA_DB_PORT', '5432')
database = os.environ.get('INSTA_DB_DATABASE', 'default')
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}:{}/{}'.format(engine,
                                                                     user,
                                                                     password,
                                                                     host,
                                                                     port,
                                                                     database)

db = SQLAlchemy(app)
# class DB(object):
#     """
#     Database Object
#     """
#     def __init__(self):
#         """
#         Initialize the Database Object
#         """
#         engine = os.environ.get('INSTA_DB_ENGINE', 'default')
#         user = os.environ.get('INSTA_DB_USER', 'default')
#         password = os.environ.get('INSTA_DB_PASSWORD', 'default')
#         host = os.environ.get('INSTA_DB_HOST', 'default')
#         port = os.environ.get('INSTA_DB_PORT', '5432')
#         database = os.environ.get('INSTA_DB_DATABASE', 'default')
#         self._engine = create_engine(engine + '://' + user + ':'
#                                      + password + '@'
#                                      + host + ':' + port + '/'
#                                      + database, echo=True)
#         self._engine.connect()
#         print(self._engine.table_names())
#
#     def get(self, table: str, fields: list=None, conditions: list=None):
#         pass
#
#
# db = DB()

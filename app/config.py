import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    USERNAME = 'anna'
    PASSWORD = 'pass'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'sekret_key'
    UPLOAD_DIRECTORY = os.path.join(basedir, '')

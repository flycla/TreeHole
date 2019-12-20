import logging

DEBUG = True
HOST = None
PORT = None
APP_SECRET_KEY = 'SECRET KEY'
DATABASE = 'database.db'
DATABASE_INIT = 'database.sql'
LOG_FILE = ''
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s:%(message)s'

CAS_ENABLE = False
CAS_SERVER = 'http://foo/cas'
CAS_AFTER_LOGIN = 'index'

RECAPTCHA = 'https://www.recaptcha.net/recaptcha/api/siteverify'
RECAPTCHA_SERVKEY = 'YOUR RECAPTCHA v2 SERVKEY'
RECAPTCHA_SITEKEY = 'YOUR RECAPTCHA v2 SITEKEY'

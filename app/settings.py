import os


class Config(object):
    OIDC_CLIENT_SECRETS = 'client_secrets.json'  
    SECRET_KEY = os.environ.get("SECRET_KEY")  



class ProductionConfig(Config):
    APP_ENVIRONMENT = 'Production'
    TESTING = False
    DEBUG = False
    LOGIN_URL = 'http://maxsessions.com/login'



class DevelopmentConfig(Config):
    APP_ENVIRONMENT = 'Development'
    TESTING = True
    DEBUG = True
    LOGIN_URL = 'http://127.0.0.1:5000/login'

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

ENV = os.environ.get('ENV')

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_CONNECT_STRING = f'postgresql+pg8000://{ DB_USER }:{ DB_PASS }@{ DB_HOST }/{ DB_NAME }'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DB_CONNECT_STRING
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevConfig(Config):
#     DEBUG = True

# class TestConfig(Config):
#     TESTING = True
#     SQLALCHEMY_ECHO = True

# class ProdConfig(Config):
#     DEBUG = False

# CONFIG_DICT = {
#     'DEV': DevConfig,
#     'TEST': TestConfig,
#     'PROD': ProdConfig,
# }
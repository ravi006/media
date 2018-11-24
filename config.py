import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

# install globally autoenv, then and add a .env file
# pip install autoenv==1.0.0
# touch .env , add this lines
# source env/bin/activate
# export APP_SETTINGS="config.DevelopmentConfig"
# and echo the setting bashrc file
# $ echo "source `which activate.sh`" >> ~/.bashrc
# $ source ~/.bashrc
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

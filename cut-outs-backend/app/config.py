import os

appRoot = os.environ.get('PLATFORM_APP_DIR') or os.path.dirname(os.path.dirname(__file__))

class Config(object):
    PREFIX = os.environ.get('APP_PATH') or '/apps'
    SECRET_KEY = os.environ.get('PLATFORM_PROJECT_ENTROPY') or 'development_secret_key'
    SCORE_PATH = os.path.join(appRoot, "resources/scores")
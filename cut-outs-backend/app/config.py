import os

class Config(object):
    SECRET_KEY = os.environ.get('PLATFORM_PROJECT_ENTROPY') or 'Developer key'
    SCORE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/resources/scores"
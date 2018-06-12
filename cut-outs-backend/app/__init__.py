from flask import Flask
from app.config import Config
import os

app_path = os.environ.get('APP_PATH') or '/apps'

app = Flask(
    __name__,
    static_url_path=app_path + '/static'
    )

from app import routes

app.config.from_object(Config())

# coding=utf-8
from __future__ import unicode_literals

import os
from flask import Flask
from .config import Config
base_path = os.path.abspath(os.path.dirname(__file__))




def create_app():
    app = Flask(__name__, static_folder='templates', static_url_path='')


    # 使用蓝图（Blueprint）关联程序
    # 关联 api
    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


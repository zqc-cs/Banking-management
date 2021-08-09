# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: __init__.py.py
@time: 2021/06/06
"""
from flask import Flask
from .main import main as main_blueprint
from .customers import customers as customers_blueprint
from .accounts import accounts as accounts_blueprint
from .loans import loans as loans_blueprint
from .statistics import statistics as statistics_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(customers_blueprint)
    app.register_blueprint(accounts_blueprint)
    app.register_blueprint(loans_blueprint)
    app.register_blueprint(statistics_blueprint)

    app.config['SECRET_KEY'] = 'dev'
    return app

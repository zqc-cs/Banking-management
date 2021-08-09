# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: __init__.py.py
@time: 2021/06/09
"""
from flask import Blueprint


accounts = Blueprint("accounts", __name__)
from . import views

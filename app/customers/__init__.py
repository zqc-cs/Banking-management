# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: __init__.py.py
@time: 2021/06/06
"""
from flask import Blueprint


customers = Blueprint('customers', __name__)
from . import views


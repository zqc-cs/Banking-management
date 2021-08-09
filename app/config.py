# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:aa
@file: config.py.py
@time: 2021/06/06
"""
from sqlalchemy import MetaData,Table
from sqlalchemy import create_engine
# declarative_base类维持了一个从类到表的关系
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOST = 'localhost'
PORT = 3306
DATABASE = 'lab3'
USERNAME = 'root'
PASSWORD = ''

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import db_conn
from core import views

if __name__ == '__main__':
    views.cmd_interactive()
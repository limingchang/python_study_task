# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)
from core import main
main.show_menu()
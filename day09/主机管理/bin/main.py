# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from core import host_manage
from core import ssh_class



ssh_obj = ssh_class.SSH_Manage()
manage = host_manage.Host_Manage(ssh_obj)
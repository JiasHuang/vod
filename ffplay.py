#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def setAct(act, val):
    if act == 'stop':
        os.system('killall -9 ffplay')
    else:
        print('unsupported: %s %s' %(act, val))
        return


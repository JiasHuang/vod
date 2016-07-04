#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xdef

def setAct(act, val):

    if act == 'forward' and val:
        cmd = 'seek %s' %(val)
    elif act == 'backward' and val:
        cmd = 'seek -%s' %(val)
    elif act == 'percent' and val:
        cmd = 'seek %s absolute-percent' %(val)
    elif act in ['osd', 'mute', 'pause', 'stop', 'playlist-next', 'playlist-prev', 'sub-remove']:
        cmd = '%s' %(act)
    else:
        print 'unsupported: %s %s' %(act, val)
        return
 
    os.system('echo %s > %s' %(cmd, xdef.fifo))


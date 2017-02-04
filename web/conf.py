#!/usr/bin/env python

import os

vodpath = '/opt/vod/'
workdir = '/tmp/'

vod  = vodpath+'vod.py'
src  = vodpath+'src.py'
run  = vodpath+'run.py'
act  = vodpath+'act.py'
cmd  = vodpath+'cmd.py'
log  = workdir+'view.log'
json = workdir+'view.json'

def loadConf(path):
    conf = os.path.expanduser('~')+'/.vodconf'
    os.system('cp -f %s %s' %(path, conf))

def readConf():
    conf = os.path.expanduser('~')+'/.vodconf'
    txt = ''
    if os.path.exists(conf):
        fd = open(conf, 'r')
        txt = fd.read()
        fd.close()
    return txt

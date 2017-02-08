#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

import xdef
import xurl
import xproc
import youtubedl

def setAct(act, val):

    if act == 'forward' and val:
        cmd = 'seek %s' %(int(val) * 1000000)
    elif act == 'backward' and val:
        cmd = 'seek -%s' %(int(val) * 1000000)
    elif act == 'percent' and val:
        with open(xdef.log, 'r') as fd:
            m = re.search(r'Duration: (.*?):(.*?):(.*?),', fd.read())
            if m:
                duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(float(m.group(3)))
                position = duration * int(val) * 1000000 / 100
                cmd = 'setposition %s' %(position)
            else:
                print('Get Duration Fail')
                return
    elif act in ['pause', 'stop']:
        cmd = '%s' %(act)
    else:
        print('unsupported: %s %s' %(act, val))
        return

    print('\n[omxp][act]\n\n\t%s%s %s' %(xdef.codedir, 'dbuscontrol.sh', cmd))
    result = subprocess.check_output('%s%s %s' %(xdef.codedir, 'dbuscontrol.sh', cmd), shell=True)
    print('\n[omxp][result]\n\n\t%s' %(result))
    return

def play(url, ref):

    xargs = ''

    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if not url:
        print('\n[omxp][play] invalid url\n')
        return
    if xproc.checkProcessRunning('omxplayer.bin'):
        setAct('stop', None)

    cookies = xurl.readLocal(xdef.cookiex)
    if cookies != '':
        xargs += ' --cookies \'%s\'' %(cookies)

    cmd = '%s %s \'%s\' 2>&1 | tee %s' %(xdef.omxp, xargs, url, xdef.log)
    print('\n[omx][cmd]\n\n\t'+cmd+'\n')
    subprocess.Popen(cmd, shell=True).communicate()

    return


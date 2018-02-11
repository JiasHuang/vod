#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import time

import xdef
import xproc
import xsrc
import xurl

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
        print('unsupported: %s %s' %(act, val))
        return

    os.system('echo %s > %s' %(cmd, xdef.fifo))
    return

def play(url, ref):

    p = None
    xargs = []

    url, cookies, ref = xsrc.getSource(url, ref=ref)

    if not url:
        print('\n[mpv][play] invalid url\n')
        return

    if cookies and re.search(r'google.com', url) and xproc.checkProcessRunning('mpv'):
        os.system('echo stop > %s' %(xdef.fifo))
        while xproc.checkProcessRunning('mpv'):
            time.sleep(1)

    if not xproc.checkProcessRunning('mpv'):

        xargs.append('--user-agent=\'%s\'' %(xurl.defvals.ua))
        xargs.append('--referrer=\'%s\'' %(ref))

        if cookies:
            xargs.append('--http-header-fields="Cookie:%s"' %(cookies))

        cmd = '%s %s \'%s\'' %(xdef.mpv, ' '.join(xargs), url)
        print('\n[mpv][cmd]\n\n\t'+cmd+'\n')
        p = subprocess.Popen(cmd, shell=True)

    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))
        os.system('echo sub-remove > %s' %(xdef.fifo))

    sub = xsrc.getSUB(ref)
    if sub:
        os.system('echo sub-add \"%s\" select > %s' %(sub, xdef.fifo))

    if p:
        p.communicate()

    return

def append(url):
    os.system('echo loadfile \"%s\" append > %s' %(url, xdef.fifo))
    return

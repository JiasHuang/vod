#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import xdef
import xproc
import youtubedl

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

    xargs = ''

    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
        xargs = '--ytdl=no'

    if not url:
        print('\n[mpv][play] invalid url\n')
        return

    if not xproc.checkProcessRunning('mpv'):

        if os.path.exists('/etc/alternatives/x86_64-linux-gnu_libvdpau_nvidia.so'):
            xargs = xargs + ' --hwdec=vdpau'

        xargs = xargs + ' --user-agent=\'%s\'' %(xdef.ua)
        xargs = xargs + ' --referrer=\'%s\'' %(ref)
        xargs = xargs + ' --input-file=\'%s\'' %(xdef.fifo)
        xargs = xargs + ' --cookies --cookies-file=\'%s\'' %(xdef.cookies)

        cmd = '%s %s \'%s\'' %(xdef.mpv, xargs, url)
        print('\n[mpv][cmd]\n\n\t'+cmd+'\n')
        subprocess.Popen(cmd, shell=True).communicate()

    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))
        os.system('echo sub-remove > %s' %(xdef.fifo))

    sub = youtubedl.extractSUB(ref)
    if sub:
        os.system('echo sub-add \"%s\" select > %s' %(sub, xdef.fifo))

    return

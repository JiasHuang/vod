#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

import xdef
import xproc
import youtubedl

def setAct(act, val):

    output = subprocess.check_output('xdotool search ffplay', shell=True)
    wid = re.search(r'([0-9]*)$', output)
    if wid:
        os.system('xdotool windowactivate '+wid.group(1))

    if act == 'stop':
        os.system('xdotool key q')
    elif act == 'pause':
        os.system('xdotool key p')
    elif act == 'forward':
        os.system('xdotool key Up')
    elif act == 'backward':
        os.system('xdotool key Down')
    else:
        print('unsupported: %s %s' %(act, val))
    return

def play(url, ref):
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if not url:
        print('\n[ffplay][play] invalid url')
        return 0
    if xproc.checkProcessRunning('ffplay'):
        setAct('stop', None)
    p = subprocess.Popen('%s \'%s\' 2>&1 | tee %s' %(xdef.ffplay, url, xdef.log), shell=True)
    if p:
        p.communicate()
    return

